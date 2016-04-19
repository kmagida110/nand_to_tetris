##########################################
## 	Computer Systems					##
##  Winter 2016							##
##  Kyle Magida							##
##  Project 0 - Strip White Space		##
##										##
##########################################

Dependencies:

To run this code a Python interpreter that can run a Python 2 program must be installed on the computer. It also uses in sys library which is a component of the standard Python library.

File structure:

	Main folder: 
		README.txt

	src folder: 
		strip_white_space.py - This is the main file that will strip the white space from a input file and save a separate file
		in the input file's directory without white space or comments if the no comments option described below is enabled.

Running code:

	The code should be run in the following manner from the src directory (Note that it can be run from any directory as long as
	the path to the src folder is included before strip_white_space.py:

Inputs:
	FILENAME: Replace with path and filename of the file that will be stripped of white space
	no-comments: if included after FILENAME the script will also strip comments from the file

	$ strip_white_space.py FILENAME no-comments

	Note that no-comments is an optional command

Output:
	The program will take the input file and save a copy of it with no white space (and no comments if that option is enabled) in the same directory as the input file. The copy will replace the filetype of .in with .out.
