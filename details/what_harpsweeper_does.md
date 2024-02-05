## The Problem

Harpsweeper works out which tunes are playable on the harp, and how to play them. 
Harpsweeper exists because this is a non-trivial problem. 

On the harp, only seven notes are available at a point in time. 
Which notes this is can be adjusted using seven pedals, with three possible configurations each. Figuring out if a sequence is 
playable, and how to play it, can become challanging for the following reasons: 
 - There are $7^3=2187$ possible pedal configurations at a given time.
 - It is impossible to change two pedals on the same foot at the same time.
 - Many notes are accessable from multiple strings, while some are accessable from only one string (D,G, and A).
 - Notes should be allowed to ring after being played, restricting when pedals can change. 

### Examples

#### Example 1

To illustrate the problem, consider a few simple and parhaps silly examples: 

Which if these two sequences are playable on the harp?

Example Sequence 1a)             |  Example Sequence 1b)
:-------------------------:|:-------------------------:
![](https://raw.githubusercontent.com/adamreir/harpsweeper/main/details/example_images/Example_sequence_1a.png)  | ![](https://raw.githubusercontent.com/adamreir/harpsweeper/main/details/example_images/Example_sequence_1b.png)

The answer is Example Sequence 1b). Example Sequence 1a) is not possible to play, because: 
 - The G string is occupied playing G in beat 1, which forces F# to be played on the F string.
 - The E string is occupied playing E on beat 1.
 - Hence neither the E or the F strings are in position to play F in beat 2.

The only difference between the two sequences is that the G in sequence 1a) is sharpened to Ab in sequence 1b). The reason that sequence 1b) is playable is:   
 - Ab (G in sequence 1a)) can be played using the A string, freeing up the G string.
 - Gb (F# in sequence 1a)) can now be played using the G string, freeing up the F string.
 - The F on beat 2 can be played using the F string.

Although this example is trivial, it illustrates why organizing for harp can be challanging: Adjusting a single note can propagate through the harp, changing which other notes are played by what string. 

In Harpsweeper, the to examples looks like this: 

Example Sequence 1 (Harpsweeper) |  Example Sequence 2 (Harpsweeper)
:-------------------------:|:-------------------------:
![](https://raw.githubusercontent.com/adamreir/harpsweeper/main/details/example_images/Example_sequence_1_harpsweeper.png)  |  ![](https://raw.githubusercontent.com/adamreir/harpsweeper/main/details/example_images/Example_sequence_2_harpsweeper.png)

#### Example 2

Now consider an example that is a bit more complicated. Is the following sequence playable on the harp? 

Example Sequence 2 |
:-------------------------:|
![](https://raw.githubusercontent.com/adamreir/harpsweeper/main/details/example_images/Example_sequence_2.png) |

The answer is no! At least given the restrictions that are programmed into Harpsweeper. Here is the reason: 
 - The A, G, F and E strings are in the ♮ position in beat one and two.
 - The G string cannot change in beat 3, because it is ringing.
 - The G string can change to the b or # position in beat 4, but that is to late to play Ab or Gb.
 - The A string can change to Ab in beat 3
 - The G string can change to Gb in beat 3, but
 - Both the A and G strings cannot be changed simultaneouly on beat 3, because their pedal is on the same foot.

Again, this simple example illustrates that the pedals are interconnected in a way that makes composing for the harp challanging. 

In Harpsweeper, the impossibility of this sequence looks like this: 

Example Sequence 2 (Harpsweeper) |
:-------------------------:|
![](https://raw.githubusercontent.com/adamreir/harpsweeper/main/details/example_images/Example_sequence_2_harpsweeper.png) |

