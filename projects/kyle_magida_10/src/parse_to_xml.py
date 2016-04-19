import sys
import os
KEYWORDS=['field','class','constructor','function','method','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
SYMBOLS = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
RENAME_DICT = {'<':'&lt;','>':'&gt;','&':'&amp;'}
CLASS_VAR_DEC = ['static','field']
SUBROUTINE_DEC = ['constructor','function','method']
OPS = ['+','-','*','/','&','|','<','>','=','~']
UNARY_OPS = ['-','~']


def add_prefix(prefix,final_list):
	if prefix == '':
		return
	if prefix in KEYWORDS:
		final_list.append((prefix,'keyword'))
	else:
		final_list.append((prefix,'identifier'))

def string_to_list(full_line):
	'''
	Traverses through string until certain patterns are found adds resulting xml to list
	'''

	line_len = len(full_line)
	position = 0
	final_list = []
	last_added = -1

	# Loop until end of string
	while position < line_len:

		current_char = full_line[position]

		# Keep track of unused parts of code
		if (last_added + 1) == position:
			prefix = ''
		else:
			prefix = full_line[last_added+1:position].strip()
		
		if position == (line_len - 1):
			suffix = ''
		else:
			suffix = full_line[position:]

		if current_char == ' ':
			add_prefix(prefix,final_list)
			last_added = position
			position += 1
			continue

		# Check for string
		if current_char == '"':
			
			end_quote = suffix.find('"',1)
			add_prefix(prefix,final_list)			
			final_list.append((full_line[position+1:end_quote+position],'stringConstant'))		

			position = end_quote + position + 1
			last_added = position - 1
			continue

		#Check for comments
		if full_line[position:position+2] == '/*':
			
			end_quote = suffix.find('*/',1) 
			add_prefix(prefix,final_list)		

			position = end_quote + position + 2
			last_added = position - 1
			continue

		# Check for symbol
		if current_char in SYMBOLS:
			add_prefix(prefix,final_list)
			final_list.append((current_char,'symbol'))
			last_added = position
			position += 1
			continue

		# Check for int
		try:
			x = int(current_char) / 4
			counter = 1
			end=True
			# Break out of loop at end of int
			while(end):
				try:
					x = int(full_line[position+counter]) / 4
					counter += 1
				except:
					end =False
			final_list.append((full_line[position:position+counter],'integerConstant'))
			position = position + counter 
			last_added = position - 1
			continue
		except:
			pass

		position += 1
	
	return final_list

def prep_file_list(args):
	'''
	Converts input string (filename or directory) into a list of files
	'''
	
	input_string = args[1]

	try:
		# Check if it is a directory and add / to the front
		file_list = os.listdir(input_string)
		directory = os.path.dirname(input_string)
		if directory == '':
			directory = input_string
		directory = directory + '/'
		
	except:
		file_list = [os.path.basename(input_string)]
		directory = os.path.dirname(input_string)
		if directory != '':
			directory = directory + '/'

	read_files = [directory + filename for filename in file_list if '.jack' in filename]
	write_files = [directory +filename.replace('.jack','_parsed.xml') for filename in file_list if '.jack' in filename]
	
	return read_files, write_files		

def write_file(read_file,write_file):
	with open(read_file) as r_file:
		with open(write_file,'w') as write_f:
			# build string with whole file and remove white space
			s = ''
			for line in read_file:
				line = line.split('//')[0]
				s += line.replace('\t','').strip() + ' '
			#new_s = (string_to_list(s))
			#print(s)
			ce = CompilationEngine(string_to_list(s))
			write_f.write(ce.get_xml_list())


class CompilationEngine(object):
	"""
	Translate list of tokens into nested xml
	"""
	def __init__(self, token_list):
		
		self.iterator = iter(token_list)
		self.xml_string = ''
		self.cur_token_name = ''
		self.cur_item_type = ''
		self.statement_dict = {'let':self.letStatement,'if':self.ifStatement,'while':self.whileStatement,'do':self.doStatement,'return':self.returnStatement}
		self.look_ahead_token = ''
		self.look_ahead_type = ''
		self.look_ahead = False

	# Compile functions
	def compile_class(self):
		'''
		Begins recursive path to nest xml
		'''
		
		self.iterate()
		
		#Assume string begins with class declaration
		if self.cur_token_name != 'class':
			print('File does not begin with class')
			sys.exit(1)

		# Write class
		self.xml_string += '<class>\n' 
		self.write_current_token(1)
		
		# Write class name and opening bracket
		self.write_current_token(1)
		self.write_current_token(1)

		while self.cur_token_name in CLASS_VAR_DEC or self.cur_token_name in SUBROUTINE_DEC:
			if self.cur_token_name in SUBROUTINE_DEC:
				self.xml_string += '\t<subroutineDec>\n'				
				self.compile_subroutine(2)
				self.xml_string += '\t</subroutineDec>\n'
			if self.cur_token_name in CLASS_VAR_DEC:
				self.xml_string += '\t<classVarDec>\n'
				self.compile_class_var_dec(2)
				self.xml_string += '\t</classVarDec>\n'

			

		# Write closing bracket
		self.write_w_o_iterate(1)
		self.xml_string += '</class>'
		return

	def compile_subroutine(self,level):

		# Routine type
		self.write_current_token(level)
		# Return type, name and first paren
		self.write_current_token(level)
		self.write_current_token(level)
		self.write_current_token(level)

		indent = level * '\t'
		if self.cur_token_name == '(':
			self.write_current_token(level)

		self.xml_string += indent + '<parameterList>\n'
		self.compile_parameter_list(level+1)
		self.xml_string += indent + '</parameterList>\n'

		if self.cur_token_name == ')':
			self.write_current_token(level)

		self.xml_string += indent + '<subroutineBody>\n'
		self.compile_subroutine_body(level+1)
		self.xml_string += indent + '</subroutineBody>\n'
		return
	
	def compile_subroutine_body(self,level):

		indent = level * '\t'
		# Opening bracket
		self.write_current_token(level)
		while self.cur_token_name == 'var':
			self.xml_string += indent + '<varDec>\n'
			self.compile_var_dec(level+1)
			self.xml_string += indent + '</varDec>\n'

		self.parse_statements(level)
		# Print closing bracket
		self.write_current_token(level)
		return

	def compile_var_dec(self,level):
		
		# Write var
		self.write_current_token(level)
		self.iterate_until(level,';',True)
		return
		
	def compile_parameter_list(self,level):
		# Don't write closing paren
		self.iterate_until(level,')',False)
		return

	def compile_class_var_dec(self,level):
		# static or field
		self.write_current_token(level)		
		#Iterate through end of line
		self.iterate_until(level,';',True)
		return
	
	def parse_statements(self,level):
		
		indent = level *'\t'
		self.xml_string += indent + '<statements>\n'	

		while self.cur_token_name != '}':
			if self.cur_token_name not in self.statement_dict:
				print(self.xml_string)
				print(self.cur_token_name, " Not in statement dict")
				sys.exit(1)

			func = self.statement_dict[self.cur_token_name]
			func(level+1)
			
		self.xml_string += indent + '</statements>\n'
		return			

	# Statements
	def letStatement(self,level):
		
		indent = level *'\t'
		self.xml_string += indent + '<letStatement>\n'

		# write let and var name
		self.write_current_token(level+1)
		self.write_current_token(level+1)

		if self.cur_token_name == '[':
			self.write_current_token(level+1)
			self.write_expression(level+1)
			# Write ]
			self.write_current_token(level+1)
		# Write equals
		self.write_current_token(level+1)
		self.write_expression(level+1)
		# EOL
		self.write_current_token(level+1)
		self.xml_string += indent + '</letStatement>\n'
		return

	def ifStatement(self,level):

		indent = level *'\t'
		self.xml_string += indent + '<ifStatement>\n'
		self.write_current_token(level+1)
		# ( + expression + ) + {
		self.write_current_token(level+1)
		self.write_expression(level+1)
		self.write_current_token(level+1)	
		self.write_current_token(level+1)

		self.parse_statements(level+1)
		# Close bracket
		self.write_current_token(level+1)
		# Check for else		
		if self.cur_token_name == 'else':
			#Write else {
			self.write_current_token(level+1)
			self.write_current_token(level+1)
			self.parse_statements(level+1)
			# Close bracket
			self.write_current_token(level+1)

		self.xml_string += indent + '</ifStatement>\n'
		return

	def whileStatement(self,level):

		indent = level * '\t'
		double_indent = (level + 1)*'\t'
		self.xml_string += indent + '<whileStatement>\n'
		# While & first (
		self.write_current_token(level+1)
		self.write_current_token(level+1)
		# Condition
		self.write_expression(level+1)
		# ){
		self.write_current_token(level+1)
		self.write_current_token(level+1)
		
		# Statements
		self.parse_statements(level+1)
		# Close bracket
		self.write_current_token(level+1)		
		self.xml_string += indent + '</whileStatement>\n'
		return

	def doStatement(self,level):

		indent = level * '\t'
		self.xml_string += indent + '<doStatement>\n'

		# do keyword
		self.write_current_token(level+1)
		# Write subroutine
		self.look_ahead_func()
		self.write_subroutine_call(level+1)
		# Write semi-colon
		self.write_current_token(level+1)
		self.xml_string += indent + '</doStatement>\n'
		return

	def returnStatement(self,level):
		# Write return
		indent = level * '\t'
		self.xml_string += indent + '<returnStatement>\n'
		self.write_current_token(level+1)

		# Write expression
		if self.cur_token_name !=';':
			self.write_expression(level+1)

		# Write semi-colon
		self.write_current_token(level+1)
		self.xml_string += indent + '</returnStatement>\n'
		return

	def write_expression(self,level):
		indent = level *'\t'
		self.xml_string += indent + '<expression>\n'
		self.write_term(level+1)

		#Add ops as needed
		while self.cur_token_name in OPS:
			self.write_current_token(level+1)
			self.write_term(level+1)
		self.xml_string += indent + '</expression>\n'
		
	def write_term(self,level):

		indent = level *'\t'
		self.xml_string += indent + '<term>\n'


		if self.cur_token_name =='(':
			self.write_current_token(level+1)
			self.write_expression(level+1)
			# Closing paren
			self.write_current_token(level+1)
			
		else:
			self.look_ahead_func()

			# check Unary
			if self.cur_token_name in UNARY_OPS:
				self.write_current_token(level+1)
				self.write_term(level+2)
			# Arrays
			elif self.look_ahead_token == '[':
				# name[exp]
				self.write_current_token(level+1)
				self.write_current_token(level+1)
				self.write_expression(level+1)
				self.write_current_token(level+1)
			#subroutine
			elif self.look_ahead_token in ['(','.']:
				self.write_subroutine_call(level+1)			
			else:
				# Write term
				self.write_current_token(level+1)
				
		self.xml_string += indent + '</term>\n'
		return

	def write_expression_list(self,level):

		indent = level *'\t'
		self.xml_string += indent + '<expressionList>\n'
		while self.cur_token_name != ')':
			self.write_expression(level+1)
			if self.cur_token_name == ',':
				self.write_current_token(level+1)
		self.xml_string += indent + '</expressionList>\n'
		return

	def write_subroutine_call(self,level):


		if self.look_ahead_token == '(':
			# Write function name
			self.write_current_token(level)
			# Write (
			self.write_current_token(level)

			self.write_expression_list(level)
			self.write_current_token(level)
		elif self.look_ahead_token == '.':
			# Class name
			self.write_current_token(level)
			# write . 
			self.write_current_token(level)
			# write subroutine name
			self.write_current_token(level)
			# (
			self.write_current_token(level)
			self.write_expression_list(level)
			self.write_current_token(level)
			
		else:
			# Error checking
			print(self.xml_string)
			print(self.cur_token_name,'Not a subroutine')
			sys.exit(1)
		return

	# Writing functions
	def look_ahead_func(self):
		'''
		Looks ahead and stores next iterator values without updating current
		'''
		self.look_ahead_token, self.look_ahead_type = next(self.iterator)
		self.look_ahead = True
		return

	def iterate(self):
		'''
		iterate and store results
		'''
		if self.look_ahead:
			self.cur_token_name = self.look_ahead_token
			self.cur_item_type = self.look_ahead_type
			self.look_ahead = False
		else:
			self.cur_token_name, self.cur_item_type = next(self.iterator)
		return

	def iterate_until(self,level,end_char,write_close):
		'''
		Iterate through a certain character and add the character if write_close is true
		'''
		while self.cur_token_name != end_char:
			self.write_current_token(level)

		if write_close:
			self.write_current_token(level)
		return

	def xml_encode(self,name,item_type,indent_num):
		'''
		xml a single encoded item
		'''
		rv = ''
		rv += indent_num*'\t'
		# Rename select tokens and encode with xml
		if name in RENAME_DICT:
			name = RENAME_DICT[name]

		rv += '<' + item_type + '> ' + name + ' </' + item_type + '>' + '\n'
		
		return rv
	
	def write_current_token(self,level):
		self.write_w_o_iterate(level)
		self.iterate()
		return

	def write_w_o_iterate(self,level):
		self.xml_string += self.xml_encode(self.cur_token_name,self.cur_item_type,level)
		return

	def get_xml_list(self):
		
		if self.xml_string == '':
			self.compile_class()
			return self.xml_string
		else:
			return self.xml_string

if __name__ == '__main__':
	args = sys.argv
	if len(args) != 2:
		print("Usage: python parse_to_xml.py FILENAME or DIRECTORY")
		sys.exit(1)

	
	read_files, write_files = prep_file_list(args)

	for i in range(len(read_files)):
		with open(read_files[i]) as read_file:
			with open(write_files[i],'w') as write_f:
				# build string with whole file and remove white space
				s = ''
				for line in read_file:
					line = line.split('//')[0]
					s += line.replace('\t','').strip() + ' '
				#new_s = (string_to_list(s))
				#print(s)
				ce = CompilationEngine(string_to_list(s))
				write_f.write(ce.get_xml_list())


				



