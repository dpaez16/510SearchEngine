import metapy
import pytoml

"""takes in q query, and returns a list of results from the dataset using metapy"""
def performSearch(q, number_of_results, idx):
    query = metapy.index.Document()
    ranker = metapy.index.OkapiBM25(k1=1.2,b=0.75,k3=500)
    query.content(q.strip().lower())
    print("before ranker.score")
    results = ranker.score(idx, query, number_of_results)
    print("after ranker.score")
    return results
