# Harpsweeper
This is the repocitory for Harpsweeper, a program for composing and organizing for harps. 

This program aids composing and organizing sequences of notes for the harp.

Harpsweeper lets you generate a sequency of notes. It then shows the notes that can be added, given that
 - there exists a sequence of pedal configurations that can play the sequence.
 - only one pedal per foot can change in a single period.
 - pedals do not change at the same time or right after the corresponding string is played.

## Examples of usage: 

Example of working in Harpsweeper: 

<img src="https://raw.githubusercontent.com/adamreir/harpsweeper/main/harpsweeper_example.png" alt="drawing" width="700"/>

Generated sheet music based on the sequence above: 

<img src="https://raw.githubusercontent.com/adamreir/harpsweeper/main/example_sheets.png" alt="drawing" width="700"/>

Open Harpsweeper for a more detailed user guide. 

## Download: 

You can download a copy of Harpsweeper from Dropbox [here](https://www.dropbox.com/scl/fo/b9piezza5x2jjrh2e3miv/h?rlkey=rs0rz4ggzmhqkvangq15cyj6c&dl=0).

## Source Files: 
 - Code used to find available notes: 
   - solver.py
 - Code used to write sheet music:
   - write_sheet.py
 - Code used to generate the graphical user interface (GUI):
   - layouts.py -> defines each window of the GUI. 
   - theme.py -> Defines and organizes the two themes.
   - texts.py -> Stores the text used in the GUI and keeps track of the chosen language.
 - The main loop: 
   - main.py
 - Self-explanatory additional files:
   - LICENSE
   - icon.ico

## Compiling Harpsweeper into an executable program:

To compile Harpsweeper, you need to:
 - Download the source files
 - Install pyinstaller
 - Run the following in Command Promt (Windows):  
```
pyinstaller --onefile --windowed --clean --add-data 'LICENSE;.' --add-data 'icon.ico;.' --icon 'icon.ico' -n 'Harpsweeper'  main.py
```
