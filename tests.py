def test_results_class():
    from classes import primer,primer_pair, primer_results
    a = primer('AAAAGGGGGAAA', 56, 'LP')
    b = primer('GGGGGGCCCCCCCC', 52, 'RP')
    c = primer_pair((a, b))
    d = primer_results('SALK_000000', c, 'AGAGAGAGAGAGAGAGAGAGAGAGAGAG')
    assert d.__str__() == "Primer Results for:SALK_000000" + '\n' + \
                          "Primer: LP	AAAAGGGGGAAA	56" + '\n' + \
                          "Primer: RP	GGGGGGCCCCCCCC	52" + '\n' + \
                          "Sequence used for generating primers:" + '\n' + \
                          "AGAGAGAGAGAGAGAGAGAGAGAGAGAG", "Primer results print __str__() method error"
test_results_class()