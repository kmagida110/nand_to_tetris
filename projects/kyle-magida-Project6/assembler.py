import queue
import sys
A_COMMAND = 'A'
L_COMMAND = 'L'
C_COMMAND = 'C'

class Parser(object):
	'''
	Parses a file and stores a list of tuples wih the command type and additional information about the command
	'''
	
	def __init__(self, input_file):
		self.input_file = input_file
		self.command_list = self.create_command_list()
		self.parsed_list = []
		self.parsed = False


	def create_command_list(self):
		'''
		Strip white space and comments to create a list of all the commands
		'''

		command_list = []
		with open(self.input_file,'r') as input_file:
			for full_line in input_file:
				# Remove comments, spaces and white space
				full_line = full_line.split('//')[0]
				reduced_line = full_line.replace(' ','').replace('\t','').strip()

				# Only add rows with text, covers comment lines and initally blank lines
				if reduced_line != '\n' and reduced_line != '':
					command_list.append(reduced_line)
		return command_list

	def process_type(self,command):
		'''
		Returns type of command (A, C, or L) and associated value (for A and L) as a tuple
		'''
		if command[0] == '@':
			command_type = A_COMMAND
			symbol = int(command[1:])
		elif command[0] == '(' and command[-1] == ')':
			command_type = L_COMMAND
			symbol = command[1:-1]
		else:
			command_type = C_COMMAND
			symbol = self.divide_c_command(command)

		return {'type':command_type,'command':symbol}

	def divide_c_command(self,command):
		'''
		Takes c command and returns dictionary of dest, comp and jump
		'''
		rv = {'dest':None,'comp':None,'jump':None}
		if ';' in command and '=' in command:
			split_by_semi = command.split(';')
			split_by_eq = split_by_semi[0].split('=')
			rv['comp'] = split_by_eq[1]
			rv['jump'] = split_by_semi[1]
			rv['dest'] = split_by_eq[0]
			return rv
		if ';' not in command:
			split_by_eq = command.split('=')
			rv['dest'] = split_by_eq[0]
			rv['comp'] = split_by_eq[1]
			return rv
		if '=' not in command:
			split_by_semi = command.split(';')
			rv['jump'] = split_by_semi[1]
			rv['comp'] = split_by_semi[0]
			return rv

	def get_parsed_list(self):
		'''
		Take full list of commands and converts into commands that can be used by the encoder
		'''
		if self.parsed:
			return self.parsed_list

		for command in self.command_list:
			command_dict = self.process_type(command)
			if command_dict['type'] != L_COMMAND:
				self.parsed_list.append(command_dict)

		self.parsed = True

		return self.parsed_list

class Encoder(object):

	def __init__(self):
		
		self.parsed_list = parsed_list
		self.jump_dict = {None:'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}
		self.dest_dict = {None:'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}
		self.comp_dict = {'0':'101010','1':'111111','-1':'111010','D':'001100','A':'110000','!D':'001101','!A':'110001','-D':'001111','-A':'110011','D+1':'011111','A+1':'110111','D-1':'001110','A-1':'110010','D+A':'000010','D-A':'010011','A-D':'000111','D&A':'000000','D|A':'010101'}

			
	def convert_to_machine(self,command_tuple):
		'''
		Use code type to convert to machine code
		'''
		if command_tuple['type'] == A_COMMAND:
			return self.get_A_code(command_tuple['command'])
		elif command_tuple ['type'] == C_COMMAND:
			return self.get_C_code(command_tuple['command'])
		else:
			return False

	def get_A_code(self,command):
		'''
		Convert int number to binary
		'''
		# Handle overflow and only get 15 characters

		return '0' + "{0:015b}".format(command)[-15:]

	def get_C_code(self,command_dict):
		dest = self.dest_dict[command_dict['dest']]
		jump = self.jump_dict[command_dict['jump']]
		comp = self.get_comp_code(command_dict['comp'])
		return '111' + comp + dest + jump

	def get_comp_code(self,comp):
		if 'M' in comp:
			a = '1'
			comp = comp.replace('M','A')
		else:
			a = '0'

		return a + self.comp_dict[comp]

if __name__ == '__main__':
	
	#Check that script is called appropriately
	if len(sys.argv) < 2:
		print("Usage: python assembler.py FILENAME")
		exit(1)

	input_filename = sys.argv[1]

	#Get name of output file and open for writing
	output_file = input_filename[:input_filename.rfind('.')] + '.out'
	out = open(output_file,'w')
	parser = Parser(input_filename)
	parsed_list = parser.get_parsed_list()
	encoder = Encoder()
	for command_dict in parsed_list:
		out.write(encoder.convert_to_machine(command_dict)+'\n')
	out.close()
# 		