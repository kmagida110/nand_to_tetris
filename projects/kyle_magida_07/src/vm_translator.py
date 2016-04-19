import sys
from os import listdir
MEMORY_LIST = ['push','pop']

class Parser(object):
	'''
	Parses file and saves list of parsed commands
	'''
	def __init__(self):
		self.command_list = []
		self.parsed_list = []
		self.parsed = False
		self.memory_list = MEMORY_LIST
		
	def add_file_to_command_list(self,input_file):
		'''
		Strip white space and comments from file to create a list of all the commands, split by space
		'''

		command_list = []
		with open(input_file,'r') as input_file:
			for full_line in input_file:
				# Remove comments, spaces and white space
				full_line = full_line.split('//')[0]
				reduced_line = full_line.replace('\t','').strip()

				# Only add rows with text, covers comment lines and initally blank lines
				if reduced_line != '\n' and reduced_line != '':
					command_list.append(reduced_line.split())
		self.command_list = self.command_list + command_list

	def parse_commands(self):
		'''
		Parse list into segments; commands and arguments
		'''
		if self.parsed:
			print('already parsed')
			return
		parsed_list = []

		# Separate commands into dictionary
		for command in self.command_list:
			command_dict = {}
			if command[0] in MEMORY_LIST:
				command_dict['segment'] = command[1]
				command_dict['index'] = command[2]
			command_dict['command'] = command[0]
			parsed_list.append(command_dict)

		self.parsed = True
		self.parsed_list = parsed_list

