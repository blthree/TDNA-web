from load_genes import read_json_compressed, save_json_compressed
from classes import gene


data = read_json_compressed()
a = data[0]
name = a['name']
chrom = a['chrom']
start = a['start']
end = a['end']
ori = a['orientation']
exons = a['exons']
test_gene = gene(name, chrom, start, end, ori, exons=exons)
print(test_gene.exons)