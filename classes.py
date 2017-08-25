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
        self.start = start
        self.end = end
        self.orientation = orientation
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
