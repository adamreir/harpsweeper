# How Harpsweeper Works

Harpsweeper's functionaliry can be organized into two distinct operations.  
 - Find notes that can be added to a sequence.
 - Write sheet music to a plain text file. 

This file documents each of these two operations in order, after a short note on the notation being used. 

### Notation: 
When Harpsweeper finds valid pedal-configuration, it has access to the total number of periods ($T$), and a list of the currently selected notes. 
Let $t=1,\dots,T$ be the index of time (/periods).  

In this document, I will occationaly write examples of pedal configurations and string plucs. Pedal configurations are a list that shows how the pedals are currently set, 
and string plucs shows which strings are being plucked. Both pedal configurations and string plucs are displayed as a list of 7 elements, corresponding to the seven 
pedals and corresponding strings on the harp. The order follows the common C, D, E, F, G, A, B order. 

The following pedal configuration, for example, shows a harp that have the E string set to Eb, and the rest of it's string set to the natural notes: 

[♮,♮,b,♮,♮,♮,♮]

The following pedal configuration and string plucs shows the harp in the same configuration as above, playing Eb on the E string: 

[♮,♮,b,♮,♮,♮,♮], [0,0,1,0,0,0,0]

## Operation 1: Find Notes That Can be Added to a Sequence

Every time the user adds or removes a note, Harpsweeper identifies available notes in two steps: 
 1. Finds all valid pedal configurations and corresponding string-plucks that plays the selected note-sequence. 
 2. For every note used: checks that there is a pedal configuration that can play this note.

### 1. Find Valid Pedal-Configurations

Finding valid pedal-configurations is done in two steps: 
1. Within period: Find pedal configurations and string plucs that plays the selected notes.
2. Across periods: Remove pedal configurations that are inconsistent with pedal configurations in the previous period ($t-1$). 

#### Within period

To identify valid pedal-configurations, Harpsweeper starts by doing the following for each period $t$: 
 - Generates a list of the $7^3=2,187$ pedal configuraitons available on the harp.
 - Removes any pedal-configuration that cannot play the selected notes.
 - For each pedal configuration, identify any string pluc that playes the selected notes.
 - Store a list of pedal configurations and corresponding string pluc. 

Consider an example: Let a note-sequence consist of a single period ($T=1$). In that period, the harp plays the note F. 
There are _many_ ways of doind this on the harp, so consider this pedal-configuration: 

[♮,♮,#,♮,♮,♮,♮]

There are two ways to play F on this configuration: on the E and F string. The results of the operation above is one list of pedal-configurations, and one list of corresponding 
string plucs: 

Pedal configurations:  | String plucs:  
:-------------------------:|:-------------------------:
...            | ...
[♮,♮,#,♮,♮,♮,♮] | [0,0,1,0,0,0,0]
[♮,♮,#,♮,♮,♮,♮] | [0,0,0,1,0,0,0]
...            | ...

Notice that the pedal configuration is duplicated. This is because it is associated with more than one valid string pluck. 

#### Across periods

Harpsweeper now knows which which pedal configurations and string plucs that plays the selected notes, within each period. It still does not knows which of the configurations are valid, however. This is because any of the pedal configurations can be unreachable from the last period, because it e.g. requires moving more than one pedals on either of the two feet. 

From here on, I will remove to a pedal configuraiton and a corresponding string plucs as a 'configuration'. 

Harpsweeper not looks at every configuration in period $t$, and checks every configuration in $t-1$, and ensures that there exists a configuration in $t-1$ that can be changed to the current configuraiton  
 - changing more than one pedal per foot.
 - changing a string that was played in period $t-1$
 - does not change any of the strings that will be played in period $t$.



## Write Sheet Music

When the user wants to export suggested sheet music, Harpsweeper does the following: 
1. Constructs a list of every valid sequence of pedal configuraitons that can play the note-sequence.
2. Calculates how many pedal changes are included in each of these pedal-sequences.
3. Writes the pedal sequences that involves the lowest number of pedal-changes to a plain text file.
