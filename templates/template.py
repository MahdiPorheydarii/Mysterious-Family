from dash import html
import dash_bootstrap_components as dbc

github_link = html.A(
    html.Img(src='https://icons.getbootstrap.com/assets/icons/github.svg', style={'height': '25px', 'width': '25px',}),
    href='https://github.com/MahdiPorheydarii/Mysterious-Family',
)

navbar = dbc.Navbar(
    [
        dbc.NavbarBrand("Mysterious Family", style={'margin-left': '13px'}),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Import Tree", href="/import_tree")),
                dbc.NavItem(dbc.NavLink("Info", href="/info")),
                dbc.NavItem(github_link),
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