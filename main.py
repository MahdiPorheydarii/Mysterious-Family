import networkx as nx
import dash
from dash import dcc, html
import matplotlib.pyplot as plt
from src.plot import plot_family_tree, graph_to_plotly
from src.Tree import family

fam = family()

graph = nx.DiGraph()
pos = plot_family_tree(fam.root, graph=graph)
labels = {node: node.name for node in graph.nodes()}
nx.draw(graph, pos=pos, with_labels=True, labels=labels, node_size=1500, node_color="#33FFC1", font_size=10)
plt.show()


app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Graph(id='family-tree-graph', figure=graph_to_plotly(graph, pos)),
])

if __name__ == '__main__':
    app.run_server(debug=True)