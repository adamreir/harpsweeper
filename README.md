# Harpsweeper
This is the repocitory for Harpsweeper, a program for composing and organizing for harps. 

Harpsweeper lets you generate a sequency of notes, and shows which notes can be added to the sequence, given that there exists a sequence of pedal configurations that can play the sequence. Pedal configurations are subject to the following constraints: 
 - only one pedal per foot change single period.
 - strings cannot change pich wile they are played.
 - strings cannot change pich right after they are played. 

## Download: 

You can download a free copy of Harpsweeper [here](https://www.dropbox.com/scl/fi/xp1fs40lh7kjn7fwa1m4a/Harpsweeper.exe?rlkey=l376cwyrrmde5t23czvv4ma5z&dl=0).

## Example: 

Example of working in Harpsweeper: 

<img src="https://raw.githubusercontent.com/adamreir/harpsweeper/main/example_images/harpsweeper_example.png" alt="drawing" width="700"/>

Generated sheet music based on the sequence above: 

<img src="https://raw.githubusercontent.com/adamreir/harpsweeper/main/example_images/example_sheets.png" alt="drawing" width="700"/>

Open Harpsweeper for a more detailed user guide. You can also read detailed documentations of the options [here](documentation/options_explained.md). 

## Source Files: 
 - Code used to find available notes: 
   - solver.py
 - Code used to write sheet music:
   - write_sheet.py
 - Code used to generate the graphical user interface (GUI):
   - layouts.py -> defines each window of the GUI. 
   - theme.py -> defines and organizes the two themes.
   - texts.py -> stores the text used in the GUI and keeps track of the chosen language.
 - Classes used to store and pass solvers and sequences between windows:
   - holders.py
 - The main loop: 
   - main.py
 - Self-explanatory additional files:
   - LICENSE
   - icon.ico

An overview of the main code objects can be found [here](documentation/main_code_objects.md). The source code contains detailed documentation of how to use the main code objects. 

## Compiling source files into an executable program:

To compile Harpsweeper, you need to:
 - Download the source files
 - Install Python and required dependencies (see [requirements.txt](requirements.txt))
 - Install pyinstaller
 - Run the following in Command Promt (Windows):  
```
pyinstaller --onefile --windowed --clean --add-data 'LICENSE;.' --add-data 'icon.ico;.' --icon 'icon.ico' -n 'Harpsweeper'  main.py
```
