class primer_results(object):
    def __init__(self, poly_name, primer_pair, sequence):
        self.name = poly_name
        self.primer_pair = primer_pair
        self.sequence = sequence
        print(type(self.primer_pair))
        self.left_primer = self.primer_pair.left_primer
        self.right_primer = self.primer_pair.right_primer
        # add logic to automatically name primers based on the poly_name
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
        s = "Primer: " + self.primer_name + '\t' + self.primer_sequence + '\tTm: ' + str(self.primer_tm)
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


