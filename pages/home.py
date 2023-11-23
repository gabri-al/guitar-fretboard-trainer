import dash
from dash import html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import random
import time
import numpy as np
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path='/', name='Home',
                   title='Guitar Notes Trainer',
                   description = 'Tool designed to help improve your knowledge of the guitar fretboard. Press play and guess notes on the guitar!',
                   image = '/assets/img/App_MetaImg.png')

############################################################################################
# Import other modules (functions, settings)
from assets.guitar import createGuitar, tuner
from assets.filters import _filters
from assets.udfs import calculateMode, notesBuilder

############################################################################################
# Page layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2(['Press Play and start Training!'])
        ], width=12)
    ]),
    dbc.Row(
        _filters
    ),
    dbc.Row([
        dbc.Col([
            tuner
        ], width = 1),
        dbc.Col(createGuitar(), id='guitarFretboard', width=11)
    ]),
    # Question
    dbc.Row([
        dbc.Col([], width = 3),
        dbc.Col([], id = 'questionCol', width = 6),
        dbc.Col([], id = 'questionCol-audio', width = 1),
        dbc.Col([], width = 2)
    ]),
    # Results
    dbc.Row([
        dbc.Col([], width = 3),
        dbc.Col(id = 'resultsCol', width = 6),
        dbc.Col([], width = 3)
    ]),
    # Next question
     dbc.Row([
        dbc.Col([], width = 3),
        dbc.Col([
            html.Button(html.I(className="fa-solid fa-forward-step"), id='next-button', n_clicks=0,
                                    title='Next question', className='my-button-next', hidden = True)
        ], id = 'nextCol', width = 6),
        dbc.Col([], width = 3)
    ]),   
    # Answer
    dbc.Row([
        dbc.Col([], width = 4),
        dbc.Col([
            dbc.Textarea(id = 'answer-input', placeholder="Type answer & click submit", className= "answer-input-area",
                        hidden = 'true', spellCheck = False)
        ], width = 3),
        dbc.Col([
            html.Button(html.I(className="fa-solid fa-share"), id='submit-button', n_clicks=0,
                            title='Submit answer', className='my-button-submit', hidden = True)
        ], width = 2),
        dbc.Col([], width = 3)
    ]),
])

############################################################################################
# Page Callback
@callback(Output('guitarFretboard', 'children'),
          Output('questionCol', 'children'),
          Output('answer-input', 'hidden'),
          Output('answer-input', 'value'),
          Output('submit-button', 'hidden'),
          Output('play-button', 'hidden'),
          Output('stop-button', 'hidden'),
          Output('resultsCol', 'children'),
          Output('next-button', 'hidden'),
          Output('questionCol-audio', 'children'),
          Output('browser-memo', 'data'),
          # Inputs from filters
          Input('tuner-string-6', 'value'),
          Input('tuner-string-5', 'value'),
          Input('tuner-string-4', 'value'),
          Input('tuner-string-3', 'value'),
          Input('tuner-string-2', 'value'),
          Input('tuner-string-1', 'value'),
          Input('audio-filter-checklist', 'value'),
          Input('strings-filter-checklist', 'value'),
          Input('frets-filter-dropdown', 'value'),
          Input('accidentals-filter-checklist', 'value'),
          # Inputs from buttons
          Input('play-button', 'n_clicks'),
          Input('stop-button', 'n_clicks'),
          Input('submit-button', 'n_clicks'),
          Input('answer-input', 'value'),
          Input('next-button', 'n_clicks'),
          State('browser-memo', 'data'))
