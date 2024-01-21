from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from .template import navbar, header

info_layout = dbc.Container(
    fluid=True,
    children=[
        navbar,
        header,
        dbc.Card(
        [
            dbc.CardHeader("Contact"),
            dbc.CardBody(
                [
                    html.H4("Do we even need this?", className="card-title", style={'color':'yellow'}),
                    html.P("yet to be determined.", className="card-text"),

                ]
            ),
        ],
        className="border-light mb-3",
        style={"max-width": "100%", 'height': "520px",},
      )
    ]
)

def info_callbacks(app):
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])
