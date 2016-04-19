import sys
import os
KEYWORDS=['field','class','constructor','function','method','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
SYMBOLS = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
RENAME_DICT = {'<':'&lt;','>':'&gt;','&':'&amp;'}
CLASS_VAR_DEC = ['static','field']
SUBROUTINE_DEC = ['constructor','function','method']
OPS_DICT = {'+':'add','-':'sub','*':'Math.multiply','/':'Math.divide','&':'and','|':'or','<':'lt','>':'gt','=':'eq','~':'not'}
UNARY_OPS_DICT = {'-':'neg','~':'not'}


class Symbol_Tables(object):
	'''build ordered list of symbol tables'''
	def __init__(self,name): 
		self.table_list = []
		self.add_new_table('class',name)

	def iterate_num_locals(self):
		self.table_list[0]['num_locals'] += 1
		return

	def get_num_locals(self):
		return self.table_list[0]['num_locals']

	def get_class_var(self):
		for table in self.table_list:
			if table['type'] == 'class':
				return table['num_locals']

	def get_class_name(self):
		for table in self.table_list:
			if table['type'] == 'class':
				return table['name']

	def add_new_table(self,table_type,name):
		new_table = {'type':table_type,'name':name,'num_locals':0,'label_counter':0}
		self.table_list.insert(0,new_table)
		return

	def get_and_iterate_label_counter(self):
		cur_val = self.table_list[0]['label_counter']
		self.table_list[0]['label_counter'] += 1
		name = self.get_class_and_func()
		return name + '.' + str(cur_val)

	def drop_table(self):
		'''
		Removes lowest symbol table 
		'''
		
		if len(self.table_list) > 1:
			self.table_list.pop(0)
		else:
			print('No table left')
			sys.exit(1)
		return

	def add_symbol(self,id_name,id_type,id_kind):
		cur_table = self.table_list[0]
		kind_num = cur_table.get(id_kind + '_counter',0)
		cur_table[id_kind + '_counter'] = kind_num + 1
		name_w_class = cur_table['name'] + '_' + id_name 

		cur_table[id_name] = {'type':id_type,'kind':id_kind,'kind_num':kind_num}
		return
		
	def var_count(self,kind):
		return table_list[0][kind]

	def get_symbol(self,identifier):
		'''
		Returns symbol dictionary or False if not in scope
		'''

		for table in self.table_list:
			if identifier in table:
				return table[identifier]
		return False

	def get_class_and_func(self):
		if 'class' in self.table_list[0]:
			return self.table_list[0]['name']
		else:
			return  self.table_list[1]['name'] + '.' + self.table_list[0]['name']
		 		
class Tokenizer(object):
	
	def __init__(self):
		self.symbol_dict = {}
		

	def add_prefix(self,prefix,final_list):
		if prefix == '':
			return
		if prefix in KEYWORDS:
			final_list.append((prefix,'keyword'))
		else:
			final_list.append((prefix,'identifier'))
		return

	def string_to_list(self,full_line):
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
				self.add_prefix(prefix,final_list)
				last_added = position
				position += 1
				continue

			# Check for string
			if current_char == '"':
				
				end_quote = suffix.find('"',1)
				self.add_prefix(prefix,final_list)			
				final_list.append((full_line[position+1:end_quote+position],'stringConstant'))		

				position = end_quote + position + 1
				last_added = position - 1
				continue

			#Check for comments
			if full_line[position:position+2] == '/*':
				
				end_quote = suffix.find('*/',1) 
				self.add_prefix(prefix,final_list)		

				position = end_quote + position + 2
				last_added = position - 1
				continue

			# Check for symbol
			if current_char in SYMBOLS:
				self.add_prefix(prefix,final_list)
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

	def prep_file_list(self,args):
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
		write_files = [directory +filename.replace('.jack','.vm') for filename in file_list if '.jack' in filename]
		
		return read_files, write_files		

	def string_from_file(self,read_file,write_file):
		with open(read_file) as r_file:
		
			# build string with whole file and remove white space
			s = ''
			for line in r_file:
				line = line.split('//')[0]
				s += line.replace('\t','').strip() + ' '
			ce = CompilationEngine(self.string_to_list(s))
			return ce.get_vm_list(os.path.basename(read_file).replace('.jack',''))

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
		self.symbol_table = None
		self.vm_string = ''

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
		self.iterate()
		
		# Write class name and opening bracket
		# Add class to symbol table
		class_name = self.cur_token_name
		self.symbol_table = Symbol_Tables(class_name)

		self.iterate(2)

		while self.cur_token_name in CLASS_VAR_DEC or self.cur_token_name in SUBROUTINE_DEC:
			
			if self.cur_token_name in SUBROUTINE_DEC:				
				self.compile_subroutine(class_name)
			if self.cur_token_name in CLASS_VAR_DEC:
				self.compile_class_var_dec()
		return

	def compile_subroutine(self,class_name):

		# Return type, name and first paren
		routine_type = self.cur_token_name
		self.iterate()
		return_type = self.cur_token_name
		self.iterate()		

		# Create subroutine table with name of subroutine
		self.symbol_table.add_new_table('subroutine',self.cur_token_name)
		if routine_type == 'method':
			self.symbol_table.add_symbol('this',class_name,'argument')
		func_name = 'function ' + class_name + '.' + self.cur_token_name


		self.vm_string += func_name + '\n'

		# Name and 1st paren
		self.iterate(2)

		if self.cur_token_name == '(':
			self.iterate()

		self.compile_parameter_list()

		if self.cur_token_name == ')':
			self.iterate()

		self.compile_subroutine_body()
		new_func_name = func_name + ' ' + str(self.symbol_table.get_num_locals())

		# Add local count to function call		
		self.vm_string = self.vm_string.replace(func_name,new_func_name)
		if routine_type == 'constructor':
			index = self.vm_string.find(new_func_name) + len(new_func_name) + 1
			mem_alloc = 'push constant ' + str(self.symbol_table.get_class_var()) + '\ncall Memory.alloc 1\npop pointer 0\n'
			self.vm_string = self.vm_string[:index] + mem_alloc + self.vm_string[index:]
		if routine_type == 'method':
			index = self.vm_string.find(new_func_name) + len(new_func_name) + 1
			constructor = 'push argument 0\npop pointer 0\n'
			self.vm_string = self.vm_string[:index] + constructor + self.vm_string[index:]


		
		self.symbol_table.drop_table()
		return
	
	def compile_subroutine_body(self):

		# Opening bracket
		self.iterate()

		while self.cur_token_name == 'var':
			self.iterate()
			self.compile_var_dec()
			
		self.parse_statements()
		# closing bracket
		self.iterate()
		return 

	def compile_var_dec(self):
		
		# Write var
		while self.cur_token_name !=';':
			var_type = self.cur_token_name
			self.iterate()
			var_name = self.cur_token_name
			self.symbol_table.add_symbol(var_name,var_type,'local')
			self.iterate()
			self.symbol_table.iterate_num_locals()
		
		# Iterate past ';'
		self.iterate()
		return
		
	def compile_parameter_list(self):
		# Don't write closing paren

		while self.cur_token_name != ')':
			if self.cur_token_name == ',':
				self.iterate()
			param_type = self.cur_token_name
			self.iterate()
			param_name = self.cur_token_name
			self.symbol_table.add_symbol(param_name,param_type,'argument')
			self.iterate()

		return

	def compile_class_var_dec(self):
		# static or field
		field_type = self.cur_token_name
		self.iterate()
		while self.cur_token_name !=';':
			param_type = self.cur_token_name
			self.iterate()
			param_name = self.cur_token_name
			if field_type == 'field':
				pointer_type = 'this'
				# Iterate locals only for non static variables
				self.symbol_table.iterate_num_locals()
			elif field_type == 'static':
				pointer_type = 'static'
			self.symbol_table.add_symbol(param_name,param_type,pointer_type)
			self.iterate()
		# Iterate past ;
		self.iterate()

		return
	
	def parse_statements(self):	
		

		while self.cur_token_name != '}':
			if self.cur_token_name not in self.statement_dict:
				print(self.vm_string)
				print(self.cur_token_name, " Not in statement dict")
				while 1:
					try:
						print(self.cur_token_name)
						self.iterate()
					except:
						sys.exit(1)

			func = self.statement_dict[self.cur_token_name]
			func()
			
		return			

	# Statements
	def letStatement(self):
		
		# write let
		self.iterate()
		# Var Name
		variable_dict = self.symbol_table.get_symbol(self.cur_token_name)
		variable_address = variable_dict['kind'] + ' '  + str(variable_dict['kind_num']) + '\n'
		self.iterate()
		is_array = False


		if self.cur_token_name == '[':
			self.iterate()
			is_array = True
			self.write_expression()
			self.vm_string += 'push ' + variable_address + 'add\n'
			self.iterate()

		
		# equals
		self.iterate()
		# Pop Result of expression on stack to address
		self.write_expression()
		if is_array:
			# pop returned to temp
			self.vm_string += 'pop temp 0\n'
			# pop address to that
			self.vm_string += 'pop pointer 1\n'
			# Put temp into that
			self.vm_string += 'push temp 0\npop that 0\n'
		else:
			self.vm_string += 'pop ' + variable_address
		# EOL
		self.iterate()
		return

	def ifStatement(self):

		# if(
		self.iterate(2)
		# condition
		self.write_expression()
		true_label = self.symbol_table.get_and_iterate_label_counter() + '.TRUE\n'
		false_label = self.symbol_table.get_and_iterate_label_counter() + '.FALSE\n'
		continue_label = self.symbol_table.get_and_iterate_label_counter() + '.CONTINUE\n'

		self.vm_string += 'if-goto ' + true_label
		#){
		self.iterate(2)
		self.vm_string += 'goto ' + false_label
		self.vm_string += 'label ' + true_label
		self.parse_statements()
		# Close bracket
		self.iterate()
		self.vm_string += 'goto ' + continue_label
		# Check for else		
		if self.cur_token_name == 'else':
			#Write else {
			self.iterate(2)
			self.vm_string += 'label ' + false_label
			self.parse_statements()
			# Close bracket
			self.iterate()
			self.vm_string += 'label ' + continue_label
		else:
			self.vm_string = self.vm_string.replace('goto ' + continue_label,'')
			self.vm_string += 'label ' + false_label

		return

	def whileStatement(self):

		# While & first (
		self.iterate(2)
		# Condition & label loop
		loop_label = self.symbol_table.get_and_iterate_label_counter() + '.LOOP\n'
		self.vm_string += 'label ' + loop_label
		self.write_expression()
		# Get label
		continue_label = self.symbol_table.get_and_iterate_label_counter() + '.CONTINUE\n'
		self.vm_string += 'not\nif-goto ' + continue_label
		# ){
		self.iterate(2)
		
		# Statements
		self.parse_statements()
		#Ending labels
		self.vm_string += 'goto ' + loop_label
		self.vm_string += 'label ' + continue_label
		# Close bracket
		self.iterate()
		
		return
	
	def doStatement(self):

		# do keyword
		self.iterate()
		# Write subroutine
		self.look_ahead_func()
		self.write_subroutine_call()
		# semi-colon
		self.iterate()
		# Pop returned 0
		self.vm_string += 'pop temp 0\n'
		return

	def returnStatement(self):
		# Write return
		self.iterate()

		# Write expression
		if self.cur_token_name !=';':
			self.write_expression()
		else:
			# Void function
			self.vm_string += 'push constant 0\n'

		# Write semi-colon
		self.iterate()
		self.vm_string += 'return\n'
		return

	def write_expression(self):
		
		self.write_term()		

		#Add ops as needed
		while self.cur_token_name in OPS_DICT:
			# Store op
			op = OPS_DICT[self.cur_token_name]
			self.iterate()

			# Write next constant
			self.write_term()
			if '.' in op:
				# Account for multiply and divide
				self.vm_string += 'call ' + op + ' 2\n'
			else:
				self.vm_string += op + '\n'
		return
		
	def write_term(self):


		if self.cur_token_name =='(':
			#Iterate past (
			self.iterate()
			self.write_expression()
			# Closing paren
			self.iterate()			
		else:
			self.look_ahead_func()
			# check Unary
			if self.cur_token_name in UNARY_OPS_DICT:
				operator = UNARY_OPS_DICT[self.cur_token_name]
				self.iterate()
				self.write_term()
				self.vm_string += operator + '\n'
			
			# Array
			elif self.look_ahead_token == '[':
				# name[exp]
				variable_dict = self.symbol_table.get_symbol(self.cur_token_name)
				# name[
				self.iterate(2)

				self.write_expression()

				# Error checking for one expression in brackets
				if self.cur_token_name != ']':
					print('long subarray')
					print(self.cur_token_name)
					print(list(self.iterator))
					sys.exit(1)
				
				#Push array name, add and pop to that
				self.vm_string += 'push ' + variable_dict['kind'] + ' '  + str(variable_dict['kind_num']) + '\n'
				self.vm_string += 'add\npop pointer 1\npush that 0\n'
				self.iterate()
			#subroutine
			elif self.look_ahead_token in ['(','.']:
				self.write_subroutine_call()			
			
			# Push item on stack
			else:
				if self.cur_item_type == 'identifier':
					item_dict = self.symbol_table.get_symbol(self.cur_token_name)
					self.vm_string += 'push ' + item_dict['kind'] + ' ' + str(item_dict['kind_num']) + '\n'
				elif self.cur_token_name == 'true':
					self.vm_string += 'push constant 0\nnot\n'
				elif self.cur_token_name == 'false' or self.cur_token_name == 'null':
					self.vm_string += 'push constant 0\n'
				elif self.cur_token_name == 'this':
					self.vm_string += 'push pointer 0\n'
				elif self.cur_item_type == 'stringConstant':
					self.write_string(self.cur_token_name)				
				else:
					self.vm_string += 'push constant ' + self.cur_token_name + '\n'
				
				self.iterate()

		return
	
	def write_string(self,name):
		self.vm_string += 'push constant ' + str(len(name)) +  '\ncall String.new 1\n'	
		for letter in name:
			self.vm_string += 'push constant ' + str(ord(letter)) +  '\ncall String.appendChar 2\n'
		self.iterate()
		return

	def write_expression_list(self):

		expression_counter = 0
		while self.cur_token_name != ')':
			expression_counter += 1
			self.write_expression()
			if self.cur_token_name == ',':
				self.iterate()
		return expression_counter

	def write_subroutine_call(self):

		args = 0 
		if self.look_ahead_token == '(':
						
			# call class function
			subroutine_name = self.symbol_table.get_class_name() + '.' + self.cur_token_name
			self.vm_string += 'push pointer 0\n'
			args += 1
			# Iterate function name and paren
			self.iterate(2)
		elif self.look_ahead_token == '.':
			# Class/local name
			var_dict = self.symbol_table.get_symbol(self.cur_token_name)
			subroutine_name = ''

			# If current class keep name else, find class name
			if var_dict == False:
				subroutine_name = self.cur_token_name
				self.iterate()
			else:
				# Existing variable, push
				self.vm_string += 'push ' + var_dict['kind'] + ' ' + str(var_dict['kind_num']) + '\n'
				args += 1
				subroutine_name = var_dict['type']
				self.iterate()
			# iterate  . , function name
			for x in range(2):
				subroutine_name += self.cur_token_name
				self.iterate()
			

			# Pass paren
			self.iterate()	
		else:
			# Error checking
			print(self.xml_string)
			print(self.cur_token_name,'Not a subroutine')
			sys.exit(1)
		if self.cur_item_type == 'stringConstant':
			self.write_string(self.cur_token_name)
			self.iterate()
			self.vm_string += 'call ' + subroutine_name + ' 1\n'
			return

		# Place arguments
		args += self.write_expression_list()
		self.vm_string += 'call ' + subroutine_name + ' ' + str(args) + '\n'
		# Closing paren
		self.iterate()
		
		return

	# Writing functions
	def look_ahead_func(self):
		'''
		Looks ahead and stores next iterator values without updating current
		'''
		self.look_ahead_token, self.look_ahead_type = next(self.iterator)
		self.look_ahead = True
		return

	def iterate(self,n=1):
		'''
		iterate n times, clearing look ahead if needed
		'''
		if self.look_ahead:
			self.cur_token_name = self.look_ahead_token
			self.cur_item_type = self.look_ahead_type
			self.look_ahead = False
			if n > 1:
				for x in range(n-1):
					self.cur_token_name, self.cur_item_type = next(self.iterator)
		else:
			for x in range(n):
				self.cur_token_name, self.cur_item_type = next(self.iterator)
		return

	def get_vm_list(self,class_name):
		
		if self.xml_string == '':
			self.compile_class()
			return self.vm_string
		else:
			return self.vm_string

if __name__ == '__main__':
	
	args = sys.argv
	if len(args) != 2:
		print("Usage: python parse_to_xml.py FILENAME or DIRECTORY")
		sys.exit(1)

	t = Tokenizer()
	
	read_files, write_files = t.prep_file_list(args)
	

	for i in range(len(read_files)):
		with open(write_files[i],'w') as write_f:
			# Write a string from the tokenizer passed through the Compilation engine
			write_f.write(t.string_from_file(read_files[i],write_files[i]))


				




