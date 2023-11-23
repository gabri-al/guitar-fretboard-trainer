from dash import html, dcc

## Create tuning dropdowns for each string
NOTES_DROPDOWN = ["A", "A#", "Bb", "B", "C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab"]

tuner = (
    html.Div(className = 'fret-column-extra-small', children = [
        dcc.Dropdown(options=NOTES_DROPDOWN, value='E', searchable=False, placeholder=None, persistence=True, 
                         persistence_type='session', id='tuner-string-6', multi=False, clearable=False),
        html.Div(className = 'tuner-vertical-space'),
        dcc.Dropdown(options=NOTES_DROPDOWN, value='A', searchable=False, placeholder=None, persistence=True, 
                         persistence_type='session', id='tuner-string-5', multi=False, clearable=False),
        html.Div(className = 'tuner-vertical-space'),
        dcc.Dropdown(options=NOTES_DROPDOWN, value='D', searchable=False, placeholder=None, persistence=True, 
                         persistence_type='session', id='tuner-string-4', multi=False, clearable=False),
        html.Div(className = 'tuner-vertical-space'),
        dcc.Dropdown(options=NOTES_DROPDOWN, value='G', searchable=False, placeholder=None, persistence=True, 
                         persistence_type='session', id='tuner-string-3', multi=False, clearable=False),
        html.Div(className = 'tuner-vertical-space'),
        dcc.Dropdown(options=NOTES_DROPDOWN, value='B', searchable=False, placeholder=None, persistence=True, 
                         persistence_type='session', id='tuner-string-2', multi=False, clearable=False),
        html.Div(className = 'tuner-vertical-space'),
        dcc.Dropdown(options=NOTES_DROPDOWN, value='E', searchable=False, placeholder=None, persistence=True, 
                         persistence_type='session', id='tuner-string-1', multi=False, clearable=False)
    ])
)

## Function that builds the Guitar layout (this is also used by callbacks)
def fretCreatorhelper(fret_i, highlight):
    '''This helper function create all elements that goes into a fret column'''
    dottedFrets = [3,5,7,9,15,17,19,21]
    dottedFretsDouble = [12,24]
    fret_col_children = []
    # Calculate dot in mid fret
    if fret_i in dottedFrets:
        midFretElement = 'fret-element-dotted'
    else:
        midFretElement = 'fret-element'
    # Calculate double dot frets
    if fret_i in dottedFretsDouble:
        doubleDotElement = 'fret-element-dotted'
    else:
        doubleDotElement = 'fret-element'
    # Build each string and update it if there's a note to be highlighted        
    for s in range(6, 0, -1):
        new_string = html.Div(className = 'string'+str(s), children = [
            html.Div(className='note-element', id='string6-fret'+str(fret_i))])
        if s in highlight.keys():
            highlight_at_string = highlight[s]
            for j in range(len(highlight_at_string)):
                highlight_info = highlight_at_string[j]
                if highlight_info[0] == fret_i:
                    new_string = html.Div(className = 'string'+str(s), children = [
                        html.Div(str(highlight_info[1]), className='note-element-'+str(highlight_info[2]), id='string6-fret'+str(fret_i))])
        fret_col_children.append(new_string)
        # Add fret element below string when needed
        if s == 5 or s == 3:
            fret_col_children.append(html.Div(className = doubleDotElement))
        elif s == 4:
            fret_col_children.append(html.Div(className = midFretElement))
        elif s == 6 or s == 2:
            fret_col_children.append(html.Div(className = 'fret-element'))
        else:
            pass # if e-string don't attach anywhing below
    return fret_col_children

def createGuitar(highlight = {}, nFrets = 24):
    '''Create frets elements, strings on the neck plus headers. Optionally, it highlights notes with or without answer.
    Highlight is a dictionary with keys = strings and values = list of touples [(fret, note_value, class of note element), ()]'''
    GuitarFretsList = []
    FretsHeader = []
    for i in range(1, nFrets+1, 1):
        # Calculate fret column width
        if i < 8:
            fretSize = 'big'
        elif i >= 8 and i < 14:
            fretSize = 'medium'
        else:
            fretSize = 'small'
        # Build fret column and call helper to build sub-elements
        newFret = (
            html.Div(className = 'fret-column-'+fretSize, children = fretCreatorhelper(i, highlight))
        )
        # Build fret headers
        newFretHeader = (
            html.Div(className = 'fret-column-'+fretSize, children = [
                html.Div(className = 'fret-header', children = ["fr-"+str(i)])
            ])
        )
        GuitarFretsList.append(newFret)
        FretsHeader.append(newFretHeader)

    return [html.Div(className = 'GuitarFretHeaders', children = FretsHeader),
            html.Div(className = 'GuitarNeck', children = GuitarFretsList)]