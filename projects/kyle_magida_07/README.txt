##########################################
## 	Computer Systems					##
##  Winter 2016							##
##  Kyle Magida							##
##  Project 7 - Virtual Machine 1		##
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
		FILE_LOCATION: Replace with a directory or file of the type .vm that should be translated into .asm. If a directory is passed all files in that directory that have a .vm will be translated, others will be ignored. The script will identify 

	

Output:
	The program will convert the input file(s) into assembly language and save an output file or files to the same directory. The output file will replace .vm with .asm while maintaining the rest of the file name.