# Main Code objects. 

The source code for Harpsweeper defines Python functions and classes across several files. These elements are called from various files across the project. 
This file documents the main entry points defined in each file. 

## solver.py
Solver.py defines the class 'Solver' that wraps up the functions defined in solver_functions.py and write_sheets.py. 

```
class Solver:
    """Class used to get a list of available notes and write sheet music.

        Instanciate:
        ------------
        solver = Solver(tune: list[list[int]], T: int, loop: bool)
            tune : list[list[int]]
                The selected notes. The index of each sublist corresponds to a period, 
                and contains notes formatted as integer (0=C, 1=C# etc.).
                E.g. walking up the C-major scale: [[0], [2], [4], [5], [7], [9], [11]].
    
            T : int
                The total number of periods.
    
            loop : bool
                Indicates whether the 'Loop sequence' option is enabled.


        Attributes:
        -----------
        tune : list[list[int]]
            Internal copy of the tune.
        T : int
            Internal copy of the number of periods.
        loop : bool
            Internal copy of the 'loop sequence' option indicator.

        conf_lists : list[np.array]
            A list of arrays. An array at list index t contains a list of valid pedal configurations in period t.
        ring_lists : list[np.array]
            A list of arrays. An array at list index t contains a list of string rings in period t.
        *Note that each pedal configuration corresponds to a string ring at the same index.
        *i.e. ring_list[t][n] corresponds to conf_list[t][n]

        Methods:
        --------
        solve(self) -> None:
            fills 'conf_lists' and 'ring_lists' with valid pedal configurations and corresponding string rings .
            Called by __init__
        get_avail_notes(self) -> list[str]:
            Returns a list of available notes. Each note is a string, formatted as 'note_period', where 
            'note' is a number between 0 and 12, and 'period' is the time period.
        get_sheets(self, eng : bool) -> str:
            eng : bool 
                Indicates usage of English rather than Norwegian
            -> str: 
                A string that contains sheet music which can be written to a file. 
    """
 ```

`Solver` implements two methods that acts as main entrance points: 
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

The return value of the function is a str in ['welcome', 'about', 'licence', 'main', 'save','exit'], which indicates where the user wants to go. 

## texts.py

Defines the Texts class. This class hols all of the text displayed in the GUI, returned by calling various methods. The attribute 'eng' (bool) determine if the texts returned by these methods are in English or Norwegian. 

To instanciate, type
```
theme = Theme(sg)
```
Where 
 - 'sg' 





