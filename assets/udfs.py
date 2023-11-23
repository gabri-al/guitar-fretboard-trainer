# User defined functions
from assets.custom_classes import Note, GuitarString

### Function to calculate all notes on the guitar plus the random questions options
def notesBuilder(tuning6, tuning5, tuning4, tuning3, tuning2, tuning1, strings_filter, frets_filter, accidentals_filter):
    myGuitar = {
        6: GuitarString(Note([tuning6], True if len(tuning6)>1 else False)),
        5: GuitarString(Note([tuning5], True if len(tuning5)>1 else False)),
        4: GuitarString(Note([tuning4], True if len(tuning4)>1 else False)),
        3: GuitarString(Note([tuning3], True if len(tuning3)>1 else False)),
        2: GuitarString(Note([tuning2], True if len(tuning2)>1 else False)),
        1: GuitarString(Note([tuning1], True if len(tuning1)>1 else False))}
    # Write to memory
    random_pos = []
    for s in range(1,7,1):
        for f in range(1,25,1):
            if s in strings_filter and f <= frets_filter:
                if ((myGuitar[s].getNote(f).isAccidental()) and (accidentals_filter is None)) or (not myGuitar[s].getNote(f).isAccidental()):
                    random_pos.append((s, f))
    #print(myGuitar[6].getNote(1).getValue())
    #print(random_pos) # List of tuples [(string, fret)] of random positions that can be asked
    return myGuitar, random_pos

### Function to determine the mode of the app
def calculateMode(play_clicks, stop_clicks, submit_clicks, next_clicks, store_data):
    """Define what is the app_mode (new question, new answer, stop, waiting) based on input data"""
    #print("Checking mode based on browser clicks: play:%3d, stop:%3d, submit:%3d, next:%3d" % (play_clicks, stop_clicks, submit_clicks, next_clicks))
    #print("Current memory data: %s" % store_data)
    # Save data to memory dict the first time
    if 'play_clicks' not in store_data.keys():
        store_data['play_clicks'] = play_clicks
    if 'stop_clicks' not in store_data.keys():
        store_data['stop_clicks'] = stop_clicks
    if 'submit_clicks' not in store_data.keys():
        store_data['submit_clicks'] = submit_clicks
    if 'next_clicks' not in store_data.keys():
        store_data['next_clicks'] = next_clicks
    # Calculate mode
    ## On startup
    if play_clicks == 0 and stop_clicks == 0 and submit_clicks == 0 and next_clicks == 0:
        store_data['play_clicks'] = play_clicks; store_data['stop_clicks'] = stop_clicks; store_data['submit_clicks'] = submit_clicks; store_data['next_clicks'] = next_clicks
        return store_data, 'first call'
    ## After initial clicks
    if stop_clicks > store_data['stop_clicks']:
        mode = 'stop'
    elif submit_clicks > store_data['submit_clicks']:
        mode = 'new answer'
    elif (play_clicks > store_data['play_clicks']) or (next_clicks > store_data['next_clicks']):
        mode = 'new question'
    else:
        mode = 'no update'
    store_data['play_clicks'] = play_clicks; store_data['stop_clicks'] = stop_clicks; store_data['submit_clicks'] = submit_clicks; store_data['next_clicks'] = next_clicks
    return store_data, mode
