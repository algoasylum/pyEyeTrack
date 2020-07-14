Pupil tracking on text UI

Description: This application/demo tracks the eyes of the user while the user reads a sample text displayed on the UI.

Working: As the program runs, a blank PyQt window appears on the screen. Press 'ctrl' to display a line of text on the screen. This timestamp denotes the start time of the user reading the line. Press 'shift' after reading the line. This timestamp denotes the end time of the user reading the line. Both the start time and the end time of the user reading the lines are logged into a CSV. On the keypress of Escape, the program terminates. 

Library Function: The program makes use of the pupil tracking functionality of the library.

Output: The application returns a CSV having the x and y coordinates of both the eyes. 

