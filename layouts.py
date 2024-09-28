
#External libraries:
import PySimpleGUI as sg
#Import from harpsweeper files:
from solver import Solver
from convert_sheets_to_string import tune_as_string
#Python standard library:
import pickle
import copy
import traceback
import webbrowser
import sys
import os.path
from os import startfile

# Functions to make buttons, text, and input fields. Reduces the need to duplicate code.

def text(text):
    return sg.Text(text)


def button(button_text, key, **kwargs):
    return sg.Button(button_text=button_text, key=key, **kwargs)


def input(default_text, key):
    return sg.Input(default_text=default_text, key=key)


def filebrowse(button_text, file_types):
    return sg.FileBrowse(button_text=button_text, file_types=file_types)


def saveas(button_text, file_types):
    return sg.SaveAs(button_text=button_text, file_types=file_types)


# Function to get a list of ringing notes, i.e. notes that were played in the last period.
def get_ring_notes(T, active_notes, loop):
    print('getting ring notes')
    ring_notes = copy.deepcopy(active_notes)
    ring_notes = [a.split('_') for a in ring_notes]
    if loop:
        ring_notes = {f'{note}_{str((int(t) + 1) % T)}' for note, t in ring_notes}
    else:
        ring_notes = {f'{note}_{str((int(t) + 1) % T)}' for note, t in ring_notes if str(T - 1) != t}
    return ring_notes

#Function to get filename after compiling excel

def get_filename(filename):
    """Returns the absolute path for `filename'. The absolute path changes when Harpsweeper is compiled."""
    try:
        # Hack for pyInstaller. Refer https://stackoverflow.com/a/13790741
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, filename)

################
# Welcome page#
################1
def make_welcome_layout(theme,texts):
    welcome_page = [
        [text(texts.welcome)],
        [input(texts.default_input, key='-T-')],
        [button('Start', key='-start-'),
         sg.Input(visible=False, enable_events=True, key='-harp_file_load-'),
         filebrowse(button_text=texts.open, file_types=(('Sekvens', '.harps'),))],
        [sg.Checkbox('English', texts.eng, key='-eng-', enable_events=True),
         sg.Checkbox(texts.darkmode, theme.darkmode, key='-darkmode-', enable_events=True)],
        [button(texts.about_button, key='-about-')]
    ]

    welcome_layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
                      [sg.Text('', pad=(0, 0), key='-EXPAND2-'),  # the thing that expands from left
                       sg.Column(welcome_page, vertical_alignment='center', justification='center', k='-C-')]]
    return welcome_layout


