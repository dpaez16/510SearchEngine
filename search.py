import metapy
import pytoml
import sys

"""takes in q query, and returns a list of results from the dataset using metapy"""
def performSearch(q, number_of_results):
    idx = metapy.index.make_inverted_index('config.toml')
    query = metapy.index.Document()
    ranker = metapy.index.OkapiBM25(k1=1.2,b=0.75,k3=500)
    query.content(q.strip().lower())
    results = ranker.score(idx, query, number_of_results)
    searchResults = []
    for result in results:
        docIdx = result[0]
        content = idx.metadata(docIdx).get('content')
        content = "{}...".format(content[:250])
        searchResults.append((docIdx, content))
    return searchResults

searchResults = performSearch(sys.argv[1], int(sys.argv[2]))
searchResultsFile = open('searchResults.txt', 'w+')
for searchResult in searchResults:
    searchResultsFile.write("{}\t{}\n".format(searchResult[0], searchResult[1]))

searchResultsFile.close()