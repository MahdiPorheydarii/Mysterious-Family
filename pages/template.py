from dash import html
import dash_bootstrap_components as dbc

navbar = dbc.Navbar(
    [
        dbc.NavbarBrand("Mysterious Family"),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Import Tree", href="/import_tree")),
                dbc.NavItem(dbc.NavLink("Info", href="/info")),
            ],
            className="ml-auto",
            navbar=True,
        ),
    ],
    color="primary",
    dark=True,
)

header = dbc.Card(
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
)