def show_welcome_page(tune_holder, solver_holder, texts, theme):
    """Expects instances of TuneHolder, SolverHolder, Texts and Theme.

    Shows the Welcome page.

    Returns a string indicating which page the user wants to go to."""
    window = sg.Window(title="Harpsweeper",
                       layout=make_welcome_layout(theme=theme,texts=texts),
                       margins=(100, 50),
                       finalize=True,
                       icon=get_filename('icon.ico'),
                       return_keyboard_events=True,
                       resizable=True,
                       element_justification='c')
    window['-C-'].expand(True, True, True)
    window['-EXPAND-'].expand(True, True, True)
    window['-EXPAND2-'].expand(True, False, True)
    # window['-T-'].bind("<Return>", "_Enter")
    while True:
        event, values = window.read()
        print(f'Event: {repr(event)}, values:{values}')
        if isinstance(values, dict):
            if '-T-' in values:
                texts.default_input = values['-T-']

        QT_ENTER_KEY1 = 'special 16777220'
        QT_ENTER_KEY2 = 'special 16777221'

        if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2): #if event: enter key pressed:
            elem = window.FindElementWithFocus() #get the currently focused element.
            print(elem)
            print(elem.Type)
            print(elem.key)
            if elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON:  # if it's a button element, click it
                elem.Click()
            if elem is not None and elem.Type == sg.ELEM_TYPE_INPUT_TEXT:
                event = '-start-'
            if elem is not None and elem.Type == sg.ELEM_TYPE_INPUT_CHECKBOX:
                if elem.key == '-eng-':
                    event = '-eng-'
                    if isinstance(values, dict) and '-eng-' in values:
                        values['-eng-'] = not texts.eng
                if elem.key == '-darkmode-':
                    event = '-darkmode-'
                    if isinstance(values, dict) and '-darkmode-' in values:
                        values['-darkmode-'] = not theme.darkmode

        if event == '-about-':
            window.close()
            return 'about'

        if event == '-darkmode-':
            theme.darkmode = values['-darkmode-']
            theme.update_theme(sg)
            window.close()
            return 'welcome'

        if event == '-eng-':
            texts.eng = values['-eng-']
            window.close()
            return 'welcome'

        if event in ['-start-', '-T-_Enter']:
            ok = 1
            if values['-T-'] == '':
                ok = 0
                sg.popup(texts.select_periods, icon=get_filename('icon.ico'))
            for s in values['-T-']:
                if s not in ('0123456789'):
                    ok = 0
                    sg.popup(texts.only_numbers, icon=get_filename('icon.ico'))
            if ok == 1:
                T = int(values['-T-'])
                tune = [[12]] * T
                active_notes = set()
                ring_notes = set()
                avail_notes = {f'{n}_{t}' for t in range(T) for n in range(12)}
                loop = True
                tune_holder.setter(tune, active_notes, avail_notes, ring_notes, loop)
                window.close()
                return 'main'
        if event == '-harp_file_load-':
            filename = values['-harp_file_load-']
            try:
                with open(filename, 'rb') as f:
                    load_tune = pickle.load(f)
                try:
                    tune, active_notes, avail_notes, ring_notes, loop = load_tune.getter()
                except Exception: # Backwards compatibility with earlier versions of Harpsweeper.
                    tune = load_tune.tune
                    active_notes = load_tune.active_notes
                    avail_notes = load_tune.avail_notes
                    loop = True
                    ring_notes = get_ring_notes(len(tune), active_notes, loop)
                tune_holder.setter(tune, active_notes, avail_notes, ring_notes, loop)
                solver_holder.setter(Solver(tune=tune, loop=loop))
                window.close()
                return 'main'
            except Exception as e:
                sg.popup(texts.cannot_load + '\n\n' + str(e) + '\n\n' + str(traceback.format_exc()))
        if event == "Exit" or event == sg.WIN_CLOSED:
            return 'exit'


##############
# About page#
##############
def make_about_layout(texts):
    about_text = texts.about
    pad = ((4, 0), (4, 4))
    about_page = [
        [sg.Text(about_text[0] + '\n')],
        [
            sg.Text(about_text[1], pad=((4, 0), (4, 4))),
            sg.Text('adamreir@gmail.com', enable_events=True, font=('Helvetica', 10, 'underline'),
                    tooltip=texts.send_email, key='-email-', pad=((0, 0), (4, 4))),
            sg.Text(about_text[2], pad=((0, 4), (4, 4)))
        ],
        [
            sg.Text(about_text[3]),
            sg.Text('https://github.com/adamreir/harpsweeper.', enable_events=True, font=('Helvetica', 10, 'underline'),
                     key='-github-', pad=((0, 0), (4, 4))),
        ],
        [button(texts.back, key='-back-', pad=(4, 20)), button(texts.license_button, key='-license-', pad=(4, 20))]
    ]

    about_layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
                    [sg.Text('', pad=(0, 0), key='-EXPAND2-'),  # the thing that expands from left
                     sg.Column(about_page, vertical_alignment='center', justification='center', k='-C-')]]

    return about_layout


def show_about_page(texts):
    """Expects an instance of Texts.

    Shows the about page.

    Returns a string indicating which page the user wants to go to."""
    window = sg.Window(title="Harpsweeper",
                       layout=make_about_layout(texts),
                       margins=(100, 50),
                       icon=get_filename('icon.ico'),
                       resizable=True,
                       finalize=True,
                       element_justification='c')
    window['-C-'].expand(True, True, True)
    window['-EXPAND-'].expand(True, True, True)
    window['-EXPAND2-'].expand(True, False, True)

    while True:
        event, values = window.read()
        print(f'Event: {repr(event)}. Values: {values}')
        if event == '-back-':
            window.close()
            return 'welcome'
        if event == '-email-':
            webbrowser.open(url='mailto:?to=adamreir@gmail.com', new=1)
        if event == '-github-':
            webbrowser.open(url='https://github.com/adamreir/harpsweeper', new=1)
        if event == '-license-':
            window.close()
            return 'license'
        if event == "Exit" or event == sg.WIN_CLOSED:
            return 'exit'

