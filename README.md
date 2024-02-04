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

## Source Files: 
 - Code used to find available notes: 
   - solver.py
 - Code used to write sheet music:
   - write_sheet.py
 - Code used to generate the layout:
   - layouts.py -> defines each window of the GUI. 
   - theme.py -> Defines and organizes the two themes.
   - texts.py -> Stores the text used in the GUI. Keeps track of the chosen language.
 - The main loop: 
   - main.py



## Compiling Harpsweeper into an executable program

To compile Harpsweeper, you need to 

Download the source files, install pyinstaller, and run 
```
pyinstaller --onefile --windowed --clean --add-data 'LICENSE;.' --add-data 'icon.ico;.' --icon 'icon.ico' -n 'Harpsweeper'  main.py
```


## False Positive Virus Detection
Programs compiled with PyInstaller are frequently subject to false positive detection from anti virus programs. 

You can read more about this issue here: 

 - [https://github.com/pyinstaller/pyinstaller/blob/develop/.github/ISSUE_TEMPLATE/antivirus.md](https://github.com/pyinstaller/pyinstaller/blob/develop/.github/ISSUE_TEMPLATE/antivirus.md)

And a solution here: 
 - [https://pyinstaller.org/en/stable/bootloader-building.html](https://pyinstaller.org/en/stable/bootloader-building.html)
