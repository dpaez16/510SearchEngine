import metapy
import pytoml
import shutil
import os

# creates metapy .toml configuration files
if not os.path.exists("citeseer"):
    os.mkdir("citeseer")

with open('citeseer/citeseer.toml', 'w+') as f:
    f.write('type = "line-corpus"\n')
    f.write('store-full-text = true\n')

config = """prefix = "." # tells MeTA where to search for datasets

dataset = "citeseer" # a subfolder under the prefix directory
corpus = "citeseer.toml" # a configuration file for the corpus specifying its format & additional args

index = "citeseer-idx" # subfolder of the current working directory to place index files

query-judgements = "citeseer/citeseer-qrels.txt" # file containing the relevance judgments for this dataset

stop-words = "lemur-stopwords.txt"

[[analyzers]]
method = "ngram-word"
ngram = 1
filter = "default-unigram-chain"
"""
with open('citeseer-config.toml', 'w+') as f:
    f.write(config)

# starts building the inverted index
print("Creating inverted index ...", end='')
if os.path.exists("citeseer-idx"):
    shutil.rmtree("citeseer-idx")

os.mkdir("citeseer-idx")
idx = metapy.index.make_inverted_index('citeseer-config.toml')

del idx

# do not need this file anymore
os.remove("citeseer/citeseer.dat")
print("Done!")
