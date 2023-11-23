from dash import html
import dash_bootstrap_components as dbc

############################################################################################
# Import shared components

from assets.footer import _footer
from assets.nav import _nav

############################################################################################

_sidebar = html.Div([
    dbc.Row([
        dbc.Col([_nav], width = 12)
    ]),
    dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([
            html.Button(children = html.I(className="fa-solid fa-play"), id='play-button', n_clicks=0,
                        title='Play to guess random notes', className='my-button', hidden = False),
            html.Button(children = html.I(className="fa-solid fa-stop"), id='stop-button', n_clicks=0,
                        title='Stop & review results', className='my-button', hidden = True)
        ], className = 'button-col', width = 10),
        dbc.Col([], width = 1),
    ]),
    dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([html.Hr([], className = 'hr-footer')], width = 10),
        dbc.Col([], width = 1)
    ]),
    dbc.Row([
        dbc.Col([_footer], width = 12)
    ])
], className = 'sidebar-div')