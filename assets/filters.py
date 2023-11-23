from dash import html, dcc
import dash_bootstrap_components as dbc

STRINGS_ITEMS = list(range(6,0,-1))
FRETS_ITEMS = list(range(1,25,1))

_filters = [
    dbc.Col([], width = 1),
    # Audio
    dbc.Col([
        dcc.Checklist(options = [{'label' : html.I(className="fa-solid fa-volume-high"), 'value' : 'Audio ON'}],
                      value = ['Audio ON'], inline = True, persistence=True, persistence_type='session', id = 'audio-filter-checklist')  
        ], width = 1, className = 'filterMessageCol'),
    # String filter
    dbc.Col([
        html.Div(["Select strings:"], className = 'filter-text'),
        dcc.Checklist(options = STRINGS_ITEMS, value = STRINGS_ITEMS, inline = True,
                        persistence=True, persistence_type='session', id = 'strings-filter-checklist')
        ], width = 4, className = 'filterMessageCol'),
    # Fret filter
    dbc.Col([
        html.Div(["Stop at fret:"], className = 'filter-text'),
        dcc.Dropdown(options=FRETS_ITEMS, value=24, searchable=False, placeholder=None, persistence=True, 
                                persistence_type='session', id='frets-filter-dropdown', multi=False, clearable=False)
    ], width = 3, className = 'filterMessageCol'),
    # Accidental filter
    dbc.Col([
        dcc.Checklist(options = ['Remove Accidentals (#/b)'], inline = True,
                      persistence=True, persistence_type='session', id = 'accidentals-filter-checklist')        
    ], width = 3, className = 'filterMessageCol')
]