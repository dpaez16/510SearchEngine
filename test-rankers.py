import metapy
import pytoml
import numpy as np
def train_queries(config, q):
	scores = {}
	best_scores = {}
	idx = metapy.index.make_inverted_index(config)
	f_index = metapy.index.make_forward_index(config)
	# First test various jelinek mercer

	scores = {}
	l = np.linspace(0,1,10)
	for i in l:
		title = "jelinek with: " + str(i)
		ranker = metapy.index.JelinekMercer(i)
		scores[title] = run_training_ranker(ranker, idx, config, q)
	title, score = max(scores.items(), key= lambda k: k[1])
	print((title, score))
	best_scores[title] = score
	scores = {}
	k1_options = np.linspace(0, 2, 20)
	b_options = np.linspace(0, 1, 10)
	# TRY OUT DIFFERNT OKAPI
	for k1 in k1_options:
		for b in b_options:
			title = "okapi with: " + str((k1, b, 500))
			ranker = metapy.index.OkapiBM25(k1, b, 500)
			scores[title] = run_training_ranker(ranker, idx, config, q)
	title, score = max(scores.items(), key= lambda k: k[1])
	print((title, score))
	best_scores[title] = score
	
	# TRY OUT DIFFERENT ROCCHIO
	scores = {}
	alpha_o = np.linspace(0, 1.2, 10)
	beta_o = np.linspace(0,1.2, 10)
	for alpha in alpha_o:
		for beta in beta_o:
			title = "rocchio with (alpha, beta, k) : " + str((alpha, beta, 7))
			ranker = metapy.index.Rocchio(fwd = f_index, alpha = alpha, beta = beta, k = 7, initial_ranker = metapy.index.OkapiBM25())
			scores[title] = run_training_ranker(ranker, idx, config, q)
	title, score = max(scores.items(), key= lambda k: k[1])
	print((title, score))
	best_scores[title] = score
	# try out pivoted Length
	scores = {}
	s_options = np.linspace(0, 1, 10)
	for s in s_options:
		title = "pivoted length with s = " + str(s)
		ranker = metapy.index.PivotedLength(s)
		scores[title] = run_training_ranker(ranker, idx, config, q)
	title, score = max(scores.items(), key= lambda k: k[1])
	best_scores[title] = score
	print((title, score))
	print('===============')
	print('overall results:')
	print(best_scores)


def run_training_ranker(ranker, idx, config_file, q):
	ev = metapy.index.IREval(config_file)
	query = metapy.index.Document()
	vals = []
	with open(q) as query_file:
	    for query_num, line in enumerate(query_file):
	        query.content(line.strip())
	        results = ranker.score(idx, query, 20)                            
	        val = ev.ndcg(results, query_num, 20)
	        vals.append(val)
	return sum(vals) / len(vals)


config = 'citeseer-config.toml'
q = 'citeseer/citeseer-queries.txt'
train_queries(config, q)

