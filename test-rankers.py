import metapy
import pytoml
import numpy as np
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def plot2d(x, y, title, x_label):
	plt.figure()
	plt.scatter(x, y)
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel('Avg NDCG @ 20')
	plt.ylim(0.0, 1.0)
	image_name = 'ranker-test/' + title + '.png'
	plt.savefig(image_name)

def plot3d(x, y, z, title, x_label, y_label):
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.scatter(x, y, z)
	plt.title(title)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
	ax.set_zlabel('Avg NDCG @ 20')
	ax.set_zlim(0.0, 1.0)
	image_name = 'ranker-test/' + title + '.png'
	plt.savefig(image_name)

def train_queries(config, q):
	scores = {}
	best_scores = {}
	idx = metapy.index.make_inverted_index(config)
	f_index = metapy.index.make_forward_index(config)
	# First test various jelinek mercer

	scores = {}
	l = np.linspace(0,1,10)
	y = []
	for i in l:
		title = "jelinek with: " + str(i)
		ranker = metapy.index.JelinekMercer(i)
		scores[title] = run_training_ranker(ranker, idx, config, q)
		y.append(scores[title])
	title, score = max(scores.items(), key= lambda k: k[1])
	print((title, score))
	best_scores[title] = score
	plot2d(l, y, "jelinek mercer", 'lambda')
	scores = {}
	k1_options = np.linspace(0, 2, 20)
	b_options = np.linspace(0, 1, 10)
	x = []
	y = []
	z = []
	# TRY OUT DIFFERNT OKAPI
	for k1 in k1_options:
		for b in b_options:
			title = "okapi with: " + str((k1, b, 500))
			ranker = metapy.index.OkapiBM25(k1, b, 500)
			scores[title] = run_training_ranker(ranker, idx, config, q)
			x.append(k1)
			y.append(b)
			z.append(scores[title])
	title, score = max(scores.items(), key= lambda k: k[1])
	print((title, score))
	best_scores[title] = score
	plot3d(x, y, z, 'BM25 (k3 = 500)', 'k1', 'b')
	
	# TRY OUT DIFFERENT ROCCHIO
	scores = {}
	alpha_o = np.linspace(0, 1.2, 10)
	beta_o = np.linspace(0,1.2, 10)
	x = []
	y = []
	z = []
	for alpha in alpha_o:
		for beta in beta_o:
			title = "rocchio with (alpha, beta, k) : " + str((alpha, beta, 7))
			ranker = metapy.index.Rocchio(fwd = f_index, alpha = alpha, beta = beta, k = 7, initial_ranker = metapy.index.OkapiBM25())
			scores[title] = run_training_ranker(ranker, idx, config, q)
			x.append(alpha)
			y.append(beta)
			z.append(scores[title])
	title, score = max(scores.items(), key= lambda k: k[1])
	print((title, score))
	best_scores[title] = score
	plot3d(x, y, z, 'Rocchio (k = 7)', 'alpha', 'beta')
	# try out pivoted Length
	scores = {}
	s_options = np.linspace(0, 1, 10)
	y = []
	for s in s_options:
		title = "pivoted length with s = " + str(s)
		ranker = metapy.index.PivotedLength(s)
		scores[title] = run_training_ranker(ranker, idx, config, q)
		y.append(scores[title])
	plot2d(s_options, y, 'pivoted length', 's')
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

