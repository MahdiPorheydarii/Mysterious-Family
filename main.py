import networkx as nx
import matplotlib.pyplot as plt
from src.plot import plot_family_tree
from src.Tree import family

fam = family()

graph = nx.DiGraph()
pos = plot_family_tree(fam.root, graph=graph)
labels = {node: node.hash for node in graph.nodes()}
nx.draw(graph, pos=pos, with_labels=True, labels=labels, node_size=1500, node_color="#33FFC1", font_size=10)
plt.show()