################
#License page#
################
def make_license_layout(texts):
    pad = ((4, 0), (4, 4))
    license_page = [
        [sg.Text(texts.license(get_filename) + '\n')],
        [button(texts.back, key='-back-', pad=(4, 20))]
    ]

    license_layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
                    [sg.Text('', pad=(0, 0), key='-EXPAND2-'),  # the thing that expands from left
                     sg.Column(license_page, vertical_alignment='center', justification='center', k='-C-')]]

    return license_layout

def show_license_page(texts):
    window = sg.Window(title="Harpsweeper",
                       layout=make_license_layout(texts),
                       margins=(100, 50),
                       icon=get_filename('icon.ico'),
                       resizable=True,
                       finalize=True,
                       element_justification='c')
    window['-C-'].expand(True, True, True)
    window['-EXPAND-'].expand(True, True, True)
    window['-EXPAND2-'].expand(True, False, True)

    while True:
        event, values = window.read()
        print(f'Event: {repr(event)}. Values: {values}')
        if event == '-back-':
            window.close()
            return 'welcome'
        if event == "Exit" or event == sg.WIN_CLOSED:
            return 'exit'

##################
# Save/load page#
##################
def make_save_load_layout(texts):
    save_load_layout = [[sg.Column([  # Add an extra column to force horizontal separators to stay at the middle.
        [text(texts.harpsweeper_files)],

        [sg.Input(visible=False, enable_events=True, key="-harp_file_save-"),
         saveas(texts.save, file_types=(('Sekvens', '.harps'),)),
         sg.Input(visible=False, enable_events=True, key="-harp_file_load-"),
         filebrowse(texts.open, file_types=(('Sekvens', '.harps'),))],

        [sg.HorizontalSeparator()],
        [text(texts.export[0])],
        [sg.Input(visible=False, enable_events=True, key='-export-'),
         saveas(texts.export_button, file_types=(('Tekstfil', '.txt'),))],
        [text(texts.export[1])],
        [sg.HorizontalSeparator()],
        [button(texts.back, key='-back-'),
         button(texts.restart, key='-restart-')]
    ])]]

    save_load_layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
                        [sg.Text('', pad=(0, 0), key='-EXPAND2-'),  # the thing that expands from left
                         sg.Column(save_load_layout, vertical_alignment='center', justification='center', k='-C-')]]

    return save_load_layout


def show_save_load_page(tune_backup, keep_solver, texts):
    window = sg.Window(title="Harpsweeper",
                       layout=make_save_load_layout(texts),
                       margins=(100, 50),
                       icon=get_filename('icon.ico'),
                       resizable=True,
                       finalize=True,
                       element_justification='c')
    window['-C-'].expand(True, True, True)
    window['-EXPAND-'].expand(True, True, True)
    window['-EXPAND2-'].expand(True, False, True)

    while True:
        event, values = window.read()
        if event == '-back-':
            window.close()
            return 'main'
        if event == '-restart-':
            window.close()
            return 'welcome'
        if event == '-harp_file_save-':
            filename = values['-harp_file_save-']
            with open(filename, 'wb') as f:
                pickle.dump(tune_backup, f, protocol=pickle.HIGHEST_PROTOCOL)
            window.close()
            sg.popup(f'Sekvens lagret i \n {filename}')
            return 'main'
        if event == '-harp_file_load-':
            filename = values['-harp_file_load-']
            try:
                with open(filename, 'rb') as f:
                    load_tune = pickle.load(f)
                try:  # Backwards compatability. Remove this try-block at some point.
                    tune, active_notes, avail_notes, ring_notes, loop = load_tune.getter()
                except Exception:
                    tune = load_tune.tune
                    active_notes = load_tune.active_notes
                    avail_notes = load_tune.avail_notes
                    loop = True
                    ring_notes = get_ring_notes(len(tune), active_notes, loop)
                tune_backup.setter(tune, active_notes, avail_notes, ring_notes, loop)
                keep_solver.setter(Solver(tune=tune, loop=loop))
                window.close()
                return 'main'
            except Exception as e:
                sg.popup(texts.cannot_load)
        if event == '-export-':
            filename = values['-export-']
            sheets = keep_solver.sheets(texts.eng)
            if sheets == False:  # If no solver is generated, generate one before getting sheets
                tune, active_notes, avail_notes, ring_notes, loop = tune_backup.getter()
                solver = Solver(tune=tune, loop=loop)
                sheets = solver.get_sheets(texts.eng)
            with open(filename, 'w') as f:
                f.write(sheets)
            window.close()
            # sg.popup(f'Noter lagret i \n {filename}')
            startfile(filename)
            return 'main'

        if event == "Exit" or event == sg.WIN_CLOSED:
            return 'exit'


