import metapy
import pytoml

"""takes in q query, and returns a list of results from the dataset using metapy"""
def performSearch(q, number_of_results):
    idx = metapy.index.make_inverted_index('config.toml')
    query = metapy.index.Document()
    ranker = metapy.index.OkapiBM25(k1=1.2,b=0.75,k3=500)
    query.content(q.strip().lower())
    results = ranker.score(idx, query, number_of_results)
    return results



if __name__ == "__main__":
	performSearch('hello', 5)