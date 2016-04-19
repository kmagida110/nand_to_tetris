##########################################
## 	Computer Systems					##
##  Winter 2016							##
##  Kyle Magida							##
##  Project 6 - Assembler				##
##										##
##########################################

Dependencies:

To run this code a Python interpreter that can run a Python 2 program must be installed on the computer. It uses the copy and sys libraries that come standard with python

File structure:

	Main folder: 
		README.txt

	src folder: 
		assembler.py - Main file that converts Hack code to machine readable binary using a Python script

Running code:

	The code should be run in the following manner from the src directory (Note that it can be run from any directory as long as
	the path to the src folder is included before assembler.py:

Inputs:
	FILENAME: Replace with path and filename of the file that will converted into assembly language

	$ python assembler.py FILENAME 

Output:
	The program will convert the input file into assembly language and save an output file to the same directory. The output file will replace .asm with .hack while maintaining the rest of the file name.
