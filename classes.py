class primer_results(object):
    def __init__(self, poly_name, LP, RP, sequence):
        self.name = poly_name
        self.LP = LP
        self.RP = RP
        self.sequence = sequence
        self.lines = [poly_name, LP, RP, sequence]
    def pretty_print(self):
        s = self.name + '\n' + self.LP + '\n' + self.RP + '\n' + 'Sequence' + '\n'.join(self.sequence)
        return s


