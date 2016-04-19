##########################################
## 	Computer Systems					##
##  Winter 2016							##
##  Kyle Magida							##
##  Project 10 - Compiler 1 			##
##										##
##########################################

Dependencies:

To run this code a Python interpreter that can run a Python 3 program must be installed on the computer. It uses the os and sys libraries that come standard with python

File structure:

	Main folder: 
		README.txt

	src folder: 
		parse_to_xml.py - File that converts Jack files to XML that can be read by a complier.

Running code:

	The code should be run in the following manner from the src directory (Note that it can be run from any directory as long as
	the path to the src folder is included before parse_to_xml.py):

	$ python parse_to_xml.py FILE_LOCATION 

	Inputs:
		FILE_LOCATION: Replace with a directory or file of the type .jack that should be translated into .xml. If a directory is passed all files in that directory that have a .jack will be translated, others will be ignored.  

	

Output:
	The program will save .xml files in the same place as the .jack files with _parsed.xml at the end to distinguish them from other files. The .xml files are also indented for better visual inspection.

	