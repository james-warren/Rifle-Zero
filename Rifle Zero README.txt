Rifle Zero.py  JLW 2014

This program is a work in progress.  The idea is that, with a photograph of a rifle target/dartboard etc, with some known feature to scale by, the user could click on the shot impact points and aim point/bullseye. The mean point of impact would be calculated, along with x and y corrections needed to hit the aim point.

Rifle Zero.py will prompt for the filepath for the "target.gif" file provided.  It is assumed that the target ring is 1 cm in diameter.

Shots:
Left clicking on the shot impact points will mark them with green dots.
"D" will delete the shots in reverse sequece of allocation.

Bullseye/aim point
Likewise, right clicking will mark the bullseye (red dot).
"B" will delete the bullseye.

Scale Cursor Control:
Using the on-screen controls, turn the cursor on, then use the direction and +/- controls to superimpose the red circle over the black ring in the target image (assumed to be 1cm diameter).

Mean Point of Impact:
Pressing M will toggle the mean point of impact (MPI) and correction displays.

Note that the MPI will need to be toggled on and off in order to update, if changes are made to the shots or cursor (it is planned to make this dynamically update in the future).

This is one of my early attempts at OOP and could certainly be improved upon.  I wanted to code something with classes, some calculations, and GUI elements.
I need to go back through this code and improve things such as separating classes into different files and adopting better naming conventions and formats.

-- Minor update 17/05/15
Changed the correction numbers to 2 dp format (need to use IntVar to communicate with label widget, so the formatting was done when setting the IntVar, rather than trying to reformat the IntVar into something else).
