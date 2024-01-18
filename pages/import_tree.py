from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from .template import navbar, header
from dash.exceptions import PreventUpdate
import base64
from .instance import fam, graph

import_tree_layout = dbc.Container(
    fluid=True,
    children=[
        navbar,
        header,
        dcc.Upload(
            id='upload-data',
            children=dbc.Card(
                [
                    dbc.CardHeader("Upload"),
                    dbc.CardBody(
                        [
                            html.Div(
                                ['Drag and Drop or ', html.A('Select a txt File')],
                                style={'text-align': "center"},
                                className="d-flex align-items-center justify-content-center h-100"
                            ),
                        ]
                    ),
                ],
                className="border-light mb-3 mx-auto",
                style={"max-width": "30%", 'height': "250px", 'text-align': "center"},
            ),
        ),
        html.Div(id='output-data-upload')
    ]
)

def import_tree_callbacks(app):
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
        html.Div(id='output-data-upload'),
    ])

    def parse_contents(contents, filename):
        global fam, graph

        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'txt' in filename:
                text_content = decoded.decode('utf-8')
                text_content = text_content.split('\n')

                text_content = [i.strip() for i in text_content]
                
                graph.clear()
                fam.import_tree(text_content[0], text_content[1:])

                return html.Div([
                    html.H5(f'{filename} successfully imported'),
                    html.Div(['You can now check out the tree in the home page'])
                ])

            else:
                return html.Div(['Unsupported file format. Please upload a text file.'])
        except Exception as e:
            print(e)
            return html.Div(['There was an error processing this file.'])
    @app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename'),
    )
    def update_output(contents, filename):
        if contents is None:
            raise PreventUpdate

        children = parse_contents(contents, filename)

        return children