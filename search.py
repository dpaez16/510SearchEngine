import metapy
import pytoml
import sys

def performSearch(q, number_of_results, ranker):
    idx = metapy.index.make_inverted_index('citeseer-config.toml')
    query = metapy.index.Document()
    query.content(q.strip().lower())
    results = ranker.score(idx, query, number_of_results)
    searchResults = []
    for result in results:
        docIdx = result[0]
        content = idx.metadata(docIdx).get('content')
        content = "{}...".format(content[:250])
        searchResults.append((docIdx, content))
    return searchResults

ranker = metapy.index.OkapiBM25(k1=1.2,b=0.75,k3=500)

searchResults = performSearch(sys.argv[1], int(sys.argv[2]), ranker)
searchResultsFile = open('searchResults.txt', 'w+')
for docIdx, doc in searchResults:
    searchResultsFile.write("{}----------{}\n".format(docIdx, doc))

searchResultsFile.close()