##########################################
## 	Computer Systems					##
##  Winter 2016							##
##  Kyle Magida							##
##  Project 9 - Jack Game				##
##										##
##########################################

Dependencies:

This code requires a Jack complier and the VM machine provided with the NandtoTetris program.

File structure:

	Main folder: 
		README.txt

	Snake folder: 
		Main.jack - Main file that initializes and runs game
		SnakeGame.jack - Contains attributes of the snake game and particulars on how it runs, includes function to run an instance of the game
		Snake.jack - Creates an instance of a snake that can move around the screen

Compiling code:

	The jack files need to be converted to .vm files using a complier. This can be done using the included complier in the following manner from the main directory. The Snake in the command below is the folder with the code for the game

	$ JackCompiler.sh Snake 



Running game:
	Once the code is complied load the program into the VM Emulater, set the screen on and animation off and then run the program. Instructions will appear on the screen.