class CodeWriter(object):
	'''
	Converts a command dictionary to Hack code
	'''
	def __init__(self):
		self.arithmatic_dict = {'add':self.add,'sub':self.subtract,'neg':self.neg,'eq':self.eq,'gt':self.gt,'lt':self.lt,'and':self.and_string,'or':self.or_string,'not':self.not_string}
		self.memory_list = MEMORY_LIST
		self.memory_lookup = {'local':1,'argument':2,'this':3,'that':4,'static':16,'pointer':3,'temp':5,'static':256}
		self.linear_storage = ['temp','pointer','static']
		self.comp_counter = 0

	def run_command(self,command_dict):
		'''
		Determine the type of command and call the appropriate function
		'''
		if command_dict['command'] in self.memory_list:
			command_string = self.get_memory_string(command_dict)
		else:
			command_string = self.get_arithmatic_string(command_dict)

		return command_string

	def get_memory_string(self,command_dict):
		if command_dict['command'] == 'pop':
			rv = self.pop(command_dict['segment'],command_dict['index'])
		elif command_dict['command'] == 'push':
			rv = self.push(command_dict['segment'],command_dict['index'])
		return rv

	def get_arithmatic_string(self,command_dict):
		'''
		Look up value in dictionary and return string
		'''
		equation = self.arithmatic_dict[command_dict['command']]
		return equation()

	def push(self,segment,offset):

		# Get Value
		if segment == 'constant':
			final_string = '@' + str(offset) + '\n'
			final_string += 'D=A\n@SP\nA=M\nM=D\n'
			final_string += self.increment_SP()
		elif segment in self.linear_storage:
			final_string = '@' + str(self.memory_lookup[segment] + int(offset)) + '\nD=M\n@SP\nA=M\nM=D\n'
			final_string += self.increment_SP()
		else:
			final_string = '@' + str(offset) + '\nD=A\n'
			final_string += '@' + str(self.memory_lookup[segment]) + '\nA=D+M\nD=M\n'
			# Put value on stack
			final_string += '@SP\nA=M\nM=D\n'
			final_string += self.increment_SP()

		return final_string

	def pop(self,segment,offset):

		# For linear storage get top value then go to (start + offset) and store
		if segment in self.linear_storage:
			final_string = self.load_top_and_decrement()
			final_string += '@' + str(self.memory_lookup[segment]+ int(offset)) + '\nM=D\n'
			return final_string

		else:
			# Save memory address (stored item + offset) in R13
			final_string = '@' + str(offset) + '\nD=A\n@' + str(self.memory_lookup[segment]) + '\nD=M+D\n@R13\nM=D\n'
			# Pop and log value in D
			final_string += self.load_top_and_decrement()
			#Get address and store value to memory
			final_string += '@R13\nA=M\nM=D\n'
			return final_string

	def add(self):
		final_string = self.load_top_and_decrement()
		final_string += 'A=A-1\nM=M+D\n'
		return final_string

	def subtract(self):
		final_string = self.load_top_and_decrement()
		final_string += 'A=A-1\nM=M-D\n'
		return final_string
	
	def neg(self):
		'''
		Negate top of stack
		'''
		return '@0\nD=A\n@SP\nA=M-1\nM=D-M\n'

	def not_string(self):
		'''
		Not top of stack
		'''
		return '@SP\nA=M-1\nM=!M\n'

	def and_string(self):
		final_string = self.load_top_and_decrement()
		final_string += 'A=A-1\nM=D&M\n'
		return final_string

	def or_string(self):
		final_string = self.load_top_and_decrement()
		final_string += 'A=A-1\nM=D|M\n'
		return final_string

	def eq(self):
		final_string = self.load_top_and_decrement()
		# Get next value and compare
		final_string += 'A=A-1\nD=D-M\n@TRUE' + str(self.comp_counter) + '\nD;JEQ\n'
		# Set if false
		final_string += '@SP\nA=M-1\nM=0\n@CONTINUE' + str(self.comp_counter) +'\n0;JMP\n'
		# Set if true
		final_string += '(TRUE' + str(self.comp_counter) + ')\n@SP\nA=M-1\nM=-1\n(CONTINUE' + str(self.comp_counter) +')\n'
		self.comp_counter += 1
		return final_string

	def gt(self):
		final_string = self.load_top_and_decrement()
		# Get next value and compare
		final_string += 'A=A-1\nD=M-D\n@TRUE' + str(self.comp_counter) + '\nD;JGT\n'
		# Set if false
		final_string += '@SP\nA=M-1\nM=0\n@CONTINUE' + str(self.comp_counter) +'\n0;JMP\n'
		# Set if true
		final_string += '(TRUE' + str(self.comp_counter) + ')\n@SP\nA=M-1\nM=-1\n(CONTINUE' + str(self.comp_counter) +')\n'
		self.comp_counter += 1
		return final_string

	def lt(self):
		final_string = self.load_top_and_decrement()
		# Get next value and compare
		final_string += 'A=A-1\nD=M-D\n@TRUE' + str(self.comp_counter) + '\nD;JLT\n'
		# Set if false
		final_string += '@SP\nA=M-1\nM=0\n@CONTINUE' + str(self.comp_counter) +'\n0;JMP\n'
		# Set if true
		final_string += '(TRUE' + str(self.comp_counter) + ')\n@SP\nA=M-1\nM=-1\n(CONTINUE' + str(self.comp_counter) +')\n'
		self.comp_counter += 1
		return final_string

	# Helper functions
	def load_top_and_decrement(self):
		'''
		Get the item at SP, load into D and decrement SP
		'''
		return '@SP\nAM=M-1\nD=M\n'

	def increment_SP(self):
		return '@SP\nM=M+1\n'

	def decrement_SP(self):
		return '@SP\nM=M-1\n'
		
def translate_file(filename):
	'''
	take a file and convert it to machine language
	'''
	p = Parser()
	p.add_file_to_command_list(filename)
	p.parse_commands()
	parsed_list = p.parsed_list
	cw = CodeWriter()
	new_file = filename[:filename.rfind('.vm')] + '.asm'
	# Set static pointer
	write_string = '@256\nD=A\n@SP\nM=D\n'

	# Build long string to write to file
	for command_dict in parsed_list:		
		write_string += cw.run_command(command_dict)
	
	# Write to file
	with open(new_file,'w') as write_file:
		write_file.write(write_string)

if __name__ == '__main__':
	# Check that script is called appropriately
	if len(sys.argv) < 2:
		print("Usage: python assembler.py FILENAME or DIRECTORY")
		sys.exit(1)

	input_string= sys.argv[1]
	try:
		# Check if it is a directory and add / to the front
		file_list = listdir(input_string)
		if input_string[-1] != '/':
			input_string = input_string + '/'

		file_list = [input_string + x for x in file_list]
	except:
		file_list = input_string

	# Translate each file that is a .vm file
	for filename in file_list:
		if '.vm' in filename:
			translate_file(filename)
