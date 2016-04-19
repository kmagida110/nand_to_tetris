// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Set anything in R2 to 0
@0
D=A
@2
M=D

// Loop and add R0 to R2 R1 times
(LOOP)

//End Loop if loop has run R1 times
@1
D=M
@END
D;JEQ

// Add R0 value to R2
@0
D=M
@2
M=D+M
// Decrement R1
@1
M=M-1

// Loop until R1 = 0 and then end in an infinite loop
@LOOP
0;JMP

//Loop to end
(END)
@END
0;JMP
