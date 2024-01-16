import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from pages.home_page import home_layout, home_callbacks
# from import_tree_page import import_tree_layout, import_tree_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR], suppress_callback_exceptions=True)
app.config.prevent_initial_callbacks = 'initial_duplicate'



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

home_callbacks(app)
# import_tree_callbacks(app)

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/import_tree':
        # return import_tree_layout
        pass
    elif pathname == '/':
        return home_layout
    else:
        return html.Div(f'404 - Page not found for {pathname}')

if __name__ == '__main__':
    app.run_server(debug=True)