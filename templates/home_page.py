import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from .template import navbar, header
from libs.plot import plot_family_tree, graph_to_plotly
from dash.exceptions import PreventUpdate
from classes.Tree import Node
from .instance import fam, graph


pos = plot_family_tree(fam.root, graph=graph)
labels = {node: node.name for node in graph.nodes()}


home_layout = dbc.Container(
    fluid=True,
    children=[
        navbar,
        header,
        dcc.Graph(id='family-tree-graph', figure=graph_to_plotly(graph, pos),style={'width': '100%', 'height': '500px'}),
        html.Button('Fullscreen', id='fullscreen-btn', className="btn btn-secondary mb-2"),
        dbc.Row([
            dbc.Col(html.Label("Find the Farthest Child of a node:"), width=3),
            dbc.Col(
                dbc.Input(id='input-node', type='text', placeholder='Enter node name...', className="form-control-plaintext mb-2"),
                width=2
            ),
            dbc.Col(
                html.Button('Find Farthest Child', id='submit-button', className="btn btn-primary mb-2"),
                width=2
            ),
            dbc.Col(html.Div(id='output-farthest-child', className="text-info"), width=2),
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
            dbc.Col(html.Div(id='output-lca', className="text-info"), width=2),
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
                dbc.Input(id='input-parent', type='text', placeholder='Parent node', className="form-control-plaintext mb-2"),
                width=1
            ),
            dbc.Col(
                dbc.Input(id='input-new-node', type='text', placeholder='New node', className="form-control-plaintext mb-2"),
                width=1
            ),
            dbc.Col(
                html.Button('Add Node', id='add-node-button', className="btn btn-success mb-2"),
                width=2
            ),
            dbc.Col(html.Div(id='output-add-node', className="text-success"), width=2),
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
                dbc.Row([
            dbc.Col(
                html.Label("Size of the tree:"),
                width=3
            ),
            dbc.Col(
                html.Button('Get Size of the tree', id='size-button', className="btn btn-info mb-2"),
                width=2
            ),
            dbc.Col(html.Div(id='output-size', className="text-info"), width=2),
        ]),
    ]
)

def home_callbacks(app):
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
        html.Div(id='output-data-upload'),
    ])
    app.clientside_callback(
    """
    function(isFullScreen) {
        var graph = document.getElementById('family-tree-graph');
        if (isFullScreen) {
            if (graph.requestFullscreen) {
                graph.requestFullscreen();
            } else if (graph.mozRequestFullScreen) { // Firefox
                graph.mozRequestFullScreen();
            } else if (graph.webkitRequestFullscreen) { // Chrome, Safari and Opera
                graph.webkitRequestFullscreen();
            } else if (graph.msRequestFullscreen) { // IE/Edge
                graph.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.mozCancelFullScreen) { // Firefox
                document.mozCancelFullScreen();
            } else if (document.webkitExitFullscreen) { // Chrome, Safari and Opera
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) { // IE/Edge
                document.msExitFullscreen();
            }
        }
    }
    """,
    Output('family-tree-graph', 'fullscreen_mode'),
    Input('fullscreen-btn', 'n_clicks')
)

    @app.callback(
        Output('output-check-node', 'children'),
        [Input('check-node-button', 'n_clicks')],
        [State('input-check-node', 'value')]
    )
    def check_node_existence(n_clicks, input_check_node):
        if input_check_node:
            node_exists = fam.find(Node(input_check_node))
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
        [State('input-rel-node1', 'value'),
        State('input-rel-node2', 'value')]
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
        [State('input-parent', 'value'),
        State('input-new-node', 'value')]
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
    @app.callback(
        Output('output-size', 'children'),
        [Input('size-button', 'n_clicks')],
    )
    def update_size(n_clicks):
        if n_clicks:
            return f"Size of the Tree is : {fam.size}"