def calculateAction(
        # Tuner inputs
        tuning6, tuning5, tuning4, tuning3, tuning2, tuning1,
        # Filter inputs
        audio, strings_filter, frets_filter, accidentals_filter,
        # Button inputs
        play_clicks, stop_clicks, submit_clicks, answer, next_clicks, store_data):
    # STEP 1 > Calculate guitar notes and random options
    myGuitar, random_positions = notesBuilder(tuning6, tuning5, tuning4, tuning3, tuning2, tuning1, strings_filter, frets_filter, accidentals_filter)
    # STEP 2 > Calculate app mode
    store_data, app_mode = calculateMode(play_clicks, stop_clicks, submit_clicks, next_clicks, store_data)
    #print("Detected mode: %s" % app_mode)
    #print("Updated memory data: %s" % store_data)
    # STEP 3 > React to the mode
    # ----------- FIRST INIT ----------- #
    if app_mode == 'first call':
        return createGuitar(), None, 'True', '', True, False, True, None, True, None, store_data
    # ----------- NEW QUESTION ----------- #
    elif app_mode == 'new question':
        # Add a wrong answer in case the answers count is lower than question count
        if ('questions' in store_data.keys()) and ('answers' in store_data.keys()):
            while len(store_data['questions']) > len(store_data['answers']):
                store_data['answers'].append(False)
        # Pick a question
        iRandom = random.randint(0, len(random_positions)-1)
        question = random_positions[iRandom]
        istring = int(question[0]); ifret = int(question[1])
        # Data for the guitarFretboard
        to_highlight = {istring: [(ifret, "?", "question")]}
        # Data for the question element
        question_component = html.Div(["What's the highlighted note (String: "+str(istring)+", Fret: "+str(ifret)+") ?"], className = 'questionDiv')
        # Save question to memory
        if 'questions' in store_data.keys():
            store_data['questions'].append(question)
        else:
            store_data['questions'] = [question]
        # Create audio component
        audio_ = None
        if 'Audio ON' in audio:
            right_answer = myGuitar[istring].getNote(ifret).getValue()[0]
            if len(right_answer) > 1:
                right_answer = right_answer[:1] + "_sharp"
            #print("Opening audio file: %s" % str("/assets/sounds/"+right_answer+".mp3"))
            audio_ = html.Audio(id = 'audio-note', disable_n_clicks = False, autoPlay = True, controls = False, loop = False,
                                src = '/assets/sounds/'+right_answer+'.mp3')
        # Save timestamp to memory
        store_data['question_start'] = time.time()
        return createGuitar(to_highlight, 24), question_component, None, '', False, True, False, None, True, audio_, store_data
    # ----------- NEW ANSWER ----------- #
    elif app_mode == 'new answer':
        # Save elapsed time to memory
        if 'question_start' in store_data.keys():
            if 'answers_elapsed' in store_data.keys():
                store_data['answers_elapsed'].append(time.time() - store_data['question_start'])
            else:
                store_data['answers_elapsed'] = [time.time() - store_data['question_start']]
        # Fix input answer
        answer = str(answer).replace(" ", "")
        if len(answer) > 1:
            answer = answer[:1].upper() + answer[1:2]
        # Check correctness
        question = store_data['questions'][-1]
        istring = int(question[0]); ifret = int(question[1])
        right_answer = myGuitar[istring].getNote(ifret).getValue()[0]
        answer_feedback = myGuitar[istring].guessNote(ifret, answer)
        if len(right_answer) > 1:
            right_answer = right_answer[:2]
        # Save result into memory
        if 'answers' in store_data.keys():
            store_data['answers'].append(answer_feedback)
        else:
            store_data['answers'] = [answer_feedback]
        # Calculate answer component
        answer_children = [
            dbc.Alert(children=[answer+' Correct!' if answer_feedback else answer+' Incorrect!'], 
                      color = 'success' if answer_feedback else 'danger')]
        # Update guitar component
        to_highlight = {istring: [(ifret, right_answer, 'answer-correct' if answer_feedback else 'answer-incorrect')]}
        #print("User answer %3s; Right answer %3s; Answer correct? %s" % (answer, right_answer, answer_feedback))
        #print(store_data)
        return createGuitar(to_highlight, 24), None, 'True', '', True, True, False, answer_children, False, None, store_data
    # ----------- STOP (Results review) ----------- #
    elif app_mode == 'stop':
        # Add a wrong answer in case the answers count is lower than question count
        if ('questions' in store_data.keys()) and ('answers' in store_data.keys()):
            while len(store_data['questions']) > len(store_data['answers']):
                store_data['answers'].append(False)
        # Main logic
        if 'answers' not in store_data.keys(): # In this case, Stop was clicked before submitting the first answer
            store_data['answers'] = []
            answer_children = [dbc.Alert('No answers given !!!', color = 'danger')]
            to_highlight = {}
        else: # In most cases there're answers, so everything goes under else
            # Calculate correct rate
            correct_answers = 0
            for a in store_data['answers']:
                if a is True:
                    correct_answers += 1
            # Calculate average answer time
            asa_ = None
            if 'answers_elapsed' in store_data.keys():
                asa_ = np.mean(store_data['answers_elapsed'])
                asa_ = np.around(asa_, decimals= 2)
                del store_data['answers_elapsed'] # clean memory
            # Update guitar component
            to_highlight = {}
            for i in range(0, len(store_data['questions']), 1):
                question = store_data['questions'][i]
                answer_feedback = store_data['answers'][i]
                istring = int(question[0]); ifret = int(question[1])
                right_answer = myGuitar[istring].getNote(ifret).getValue()[0]
                if len(right_answer) > 1:
                    right_answer = right_answer[:2]
                if istring in to_highlight:
                    to_highlight[istring].append((ifret, right_answer, 'answer-correct' if answer_feedback else 'answer-incorrect'))
                else:
                    to_highlight[istring] = [(ifret, right_answer, 'answer-correct' if answer_feedback else 'answer-incorrect')]
            # Calculate answer component
            alert_children = [str(correct_answers)+' / '+str(len(store_data['questions']))+' correct answers!']
            if asa_:
                alert_children.append(html.Br())
                alert_children.append("Average speed of answer: "+str(asa_)+"s")
            answer_children = [dbc.Alert(alert_children, color = 'warning')]
        # Clean memory data and return
        del store_data['questions']; del store_data['answers']
        return createGuitar(to_highlight, 24), None, 'True', '', True, False, True, answer_children, True, None, store_data
    # ----------- NO UPDATES ----------- #
    else:
        raise PreventUpdate