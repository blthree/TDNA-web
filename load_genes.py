from pick_tdna_primers import run_tdna_primers
import json
import gzip
monster = 'At1g01010	chr1:000003760	0.0	W/3760-3913,3996-4276,4486-4605,4706-5095,5174-5326,5439-5630	' \
'AT1G01010.1 CDS NAC domain containing protein 1 [TAIR10] CDS gene_syn ANAC001, NAC domain containing protein 1, ' \
'NAC001, T25K16.1, T25K16_1 gene ' \
'NAC001 go_process regulation of transcription|GO:0045449||IEA go_component cellular_component|GO:0005575||' \
'ND go_process multicellular organismal development|GO:0007275||ISS go_function sequence-specific DNA binding transcription factor activity' \
'|GO:0003700|11118137|ISS product NAC domain containing protein 1 note NAC domain containing protein 1 (NAC001);' \
' FUNCTIONS IN: sequence-specific DNA binding transcription factor activity; ' \
'INVOLVED IN: multicellular organismal development, regulation of transcription; ' \
'LOCATED IN: cellular_component unknown; EXPRESSED IN: 7 plant structures; ' \
'EXPRESSED DURING: 4 anthesis, C globular stage, petal differentiation and expansion stage;' \
' CONTAINS InterPro DOMAIN/s: No apical meristem (NAM) protein (InterPro:IPR003441); ' \
'BEST Arabidopsis thaliana protein match is: NAC domain containing protein 69 (TAIR:AT4G01550.1); ' \
'Has 2503 Blast hits to 2496 proteins in 69 species: Archae - 0; Bacteria - 0; Metazoa - 0; Fungi - 0; Plants - 2502; Viruses - 0; Other Eukaryotes - 1 (source: NCBI BLink). ' \
'protein_id AT1G01010.1p transcript_id AT1G01010.1 protein_id AT1G01010.1p transcript_id AT1G01010.1'

monster_list = monster.split('\t')
def split_line(monster_list):
    monster_list = monster_list.split('\t')
    a = monster_list[:4]
    print(a)
    name = a[0]
    b = a[1].split(':')
    chrom = b[0]
    start = int(b[1])
    c = a[3].split('/')
    ori = c[0]
    d = [(x,y) for x,y in [z.split('-') for z in c[1].split(',')]]
    end = d[-1][1]
    info = {"AGI":name, "chr":chrom, "start":start, "end":end, "orientation":ori, "exons":d}
    print(info)
    return info

def save_json_compressed():
    f = open("C:\\Users\\lindsey.152\\PycharmProjects\\TDNA-web\\static\\data\\GENE.ANNO.ARAPORTv11-Aug2015", 'r')
    f2 = open("C:\\Users\\lindsey.152\\PycharmProjects\\TDNA-web\\static\\data\\genes-small.txt", 'w+')
    gf2 = gzip.GzipFile("C:\\Users\\lindsey.152\\PycharmProjects\\TDNA-web\\static\\data\\genes-small.json.gz", 'w')
    new_list = []
    for l in f.readlines():
        new_list.append(split_line(l))
    json_str = json.dumps(new_list) + '\n'
    json_bytes = json_str.encode('utf-8')
    gf2.write(json_bytes)


def read_json_compressed():
    gf2 = gzip.GzipFile("C:\\Users\\lindsey.152\\PycharmProjects\\TDNA-web\\static\\data\\genes-small.json.gz", 'r')
    json_bytes = gf2.read()
    json_str = json_bytes.decode('utf-8')
    data = json.loads(json_str)
    print(type(data))