import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import poisson, expon
from tqdm import tqdm
import random

%matplotlib inline
graph=nx.read_gml("map.gml")


# number of nodes and edges
n, m = graph.number_of_nodes(), graph.number_of_edges()
print(f"Num nodes: {n}, Num edges: {m}")

# connected components
connected_components = nx.connected_components(graph)
subgraphs = [graph.subgraph(c) for c in connected_components]
print(f"Num connected components: {len(subgraphs)}")
for subgraph in subgraphs:
	num_nodes = subgraph.number_of_nodes()
	print(f"Num nodes in component: {num_nodes}")


# largest connected component
large_subgraph = max(subgraphs, key=lambda x: x.number_of_nodes())
small_subgraph = min(subgraphs, key=lambda x: x.number_of_nodes())
# TODO: diameter
# diameter = nx.diameter(largest_subgraph)
# print(f"Diameter of largest connected component: {diameter}")


# mean degree
mean_degree = np.mean(list(dict(graph.degree()).values()))
mean_degree_square = np.mean([degree**2 for degree in dict(graph.degree()).values()])
print(f"Mean degree: {mean_degree}, Mean degree squared: {mean_degree_square}")

# max degree
max_degree = max(dict(graph.degree()).values())
print(f"Max degree: {max_degree}")


# degree distribution
def degree_distribution_plot(graph):
	degrees = [graph.degree(node) for node in graph.nodes()]
	plt.hist(degrees, bins=np.arange(0, 21), density=True)
	plt.xlabel("Degree")
	plt.ylabel("Density")
	plt.title("Degree Distribution")
	plt.show()

degree_distribution_plot(graph)


# compare with Erdos-Renyi Graph
p = mean_degree / (n-1)
print(f"p in ER graph: {p}")

ER_graph = nx.erdos_renyi_graph(n, p)
degree_distribution_plot(ER_graph)


# clustering coefficient
clustering_coef = nx.average_clustering(graph)
print(f"Clustering coefficient: {clustering_coef}")


# plot the component
large_subgraph = max(subgraphs, key=lambda x: x.number_of_nodes())
pos = nx.spring_layout(large_subgraph, iterations=100)
nx.draw(large_subgraph, pos, with_labels=False, node_size=100, font_size=8)
plt.show()


# verify a graph of map is of course planar
nx.is_planar(graph)


def get_centrality(graph):
	centrality_dict = {}
	centrality_dict['degree'] = nx.degree_centrality(graph)
	centrality_dict['betweenness'] = nx.betweenness_centrality(graph, k=100, weight='weight')
	centrality_dict['closeness'] = nx.closeness_centrality(graph, distance='weight')
	centrality_dict['pagerank'] = nx.pagerank(graph)
	return centrality_dict

centrality_dict = get_centrality(graph)

# get nodes with highest centrality score
def get_top_k_nodes(centrality_dict, k):
	top_k_nodes = {}
	for key in centrality_dict:
		top_k_nodes[key] = sorted(centrality_dict[key].items(), key=lambda x: x[1], reverse=True)[:k]
	return top_k_nodes

top_k_nodes = get_top_k_nodes(centrality_dict, k=5)
for key in centrality_dict:
	print(f"Measure: {key}")
	for node in top_k_nodes[key]:
		print(node)


# SSSP from my dormitory
source = '71'
shortest_path = nx.single_source_dijkstra_path_length(graph, source=source, weight='weight')
print(shortest_path)


# average distance between nodes
num_nodes = 171
node_samples = large_subgraph.nodes()
sum_shortest_path_lengths = sum(l for u in node_samples for l in nx.single_source_dijkstra_path_length(large_subgraph, u, weight='weight').values())
average_distance = sum_shortest_path_lengths / (num_nodes * (large_subgraph.number_of_nodes()-1))
average_distance

# longest distance between nodes
longest_distance = max(l for u in node_samples for l in nx.single_source_dijkstra_path_length(large_subgraph, u, weight='weight').values())
longest_distance

nx.diameter(large_subgraph, weight='weight')


# robustness: randomly remove nodes and see how the size of the largest connected component changes
def random_node_deletion_experiment(G, num_iterations=10, end=150, step=1):
	results = []
	for i in tqdm(range(1, end, step)):
		max_connected_components = []
		for _ in range(num_iterations):
			H = G.copy()
			nodes_to_remove = random.sample(H.nodes(), i)
			H.remove_nodes_from(nodes_to_remove)
			connected_components = list(nx.connected_components(H))
			if connected_components:
				max_connected_components.append(max(map(len, connected_components)))
			else:
				max_connected_components.append(0)
		average_max_connected_component = sum(max_connected_components) / num_iterations
		results.append(average_max_connected_component)
	return results

result = random_node_deletion_experiment(graph, num_iterations=10, end=170, step=2)
x = np.arange(1, 170, 1)
plt.plot(x, result)


def attack_sequential_deletion_experiment(graph, end=150, step=1):
    # delete nodes with highest degree sequentially
    results = []
    graph = graph.copy()
    for _ in tqdm(range(1, end, step)):
        nodes_to_remove = sorted(graph.nodes(), key=graph.degree, reverse=True)[:step]
        graph.remove_nodes_from(nodes_to_remove)
        connected_components = list(nx.connected_components(graph))
        results.append(max(map(len, connected_components)))
    return results

result = attack_sequential_deletion_experiment(graph, end=170, step=1)
x = np.arange(1, 170, 1)
plt.plot(x, result)
