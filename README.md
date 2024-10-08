# Harpsweeper
This is the repocitory for Harpsweeper, a program for composing and organizing for the harp. Welcome!

This Github page contains a link to download Harpsweeper, the source code of Harpsweeper, and explanations of what Harpsweeper does. 

Harpsweeper aims to solve two problems. First, Harpsweeper simplifies the process of composing for the harp by automating the process of eliminating notes. Harpsweeper eliminates notes by removing notes that are not accessable through a sequence of pedal configurations. Second, Harpsweeper simplifies the process of organizing for and playing the harp by suggesting pedal configurations. 

In Harpsweeper, you enter a sequence of notes. Harpsweeper then finds all pedal sequences that can play the selected sequence of notes, and shows the user which notes can be added to the sequence. Lastly, Harpsweeper writes a text document with pedal configurations. 

Pedal configurations are subject to the following constraints: 
 - one foot can only change one pedal at any point in time.
 - strings cannot change pich while they are played.
 - strings cannot change pich while they ring.

## Download: 

You can download a free copy of Harpsweeper [here](https://www.dropbox.com/scl/fi/xp1fs40lh7kjn7fwa1m4a/Harpsweeper.exe?rlkey=l376cwyrrmde5t23czvv4ma5z&dl=0).

## Example: 

Example of working in Harpsweeper: 

<img src="https://raw.githubusercontent.com/adamreir/harpsweeper/main/example_images/harpsweeper_example.png" alt="drawing" width="700"/>

Generated "sheet music" based on the sequence above: 

<img src="https://raw.githubusercontent.com/adamreir/harpsweeper/main/example_images/example_sheets.png" alt="drawing" width="700"/>

Open Harpsweeper for a more detailed user guide. You can also read detailed documentations of the options [here](documentation/options_explained.md). 

## Options

Harpsweeper has a few options. These are described [here](https://github.com/adamreir/harpsweeper/blob/main/documentation/options_explained.md)

## Thanks

Harpsweeper was developed in cooperation with [Kristin Bolstad](https://www.kristinbolstad.com/)

## Source Files: 
 - Start Harpsweeper:
   - main.py -> Toggles between windows and keeps track of data available accross windows
 - Code used to find available notes: 
   - solver.py
   - solver_functions.py
 - Export sheet music:
   - get_sheets.py -> convert music and pedal configuration to text for exporting
 - Code used to generate the graphical user interface (GUI):
   - layouts.py -> defines each window of the GUI. 
   - theme.py -> defines and organizes the two themes.
   - texts.py -> stores the text used in the GUI and keeps track of the chosen language.
 - Classes used to store and pass solvers and sequences between windows:
   - holders.py
 - Self-explanatory additional files:
   - LICENSE
   - icon.ico

An overview of the main code objects can be found [here](documentation/main_code_objects.md). The source code contains detailed documentation of how to use the main code objects. 

## Compiling source files (i.e. make Harpsweeper.exe from code files):

To compile Harpsweeper, you need to
 - download the source files
 - install Python and required dependencies (see [requirements.txt](requirements.txt))
 - install pyinstaller
 - run the following in Command Promt (Windows):  
```
pyinstaller --onefile --windowed --clean --add-data 'LICENSE;.' --add-data 'icon.ico;.' --icon 'icon.ico' -n 'Harpsweeper'  main.py
```