#############
# Note page#
#############

def make_note_buttons(notes, noteint, t, active_notes, avail_notes, ring_notes, theme):
    panel = [[sg.Text(str(t + 1) + ':')]]  # top row showing period
    m = 0
    for note in notes:
        note_str = f'{noteint[m]}_{t}'
        if note_str in active_notes:
            color = theme.notebutton_active
        elif note_str in ring_notes and note_str in avail_notes:
            color = theme.ring_color
        elif note_str in avail_notes:
            color = theme.notebutton_avail
        else:
            color = theme.notebutton_disable
        panel.append([sg.Button(note, key=f'note_{noteint[m]}_{t}', button_color=('#ffffff', color))])
        m += 1
    return panel


def make_main_layout(tune_holder, T, active_notes, avail_notes, ring_notes, theme, texts):
    pedal_order, notes, noteint = texts.ordered_notes
    print(noteint)

    # D, C, B | E, F, G, A

    note_panel = [[text('Pedal:')]]
    note_panel.extend(
        [[sg.Text(a, size=(5, 1), pad=6, justification='right')] for a in pedal_order])  # font=('Arial', 14)

    note_panel = [sg.Column(note_panel)]
    for t in range(T):
        note_panel.append(sg.Column(make_note_buttons(notes, noteint, t, active_notes, avail_notes, ring_notes, theme)))
        if t < T - 1:
            note_panel.append(sg.VSeparator())

    note_panel = [sg.Column([note_panel], scrollable=True, vertical_scroll_only=False, expand_y=True,
                            sbar_background_color=theme.sbar_background_color,
                            sbar_trough_color=theme.sbar_trough_color,
                            sbar_relief=sg.RELIEF_SOLID,
                            size_subsample_height=1)]

    main_page = [
        note_panel,
        [sg.Checkbox(texts.loop_checkmark_text, tune_holder.loop, key='-loop-', enable_events=True),
         sg.Checkbox(texts.darkmode, default=theme.darkmode, enable_events=True, key='-darkmode-')],
        [sg.Checkbox(texts.reverse_text, default=not texts.reverse, enable_events=True, key='-reverse-'),
         sg.Checkbox(texts.show_ring_colors, default=theme.show_ring_colors, enable_events=True, key='-show_ring_colors-')],
        [text(texts.bottom_note_checkmark_text),
         sg.Combo(texts.notes, default_value=texts.bottom_note_str, enable_events=True, readonly=False,
                  key='-bottom_note-')],
        [button(texts.save_or_load, key='-goto_save-'),
         button(texts.restart, key='-restart-')]
    ]

    main_layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
                   [sg.Text('', pad=(0, 0), key='-EXPAND2-'),  # the thing that expands from left
                    sg.Column(main_page, vertical_alignment='center', justification='center', k='-C-')]]

    return main_layout

def update_button_colors(window, active_notes, avail_notes, tune_backup, ring_notes, theme):
    T = len(tune_backup.tune)
    all_notes = {f'{n}_{t}' for t in range(T) for n in range(12)}
    for note in all_notes:
        if note in active_notes:
            window[f'note_{note}'].update(button_color=theme.notebutton_active)
        elif note in avail_notes and note in ring_notes:
            window[f'note_{note}'].update(button_color=theme.ring_color)
        elif note in avail_notes:
            window[f'note_{note}'].update(button_color=theme.notebutton_avail)
        else:
            window[f'note_{note}'].update(button_color=theme.notebutton_disable)


