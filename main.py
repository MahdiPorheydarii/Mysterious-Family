import networkx as nx
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
from src.plot import plot_family_tree, graph_to_plotly
from src.Tree import family
from dash.exceptions import PreventUpdate
from src.Classes import Node

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
app.config.prevent_initial_callbacks = 'initial_duplicate'

fam = family()

graph = nx.DiGraph()
pos = plot_family_tree(fam.root, graph=graph)
labels = {node: node.name for node in graph.nodes()}
#nx.draw(graph, pos=pos, with_labels=True, labels=labels, node_size=1500, node_color="#33FFC1", font_size=10)
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
            dbc.Col(html.Label("Find the Farthest Child of a node:"), width=2),
            dbc.Col(
                dbc.Input(id='input-node', type='text', placeholder='Enter node name...', className="form-control-plaintext mb-2"),
                width=3
            ),
            dbc.Col(
                html.Button('Find Farthest Child', id='submit-button', className="btn btn-primary mb-2"),
                width=2
            ),
            dbc.Col(html.Div(id='output-farthest-child', className="text-success"), width=2),
        ]),
        dbc.Row([
            dbc.Col(html.Label("Find the Lowest Common Ancestor of two nodes:"), width=3),
            dbc.Col(
                dbc.Input(id='input-node1', type='text', placeholder='First node', className="form-control-plaintext mb-2"),
                width=1
            ),
            dbc.Col(
                dbc.Input(id='input-node2', type='text', placeholder='Second node', className="form-control-plaintext mb-2"),
                width=1
            ),
            dbc.Col(
                html.Button('Find LCA', id='lca-button', className="btn btn-primary mb-2"),
                width=2
            ),
            dbc.Col(html.Div(id='output-lca', className="text-success"), width=2),
        ]),
        dbc.Row([
            dbc.Col(html.Label("Check Relationship Between Two Nodes:"), width=3),
            dbc.Col(
                dbc.Input(id='input-rel-node1', type='text', placeholder='First node', className="form-control-plaintext mb-2"),
                width=1
            ),
            dbc.Col(
                dbc.Input(id='input-rel-node2', type='text', placeholder='Second node', className="form-control-plaintext mb-2"),
                width=1
            ),
            dbc.Col(
                html.Button('Check Relationship', id='rel-button', className="btn btn-primary mb-2"),
                width=2
            ),
            dbc.Col(html.Div(id='output-rel-relationship', className="text-info"), width=2),
        ]),
        dbc.Row(html.Div(style={'height': '20px'})),
        dbc.Row([
            dbc.Col(html.Label("Check if Node Exists:"), width=3),
            dbc.Col(
                dbc.Input(id='input-check-node', type='text', placeholder='Node name', className="form-control-plaintext mb-2"),
                width=2
            ),
            dbc.Col(
                html.Button('Check Node Existence', id='check-node-button', className="btn btn-info mb-2"),
                width=2
            ),
            dbc.Col(html.Div(id='output-check-node', className="text-info"), width=2),
        ]),
        dbc.Row([
            dbc.Col(html.Label("Add a new node:"), width=3),
            dbc.Col(
                dbc.Input(id='input-parent', type='text', placeholder='Parent name', className="form-control-plaintext mb-2"),
                width=1
            ),
            dbc.Col(
                dbc.Input(id='input-new-node', type='text', placeholder='New node name', className="form-control-plaintext mb-2"),
                width=1
            ),
            dbc.Col(
                html.Button('Add Node', id='add-node-button', className="btn btn-success mb-2"),
                width=2
            ),
            dbc.Col(html.Div(id='output-add-node', className="text-info"), width=2),
        ]),
        dbc.Row([
            dbc.Col(
                html.Label("Delete a node:"),
                width=3
            ),
            dbc.Col(
                dbc.Input(id='input-delete-node', type='text', placeholder='Node to delete', className="form-control-plaintext mb-2"),
                width=2
            ),
            dbc.Col(
                html.Button('Delete Node', id='delete-node-button', className="btn btn-danger mb-2"),
                width=2
            ),
            dbc.Col(html.Div(id='output-delete-node', className="text-danger"), width=2),
        ]),
    ]
)

