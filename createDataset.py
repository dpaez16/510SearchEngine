import metapy

idx = metapy.index.make_inverted_index('citeseer-config.toml')
n = idx.num_docs()
print(n)
#f = open('citeseer.dat', 'w+')

#f.close()
