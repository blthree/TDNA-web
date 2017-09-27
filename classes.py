class primer_results(object):
    def __init__(self, poly_name, primer_pair, sequence):
        self.name = poly_name
        self.primer_pair = primer_pair
        self.sequence = sequence
        print(type(self.primer_pair))
        self.left_primer = self.primer_pair.left_primer
        self.right_primer = self.primer_pair.right_primer
        # add logic to automatically name primers based on the poly_name
        if self.left_primer.primer_name == '' and self.right_primer.primer_name == '':
            basename = self.name.split('.')[0]
            self.left_primer.primer_name = basename + ' LP'
            self.right_primer.primer_name = basename + ' RP'
    def __str__(self):
        s = "Primer Results for:" + self.name + '\n'
        s += self.primer_pair.__str__() + '\n'
        s += "Sequence used for generating primers:" + '\n' + self.sequence
        return s


class primer(object):
    def __init__(self, primer_sequence, primer_tm=None, primer_name=''):
        self.primer_sequence = primer_sequence
        self.primer_tm = primer_tm
        self.primer_name = primer_name

    def __str__(self):
        s = self.primer_name + '\t' + self.primer_sequence + '\tTm: ' + str(self.primer_tm)
        return s

class primer_pair(object):
    def __init__(self, primer_tuple, primer_pair_name=''):
        self.left_primer = primer_tuple[0]
        self.right_primer = primer_tuple[1]
        self.primer_tuple = primer_tuple
        self.name = primer_pair_name
    def __str__(self):
        s = self.left_primer.__str__() + '\n' + self.right_primer.__str__()
        return s

class polymorphism(object):
    def __init__(self, name):
        self.name = name
        # should this have a method to fetch the sequences, or fetch the sequence then load into this object?




class genomic_loc(object):
    def __init__(self, chrom, start, end, orientation):
        self.chrom = chrom
        self.start = int(start)
        self.end = int(end)
        self.orientation = orientation
        self.loc_tuple = (self.start, self.end)
        if self.orientation == 'C':
            self.is_reverse = True
        else:
            self.is_reverse = False

    def __len__(self):
        l = self.end - self.start
        return l

    def extend(self, upstream=0, downstream=0):
        """
        Extends the coordinates of locations by a specified number of bp on either end
        Modifies existing object in-place and returns None
        :param upstream: int number of bp to extend on the 5' end
        :param downstream: int number of bp to extend on the 3' end
        :return: None
        """
        if not self.is_reverse:
            self.start -= upstream
            self.end += downstream
        elif self.is_reverse:
            self.start -= downstream
            self.end += upstream
        else:
            raise AttributeError("orientation not correctly set")
        return None
    def check_intersect(self, other_loc):
        # need to account for half-open intervals
        range_self = range(self.start, self.end)
        if self.chrom == other_loc.chrom:
            if other_loc.start in range_self or other_loc.end in range_self:
                return True
            else:
                return False
        else:
            return False
    def toString(self):
        s = self.chrom + " " + str(self.start) + " " + str(self.end) + " " + self.orientation
        return s


class gene(genomic_loc):
    def __init__(self, **kwargs):
        for a in kwargs:
            setattr(self, a, kwargs[a])
        super().__init__(self.chrom, self.start, self.end, self.orientation)
        #self.exon_list = self.exons
        self.exon_list = [genomic_loc(self.chrom, int(e[0])-self.start, int(e[1])-self.start, self.orientation) for e in self.exons]
        print()
        self.sequence = ""
    def get_sequence(self, genome):
        seq = genome[self.chrom][self.start:self.end]
        if self.orientation == 'C':
            self.sequence = -seq
        else:
            self.sequence = seq
        return None

"""
LOCUS       Example                   24 bp    DNA              UNK 01-JAN-1980
DEFINITION  An example GenBank file generated by BioPython
ACCESSION   123456789
VERSION     123456789
KEYWORDS    .
SOURCE      .
  ORGANISM  .
            .
FEATURES             Location/Qualifiers
     misc_feature    4..12
ORIGIN
        1 ggggaaaatt ttaaaacccc aaaa
//
"""
