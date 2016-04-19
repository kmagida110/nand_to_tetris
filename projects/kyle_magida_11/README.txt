##########################################
## 	Computer Systems					##
##  Winter 2016							##
##  Kyle Magida							##
##  Project 11 - Compiler 2 			##
##										##
##########################################

Dependencies:

To run this code a Python interpreter that can run a Python 3 program must be installed on the computer. It uses the os and sys libraries that come standard with python

File structure:

	Main folder: 
		README.txt

	src folder: 
		complier.py - File that converts Jack files to XML that can be read by a complier.

Running code:

	The code should be run in the following manner from the src directory (Note that it can be run from any directory as long as
	the path to the src folder is included before complier.py):

	$ python complier.py FILE_LOCATION 

	Inputs:
		FILE_LOCATION: Replace with a directory or file of the type .jack that should be translated into .vm. If a directory is passed all files in that directory that have a .jack will be translated, others will be ignored.  


Output:
	The program will translate .vm files in the same directory location as the .jack files. The resulting set if files can be run on the VM Emulator by loading the entire directory. OS files can be loaded via transfer to the same directory to avoid using the built-in implementations.

	