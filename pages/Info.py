import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Info', title='Guitar Notes Trainer | Info')

############################################################################################
# Page layout

layout = dbc.Container([
    dbc.Row([
        dbc.Col([], width=1),
        dbc.Col([
            html.H2(["What's this app about?"])
        ], width=11)
    ]),
    # First part
    dbc.Row([
        dbc.Col([], width=1),
        dbc.Col([
            html.H4(['Welcome!!! Thank you for landing here'])
        ], width=11)
    ]),
    dbc.Row([
        dbc.Col([], width = 2),
        dbc.Col([
            html.P(["This tool is designed to help improve your knowledge of the guitar fretboard."]),
            html.P(["On the home page, you can see some filters at the top and a guitar fretboard."]),
            html.P(["Once you press play, some notes will get highlighted on the guitar fretboard and you'll need to guess the right note using the interactive area that will show up at the bottom."])
            ], className = 'info-col', width = 9),
        dbc.Col([], width = 1)
    ]),
    # Second part
    dbc.Row([
        dbc.Col([], width=1),
        dbc.Col([
            html.H4(['To use the app:'])
        ], width=11)
    ]),
    dbc.Row([
        dbc.Col([], width = 2),
        dbc.Col([
            html.P(["1) Set up some filters:",
                    html.Br(),
                    "you can turn audio on/off, select the strings you want to practice on, limit the fretboard (e.g. up to the 12th fret), and choose to remove accidental notes (sharps '#' or flats 'b')."
                    ]),
            html.P(["2) Tune the guitar:",
                    html.Br(),
                    "select the open note on each string using the dropdowns (the standard tuning is set by default)."]),
            html.P(["3) Press play: the app randomly asks for notes on the guitar fretboard.",
                    html.Br(),
                    "An audio is played: each audio segment contains the note, played in three different positions on the guitar.",
                    html.Br(),
                    "Type your answer and click on submit. A correct/incorrect message will be displayed.",
                    html.Br(),
                    "Click on the next button to advance to a new question."]),
            html.P(["4) Press stop to finish, when the app is in play mode.",
                    html.Br(),
                    "You can review all your questions and the score."])
            ], className = 'info-col', width = 9),
        dbc.Col([], width = 1)
    ]),
    dbc.Row([
        dbc.Col([], width=1),
        dbc.Col([
            html.H4(['Have fun and reach out in case of issues/questions'])
        ], width=11)
    ]),
    dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([
            html.Ul([
                html.Li([
                    html.A([ html.I(className="fa-brands fa-github me-3 fa-1x")], href='https://github.com/gabri-al'),
                    html.A([ html.I(className="fa-brands fa-linkedin me-3 fa-1x")], href='https://www.linkedin.com/in/gabriele-albini-85100549/'),
                    html.A([ html.I(className="fa-brands fa-medium me-3 fa-1x")], href='https://medium.com/@gabri-albini')
                ])
            ], className='list-unstyled d-flex justify-content-center justify-content-md-start')
        ], width = 4),
        dbc.Col([], width = 7),
    ])
])
