
from pyfaidx import Fasta
import os
from classes import primer_results as pr
from classes import primer, primer_pair

#global PATH to app root
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def run_tdna_primers(input_stock_num, maxn=300, ext5=300, ext3=300, p_zone=200, show_seq=False):
    # TODO: add option to show primer3 output details and save to file

    sequence_length_defs = {
        'maxN': maxn,
        'ext5': ext5,
        'ext3': ext3,
        'p_zone': p_zone * 2  # size of left and right regions together, so twice the Signal.salk.edu value
    }

    data_filenames = ['T-DNA.SALK', 'T-DNA.SAIL', 'T-DNA.GABI']

    #print(os.path.join(os.getcwd(),data_filenames[0]))
    db = init_db(data_filenames)
    fasta_path = os.path.join(APP_ROOT, 'static', 'data', 'AT9.fa')
    genome = Fasta(fasta_path)

    result = []
    for poly_name, poly_info in db[input_stock_num].items():
        print('Making primers for ' + poly_name + '\n')
        sequence = get_seq(poly_info, sequence_length_defs, genome)
        if show_seq is True:
            print('Genomic sequence around insert:\n')
            print(sequence)
            print('\n')

        conf_path = os.path.join(APP_ROOT, 'static', 'primer3.conf')
        p3s, p3p = load_conf(conf_path)
        primer_results = make_primers(sequence, sequence_length_defs, p3s, p3p)
        # need to label results. Need to use a dict for results
        LP_out = primer_results['PRIMER_LEFT_0_SEQUENCE']
        LP_tm = round(primer_results['PRIMER_LEFT_0_TM'], 1)
        RP_out = primer_results['PRIMER_RIGHT_0_SEQUENCE']
        RP_tm = round(primer_results['PRIMER_RIGHT_0_TM'], 1)
        a = pr(poly_name, primer_pair((primer(LP_out,LP_tm),primer(RP_out, RP_tm))), sequence)

        result.append(a)
    return result


def split_input(string, chunk_size):
    num_chunks = len(string)//chunk_size
    if (len(string) % chunk_size != 0):
        num_chunks += 1
    output = []
    for i in range(0, num_chunks):
        output.append(string[chunk_size*i:chunk_size*(i+1)]+'\n')
    return output

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def init_db(filenames):
    assert type(filenames) == list, "Filenames must be in the form of a list"
    records = {}

    for fname in filenames:
        fname = os.path.join(APP_ROOT, 'static','data', fname)
        f = open(fname, 'r')
        for line in f:
            s_line = line.strip('\n').split('\t')
            stock_name = s_line[0].split('.')[0]
            poly_name = s_line[0]
            poly_chr = s_line[1].split(':')[0]
            poly_chr = poly_chr[3:]
            poly_locs = s_line[3].split(',')[0]
            poly_start = poly_locs.split('/')[1].split('-')[0]
            poly_end = poly_locs.split('/')[1].split('-')[1]
            orientation = s_line[3].split('/')[0]
            # load into dict of dicts object
            if stock_name in records and poly_name in records[stock_name]:
                records[stock_name][poly_name + '.1'] = {'chr': poly_chr, 'orientation': orientation,
                                                         'start': poly_start,
                                                         'end': poly_end}
            elif stock_name not in records:
                records[stock_name] = {
                    poly_name: {'chr': poly_chr, 'orientation': orientation, 'start': poly_start, 'end': poly_end}}
            else:
                records[stock_name][poly_name] = {'chr': poly_chr, 'orientation': orientation, 'start': poly_start,
                                                  'end': poly_end}
    return records


def load_conf(conf_file):
    """
    loads all the settings for primer3 from the default file
    :param conf_file: string path to conf file
    :return: p3s: dict, p3p: dict
    """
    f = open(conf_file, 'r')
    p3s = {}
    p3p = {}
    for line in f.readlines():
        line = line.strip()
        value = line.split(',')[1]
        # divide into two separate dictionaries
        if line.startswith('SEQUENCE'):
            p3s[line.split(',')[0]] = value
        elif line.startswith('PRIMER'):
            # perform type conversions if needed
            # TODO: add handling for list arguments like PRIMER_PRODUCT_SIZE_RANGE
            if is_int(value):
                value = int(value)
            elif is_float(value):
                value = float(value)
            else:
                pass
            p3p[line.split(',')[0]] = value
        else:
            pass
    return p3s, p3p


def get_seq(poly_entry, sequence_length_defs, genome):
    """
    :param poly_entry: dict item
    'SALK_001127.52.15.x': {'chr': '1', 'orientation': 'W', 'start': '32', 'end': '303'}
    :param sequence_length_defs: dict
    :param genome: pyfaidx.Fasta
    :return seq: DNA sequence as string
    """
    # calculate the upstream and downstream distances based on the sequence input params
    bp_upstream = sequence_length_defs['maxN'] + sequence_length_defs['ext5'] + int(sequence_length_defs['p_zone'] / 2)
    bp_downstream = sequence_length_defs['ext3'] + int(sequence_length_defs['p_zone'] / 2)
    total_bp = bp_upstream + bp_downstream
    chrom = 'chr' + poly_entry['chr']

    # logic to account for orientation of T-DNA insert
    if poly_entry['orientation'] == 'W':
        new_start = max(1, int(poly_entry['start']) - bp_upstream)
        new_end = max(min(int(poly_entry['start']) + bp_downstream + 1, len(genome[chrom])), total_bp + new_start)
        seq = genome[chrom][new_start:new_end]
    elif poly_entry['orientation'] == 'C':
        #print("reverse")
        new_start = max(int(poly_entry['end']) - bp_downstream, 1)
        new_end = max(min(int(poly_entry['end']) + bp_upstream, len(genome[chrom])), new_start + total_bp)
        #print(chrom,new_start,new_end)
        #print(new_start-new_end)
        seq = -genome[chrom][new_start:new_end]
    else:
        raise ValueError("Orientation must be 'W' or 'C'!")

    return str(seq)


def make_primers(sequence, sequence_length_defs, primer3_seq_args, primer3_primer_args):
    from primer3 import designPrimers
    from functools import reduce
    '''default iSECT values:
    size: optimal=21 min=18 max=28
    Tm: opt=61 Min=53 Max=71
    %GC: min=20 max=80
    clamp=1
    maxN=300 ext5=300 ext3=300
    primer_zone=200
    BPos=110 (distance from LB primer to insertion site)
    '''
    total = reduce(lambda x, y: x + y, [v for v in sequence_length_defs.values()])
    primer3_seq_args['SEQUENCE_PRIMER_PAIR_OK_REGION_LIST'] = [0, int(sequence_length_defs['p_zone'] / 2),
                                                               total - int((sequence_length_defs['p_zone'] / 2)),
                                                               int((sequence_length_defs['p_zone'] / 2))]
    primer3_primer_args['PRIMER_PRODUCT_SIZE_RANGE'] = [total - sequence_length_defs['p_zone'], total]
    primer3_seq_args['SEQUENCE_TEMPLATE'] = sequence
    a = designPrimers(primer3_seq_args, primer3_primer_args)
    return a


if __name__ == '__main__':
    run_tdna_primers()
