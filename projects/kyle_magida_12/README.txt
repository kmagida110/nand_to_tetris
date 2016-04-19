##########################################
## 	Computer Systems					##
##  Winter 2016							##
##  Kyle Magida							##
##  Project 12 - OS 		 			##
##										##
##########################################

Dependencies:

JackComplier.sh required to compile all .jack files. .vm files already exist if complier is not available.

File structure:

	Main folder: 
		README.txt

	src folder: 
		.jack files for all OS systems as well as .jack files to run Pong game

	test folders:
		All of these folders contain a .jack with original code as well as the respective test and comparison files for those classes

Running code:

	Programs are loaded as a whole, each folder should be complied using the form below and then the entire folder should be loaded into the VM. In the test cases the built-in OS will be used for some functions, with src all the custom built ones will be used.

	$ JackComplier.sh FOLDER
 
Output/Notes:
	The program will initialize the computer and then run the main function until completion or manual override. 
	Note that the custom OS without any built-in functions is quite slow. It appears to work correctly but is very slow. My guess is that this has to do with the efficiency of the math functions primarily as well as some of the screen functions. 