def show_main_page(tune_holder, keep_solver, texts, theme):
    T = len(tune_holder.tune)
    tune, active_notes, avail_notes, ring_notes, loop = tune_holder.getter()
    keep_solver.setter(Solver(tune=tune, loop=loop))
    avail_notes = keep_solver.getter().get_avail_notes()
    print(ring_notes)
    window = sg.Window(title="Harpsweeper",
                       layout=make_main_layout(tune_holder, T, active_notes, avail_notes, ring_notes, theme, texts),
                       margins=(100, 50),
                       icon=get_filename('icon.ico'),
                       resizable=True,
                       finalize=True,
                       element_justification='c')
    # Center align (horizontal and vertical) the content:
    window['-C-'].expand(True, True, True)
    window['-EXPAND-'].expand(True, True, True)
    window['-EXPAND2-'].expand(True, False, True)

    while True:
        change_loop = False
        tune_holder.setter(tune, active_notes, avail_notes, ring_notes, loop)
        event, values = window.read()
        print(f'event: {event}, values: {values}')

        if event == '-restart-':
            window.close()
            return 'welcome'
        if event == '-goto_save-':
            window.close()
            return 'save'

        if event == '-loop-':
            change_loop = True
            loop = values['-loop-']

        if event == '-show_ring_colors-':
            theme.show_ring_colors = not theme.show_ring_colors
            update_button_colors(window, active_notes, avail_notes, tune_holder, ring_notes, theme)
            #window.close()
            #return 'main'

        if event == '-bottom_note-':
            texts.lastnote = texts.note_to_noteint[values['-bottom_note-']]
            window.close()
            return 'main'

        if event == '-reverse-':
            # Set bottom note to current top note before changing reverse status:
            pedal_order, notes, noteint = texts.ordered_notes
            texts.lastnote = noteint[0]
            texts.reverse = not values['-reverse-']
            window.close()
            return 'main'

        if event == '-darkmode-':
            theme.darkmode = values['-darkmode-']
            theme.update_theme(sg)
            window.close()
            return 'main'

        # Update tune, and active notes:
        if event is not None and event[0:4] == 'note':
            note_period = event[5:len(event)]
            note = int(note_period[0:note_period.index('_')])
            period = int(note_period[note_period.index('_') + 1:len(note_period)])

            # change sets of active notes
            if note_period in active_notes:  # Remove note from active notes
                active_notes.remove(note_period)
                tune[period].remove(note)
                if len(tune[period]) == 0:
                    tune[period] = [12]
            elif note_period not in avail_notes:  # Error message if note note not in available notes
                sg.popup("Valgt note er ikke tilgjengelig.")
            else:  # Add to tune if note in set of available notes.
                active_notes.add(note_period)
                if tune[period] == [12]:
                    tune[period] = [note]
                else:
                    tune[period].append(note)

            # Color notes based on availability/usage
        if (event is not None and event[0:4] == 'note') or event == '-loop-':
            ring_notes = get_ring_notes(len(tune), active_notes, loop)
            try:
                # solver = Solver(tune, T)
                keep_solver.setter(Solver(tune=tune, loop=loop))
            except Exception as e:
                if change_loop:
                    sg.popup(texts.not_with_loop)
                    window['-loop-'].update(False)
                else:
                    sg.popup(
                        "Fant ingen måte å spille dette på.\nGår tilbake til før denne noten ble endret.\nError-log er skrevet til error.txt")
                with open("error.txt", mode="w") as f:
                    f.write("The program encountered an error.")
                    f.write('\n\nThe tune: ')
                    f.write(tune_as_string(tune))
                    f.write('\n\nThe error message:\n\n"')
                    f.write(str(e))
                    f.write('"')
                    f.write('\n\nThe traceback\n\n"')
                    f.write(str(traceback.format_exc()))
                    f.write('"')
                tune, active_notes, avail_notes, ring_notes, loop = tune_holder.getter()
                # keep_solver.setter(Solver(tune, T, loop))
                # solver = Solver(tune, T)
                keep_solver.setter(Solver(tune=tune, loop=loop))

            avail_notes = keep_solver.getter().get_avail_notes()
            update_button_colors(window, active_notes, avail_notes, tune_holder, ring_notes, theme)

        if event == "Exit" or event == sg.WIN_CLOSED:
            return 'exit'

