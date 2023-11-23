from dash import html
import dash_bootstrap_components as dbc
import dash

_nav_dropdown = dbc.DropdownMenu(
    children = [dbc.DropdownMenuItem(page["name"], href=page["path"]) for page in dash.page_registry.values()],
    menu_variant="dark", nav=True, align_end=False, size="sm", label="Menu"
    )

_nav = dbc.Container([
	dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([html.Img(disable_n_clicks = True, src = 'assets/img/Guitar_001.png', height = '180em')],
                width = 10, className = 'nav-col-img'),
        dbc.Col([], width = 1)
    ]),
    dbc.Row([
        dbc.Col([], width = 4),
        dbc.Col([_nav_dropdown], width = 4),
        dbc.Col([], width = 4),
    ], className="nav-row")
])