@app.callback(
    Output('output-check-node', 'children'),
    [Input('check-node-button', 'n_clicks')],
    [dash.dependencies.State('input-check-node', 'value')]
)
def check_node_existence(n_clicks, input_check_node):
    if input_check_node:
        node_exists = fam.find(Node(input_check_node)) is not None
        existence_message = f"Node '{input_check_node}' exists." if node_exists else f"Node '{input_check_node}' does not exist."
        return existence_message

    return None

@app.callback(
    [Output('output-delete-node', 'children'),
     Output('family-tree-graph', 'figure')],
    [Input('delete-node-button', 'n_clicks')],
    [dash.dependencies.State('input-delete-node', 'value')]
)
def delete_node(n_clicks, input_delete_node):
    if input_delete_node:
        node_to_delete = fam.find(Node(input_delete_node))
        if node_to_delete.name != None:
            fam.delete(node_to_delete)

            pos = plot_family_tree(fam.root, graph=graph)
            labels = {node: node.name for node in graph.nodes()}
            updated_figure = graph_to_plotly(graph, pos)
            return f"Node '{input_delete_node}' deleted successfully", updated_figure
        else:
            return f"Node '{input_delete_node}' not found", graph_to_plotly(graph, plot_family_tree(fam.root, graph=graph))

    return None, graph_to_plotly(graph, plot_family_tree(fam.root, graph=graph))

@app.callback(
    Output('output-rel-relationship', 'children'),
    [Input('rel-button', 'n_clicks')],
    [dash.dependencies.State('input-rel-node1', 'value'),
     dash.dependencies.State('input-rel-node2', 'value')]
)
def update_relationship_output(n_clicks, input_rel_node1, input_rel_node2):
    if n_clicks is None:
        raise PreventUpdate

    if input_rel_node1 and input_rel_node2:
        relationship = "Related" if fam.are_related(fam.find(Node(input_rel_node1)), fam.find(Node(input_rel_node2))) else "Not Related"
        return f"{input_rel_node1} and {input_rel_node2}: {relationship}"

    return None

@app.callback(
    [Output('output-add-node', 'children'),
     Output('family-tree-graph', 'figure', allow_duplicate=True)],
    [Input('add-node-button', 'n_clicks')],
    [dash.dependencies.State('input-parent', 'value'),
     dash.dependencies.State('input-new-node', 'value')]
)
def add_new_node(n_clicks, input_parent, input_new_node):
    if input_parent and input_new_node:
        parent_node = fam.find(Node(input_parent))
        if parent_node is None:
            parent_node = Node(input_parent)

        new_node = fam.find(Node(input_new_node))
        if new_node is None:
            new_node = Node(input_new_node)
        
        fam.add(parent_node, new_node)

        # Update the graph positions after adding the new node
        pos = plot_family_tree(fam.root, graph=graph)
        labels = {node: node.name for node in graph.nodes()}
        updated_figure = graph_to_plotly(graph, pos)
        return f"Node '{input_new_node}' added as a child of '{input_parent}'", updated_figure

    return None, graph_to_plotly(graph, plot_family_tree(fam.root, graph=graph))

@app.callback(
    Output('output-lca', 'children'),
    [Input('lca-button', 'n_clicks')],
    [dash.dependencies.State('input-node1', 'value'),
     dash.dependencies.State('input-node2', 'value')]
)
def update_lca_output(n_clicks, input_node1, input_node2):
    if input_node1 and input_node2:
        lca_result = fam.lca(fam.find(Node(input_node1)), fam.find(Node(input_node2)))
        return f"Lowest Common Ancestor of {input_node1} and {input_node2}: {lca_result}"

    return None

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