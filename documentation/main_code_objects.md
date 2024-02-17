# Main Code objects. 

Harpsweeper is a self contained program with a graphical user interface. However, the various functions and classes defined used in Harpsweeper can be used as stand alone objects in other contexts. This file documents the main entry points. See docstrings in the source code for a more detailed documentation of how to use each object. 

## main.py

Contains the main execution loop. `main.py` relies (recursively) on every other file in Harpsweeper.    

## solver.py

Defines the `Solver` class. `Solver` takes a sequence of notes and finds every note that can be added to the sequence. Optionally, `Solver` can require the notes to be played in a loop, which may reduce the number of available notes. Lastly, Solver can produce sheet music, which shows how the selected notes can be played on the harp. 

Main methods:
 - `get_avail_notes(self) -> list[str]`: 
    - Returns a list of available notes.
 - `get_sheets(self, eng : bool) -> str`:
    - Returns sheet music formated as a string. Can be written directly to a file.

`Solver` calls functions defined in `solver_functions.py`, `make_sheets.py`, and `convert_sheets_to_string.py`. 

## layouts.py

Defines and displayes each screen of the GUI. These screens are displayed by calling the following functions: 
 - `show_welcome_screen(tune_holder, solver_holder, texts, theme) -> str`
 - `show_about_screen(texts) -> str`
 - `show_licence_screen(texts) -> str`
 - `show_main_screen(tune_holder, solver_holder, texts, theme) -> str`
 - `show_save_load_screen(tune_holder, solver_holder, texts) -> str`

Each function expects instances of `TuneHolder`, `SolverHolder`, `Texts`, and `Theme`  defined in `holders.py`, `texts.py`, and `theme.py`. 

`layouts.py` relies on `write_sheets.py` and `solver.py`. 

The return value of each function indicates where the user wants to go. 

## texts.py

Defines the `Texts` class. `Texts` holds all of the text displayed in the GUI, returned by calling various methods. The attribute 'eng' (bool) determine if the texts returned by these methods are in English or Norwegian. 

## theme.py

Defines the `Theme` class. `Theme` organizes the two themes available in Harpsweeper. Additionally, `Theme` keeps track of the state of the option that determines if Harpsweeper shows a separate color for ringing notes. 






