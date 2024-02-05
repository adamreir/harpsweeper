# Main Code Elements. 

The source code for Harpsweeper defines Python functions and classes across several files. These elements are called from various files across the project. 
This file documents the main entry points defined in each file. 

## solver.py
Solver.py defines the class 'Solver' that wraps up the functions defined in solver_functions.py and write_sheets.py. 

To instanciate, type
```
class solver = Solver(tune, T, loop)
```
Where
 - 'tune' is a list[list[int]]. The index of 'tune' represents periods, and each element in 'tune' is a list of selected notes.
 - 'T' is an int: total number of periods
 - 'loop' is a bool: Indicates whether the 'Loop sequence' option is enabled. 

When instanciated, the solver imidiately generates a list of valid configurationsand stores these internally. 

'Solver' implements two methods that acts as main entrance points: 
 - solver.get_avail_notes() -> numpy array of shape [12]. Each element is either 0 or 1, indicating whether the corresponding note is available. The array indexes C at index 0, C#/Db at index 1, etc. 
 - solver.get_sheets(eng) -> str. Returns a string that can be written directly to a file.
   - 'eng' is of type bool, and indicates whether the output should be in English or Norwegian.

## solver_functions.py

Defines various functions used to find the list of available notes. These functions either calls each other, or are colled by 'solver.py'.

## make_sheets.py

Defines functions that takes a list of configurations, and returns a list of sheets. Called by solver.py.

## write_sheets.py

Defines functions used to transform the list of sheets into plain text. Called by solver.py

## layouts.py

Creates the screens of the main layout. These screens are displayed by calling the following functions: 
 - welcome_screen(tune_holder, solver_holder, texts, theme) -> str
 - about_screen(texts) -> str
 - main_screen(tune_holder, solver_holder, texts, theme) -> str
 - save_load_screen(tune_holder, solver_holder, texts) -> str

Where: 
 - 'tune_holder' is an instance of TuneHolder, defined in holders.py.
 - 'solver_holder' is an instance of SolverHolder, defined in holders.py.
 - 'texts' is an instance of Texts, defined in texts.py.
 - 'theme' is an instance of Theme, defined in theme.py.

The return value is in ['welcome', 'about', 'licence', 'main', 'save','exit'], which indicates which screen the user wants to go to. See main.py to see what these values do. 

