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

Harpsweeper now takes a configuration in period $t$, checks every configuration in $t-1$, and remove the configuration in $t$ unless there exists a configuration in $t-1$ that can be changed to the current configuraiton without  
 - changing more than one pedal per foot.
 - changing a string that was played in period $t-1$
 - changing any of the strings that will be played in period $t$.

Consider another example, with two periods. For simplicity, there is only one configuration in period $t-1$, and three configuration in period $t$: 

<table>  <thead>  
 <tr> <th colspan=2> $t-1$ </th> <th colspan=3> $t$ </th></tr>
 <tr> 
   <td> [♮,♮,#,#,♮,♮,♮] </td><td> [0,0,0,0,1,0,0] </td><td> [♮,♮,#,#,#,♮,♮]</td> <td>[0,0,1,0,0,0,0] </td> <td> &#10060; </td>
 </tr>
 <tr> 
   <td>                </td><td>                 </td><td> [♮,♮,#,♮,♮,♮,♮]</td> <td>[0,0,0,1,0,0,0] </td> <td> &#10060;</td>
 </tr>
  <tr> 
   <td>                </td><td>                 </td><td> [♮,♮,#,#,♮,♮,♮]</td> <td>[0,0,1,0,0,0,0] </td> <td> &#x2714; </td>
 </tr>
</tbody>  
</table> 

Explanation: 
 - The first configuration in period $t$ is invalid, because it tries to change the G string. The G string, however, is still ringing from the last period.
 - The second configuration is also invalid. Because there are no configurations ion $t-1€ with the F string in the same configuration, the F string has to change and play at the same time.
 - The third configuration does not violate any of the restrictions, and is valid. 

Harpsweeper does this for every configuration in every period. 

This is where the 'Loop sequence' option changes the algorithm: 
 - Enabled: Harpsweeper takes configuration in period $1$, and looks through every configuration in period $T$ using the method above.
 - Disabled: Harpsweeper skips this step for the first period.

Note that if the 'Loop sequence' option is enabled, a single pass through the periods might not be enought: It starts at period $1$, looking at every configurations in $T$. When it is done, however, it might have removed configurations from period $T$, requirering more configurations to be removed from period $1$. If the option is enabled, it loops through the periods at least two times, always checking if the last pass removed any additional configurations. When no configurations have changed during the last pass, it is odone. 

### 1. Find Available Notes From the Lists of Valid Configurations
Harpsweeper now have a list of every valid configuration. It now checks that unused note $C$ (used as an example) are available in period $t$ by doing the following:  
 - For each configurations in period $t$ checks that either the $C$ or $B$ string are tuned to $C$
   - If it is, looks for a configuration it can follow in period $t-1$, and whether $C$ is available on any of the strings not being changed.
     - If it is, checks for a configuration in $t+1$ that can follow the current configuration, and that does not change the string that is being used to play $C$ in period $t$.
 - If all of the above is true, then C is available in period $t$. 

## Write Sheet Music

When the user wants to export suggested sheet music, Harpsweeper does the following: 
1. Constructs a list of every valid sequence of configuraitons that can play the note-sequence.
2. Calculates how many pedal changes are included in each of these sequences.
3. Writes the pedal sequences that involves the lowest number of pedal-changes to a plain text file.

Step 2. and 3. are trivial to compute.

For simplicity I will call a sequence of configurations for a "sheet" from now on. 

Step 1. is done by first copying the list of valid configurations in period $t=1$. This is already a list of sheets that stops in period $1$. The rest of the process is done itteratively, by generating a list of sheets that stops at period $t$ from the existing list of sheets that stops in period $t-1$ and the list of configurations in period $t$. This is done in the following way: 
 - Generate an empty list of sheets that stops in period $t$. 
 - For each sheet that stops in period $t-1$, look for a configuration in $t$ that can be added (using the same restrictions that was checked above).
   - Every time it finds such a configurations, make a new sheet that stop in period $t$ by appending the identified configuration to the current sheet, and add this to the list of configurations that stops in period $t$.

After going through every period, it has a list of sheets that can play the selected notes. Note that if the 'Loop sequence' option is enabled, it also needs to remove any sheet music that ends with a configuration that cannot be followed by the first configuration. 

To see how this works, consider a simple example with two periods. Period $1$ only have a single pedal configuration for simplicity. We start by considering the list of available configurations we allready have. 

<table>  <thead>  
 <tr> <th colspan=4> Lists of valid configurations  </th> </tr>
 <tr> <th colspan=2> $t=1$ </th> <th colspan=2> $t=2$ </th></tr>
 <tr> 
   <td> [♮,♮,#,#,♮,♮,♮] </td><td> [0,0,0,0,1,0,0] </td><td> [♮,♮,#,#,♮,♮,♮]</td> <td>[0,0,1,0,0,0,0] </td>
 </tr>
 <tr> 
   <td>                </td><td>                </td><td> [♮,♮,#,#,♮,♮,#]</td> <td>[0,0,1,0,0,0,0] </td>
 </tr>
</tbody>  
</table> 

In the first step, we simply copy the configuration(s) in period $1$. We now have a list of sheets that stop in period $1$ (consisting of a single sheet): 

<table>  <thead>  
 <tr> <th colspan=2> Sheets that stop in period $1$ </th> </tr>
 <tr> <th colspan=2> $t=1$ </th> 
 <tr> 
   <td> [♮,♮,#,#,♮,♮,♮] </td><td> [0,0,0,0,1,0,0] </td>
 </tr>
</tbody>  
</table> 

In the itterative step, we take each sheet in the current list of sheets, look through the configurations in period $2$, and checks if that that configuration can follow the current sheet. Because they can both follow, our new list of sheets have two elements: 


<table>  <thead>  
 <tr> <th colspan=4> Sheets that stop in period $2$ </th> </tr>
 <tr> <th colspan=2> $t=1$  <th colspan=2> $t=2$ </th>  </th>
 <tr> 
   <td> [♮,♮,#,#,♮,♮,♮] </td><td> [0,0,0,0,1,0,0] </td><td> [♮,♮,#,#,♮,♮,♮]</td> <td>[0,0,1,0,0,0,0] </td>
 </tr>
 <tr> 
   <td> [♮,♮,#,#,♮,♮,♮] </td><td> [0,0,0,0,1,0,0] </td><td> [♮,♮,#,#,♮,♮,#]</td> <td>[0,0,1,0,0,0,0] </td>
 </tr>
</tbody>  
</table> 

Lastly, we can also note that the first sheet does not change any pedal, while the second sheet changes pedals one times. I.e. only the first sheet will be written to the text file. 
