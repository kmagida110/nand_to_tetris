##########################################
## 	Computer Systems					##
##  Winter 2016							##
##  Kyle Magida							##
##  Project 8 - Virtual Machine 2		##
##										##
##########################################

Dependencies:

To run this code a Python interpreter that can run a Python 3 program must be installed on the computer. It uses the os and sys libraries that come standard with python

File structure:

	Main folder: 
		README.txt

	src folder: 
		vm_translator.py - Main file that converts virtual language into Hack code

Running code:

	The code should be run in the following manner from the src directory (Note that it can be run from any directory as long as
	the path to the src folder is included before vm_translator.py):

	$ python vm_translator.py FILE_LOCATION 

	Inputs:
		FILE_LOCATION: Replace with a directory or file of the type .vm that should be translated into .asm. If a directory is passed all files in that directory that have a .vm will be translated, others will be ignored. The script will identify these files.

	

Output:
	The program will convert the input files into a single file that initializes the Stack Pointer and runs Sys.init. The resulting .asm code should run the given program on the CPU Emulator 

Known Bugs:
	This is able to pass all of the tests with the exception of the Fibonacci and Static. I am doing something wrong with either the labels or the initialization, likely a combination of the two. This is a slight improvement over what I handed in last week on time and would like it to be considered with a penalty instead of what I submitted last week. If it is an easy fix I would greatly appreciate feedback on what is wrong, this has been very a very frustrating bug.
	