from pick_tdna_primers import run_tdna_primers
import json
import gzip
import os

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
    d = [(x, y) for x, y in [z.split('-') for z in c[1].split(',')]]
    end = d[-1][1]
    info = {"name": name, "chrom": chrom, "start": start, "end": end, "orientation": ori, "exons": d}
    return info

def save_json_compressed():
    base_path = os.getcwd()

    f = open(os.path.join(base_path,"static","data","GENE.ANNO.ARAPORTv11-Aug2015"), 'r')
    f2 = open(os.path.join(base_path,"static", "data", "genes-small.txt"), 'w+')
    gf2 = gzip.GzipFile(os.path.join(base_path, "static", "data", "genes-small.json.gz"), 'w+')
    new_list = []
    for l in f.readlines():
        new_list.append(split_line(l))
    json_str = json.dumps(new_list) + '\n'
    json_bytes = json_str.encode('utf-8')
    gf2.write(json_bytes)


def read_json_compressed():
    base_path = os.getcwd()
    gf2 = gzip.GzipFile(os.path.join(base_path, "static", "data", "genes-small.json.gz"), 'r')
    json_bytes = gf2.read()
    print(json_bytes)
    json_str = json_bytes.decode('utf-8')
    print(json_str)
    data = json.loads(json_str)
    return data