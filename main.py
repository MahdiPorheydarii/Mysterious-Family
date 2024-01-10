import networkx as nx
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
from src.plot import plot_family_tree, graph_to_plotly
from src.Tree import family
from src.Classes import Node

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

fam = family()

graph = nx.DiGraph()
pos = plot_family_tree(fam.root, graph=graph)
labels = {node: node.name for node in graph.nodes()}
nx.draw(graph, pos=pos, with_labels=True, labels=labels, node_size=1500, node_color="#33FFC1", font_size=10)
# plt.show()

app.layout = dbc.Container(
    fluid=True,
    children=[
                dbc.Card(
            [
                dbc.CardHeader("^_^"),
                dbc.CardBody(
                    [
                        html.H4("Mysterious Family", className="card-title"),
                        html.P("Welcome to the Mysterious Family family tree web-app!", className="card-text"),
                    ]
                ),
            ],
            className="border-primary mb-3",
            style={"max-width": "100%"},
        ),
        dcc.Graph(id='family-tree-graph', figure=graph_to_plotly(graph, pos),),
        
        dbc.Row([
            dbc.Col(html.Label("Find the farthest child of a node:"), width=2),
            dbc.Col(
                dbc.Input(id='input-node', type='text', placeholder='Enter node name...', className="form-control-plaintext mb-2"),
                width=6
            ),
            dbc.Col(
                html.Button('Submit', id='submit-button', className="btn btn-primary mb-2"),
                width=2
            ),
            dbc.Col(html.Div(id='output-farthest-child', className="text-success"), width=2),
        ]),
    ]

)

@app.callback(
    Output('output-farthest-child', 'children'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('input-node', 'value')]
)
def update_output(n_clicks, input_node):
    if input_node:
        farthest_child = fam.farthest_child(fam.find(Node(input_node)))
        return f"Farthest child of {input_node}: {farthest_child}"

    return None

if __name__ == '__main__':
    app.run_server(debug=True)