from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from .template import navbar, header
import base64

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
        html.Div(id='page-content')
    ])
    def parse_contents(contents, filename):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'txt' in filename:
                # Assume that the user uploaded a text file
                text_content = decoded.decode('utf-8')
                return html.Div([
                    html.H5(f'File Name: {filename}'),
                    html.Div(['Content: ', dcc.Markdown(text_content)])
                ])
            else:
                return html.Div(['Unsupported file format. Please upload a text file.'])
        except Exception as e:
            print(e)
            return html.Div(['There was an error processing this file.'])

    @app.callback(Output('output-data-upload', 'children'),
                  Input('upload-data', 'contents'),
                  Input('upload-data', 'filename'))
    def update_output(contents, filename):
        if contents is None:
            return 

        children = parse_contents(contents, filename)
        return children
