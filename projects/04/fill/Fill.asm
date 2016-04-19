// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.

// Initialize R13 (screen position) to SCREEN
@SCREEN
D=A
@R13
M=D

// Start Loop
(LOOP)
// Check if Keyboard is pressed
@KBD
D=M
//Jump if pressed
@PRESSED
D;JNE
//Jump if not pressed
@NOTPRESSED
D;JEQ

//Pressed
(PRESSED)
// Jump back to LOOP if cursor is greater than or equal to KBD
@R13
D=M
@KBD
D=A-D
@LOOP
D;JLE

// If keyboard is pressed set item after current screen position to -1 and increase screen position by 1
@R13
A=M
M=-1
D=A
@R13
M=D+1
@LOOP
0;JEQ


(NOTPRESSED)
// Jump back to LOOP if cursor is less than SCREEN
@R13
D=M
@SCREEN
D=D-A
@LOOP
D;JLT

// If keyboard is not pressed set current screen position to 0 and decrease screen position by 1
@R13
A=M
M=0
D=A
@R13
M=D-1
@LOOP
0;JMP
