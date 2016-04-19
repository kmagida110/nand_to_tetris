import sys

if __name__ == '__main__':
	
	#Check that script is called appropriately
	if len(sys.argv) < 2:
		print "Usage: python strip_white_space.py FILENAME (no-comments)"
		exit(1)

	input_filename = sys.argv[1]

	# Check for remove comments
	if len(sys.argv) > 2:
		if sys.argv[2] == 'no-comments':
			remove_comments = True
		else:
			print "Usage: python strip_white_space.py FILENAME no-comments, unknown parameter in place of no-comments"
			print "Comments will not be stripped"
			remove_comments = False
	else:
		remove_comments = False

	#Get name of output file and open for writing
	output_file = input_filename[:input_filename.rfind('.')] + '.out'
	out = open(output_file,'w')

	#Loop over input file and write to output file
	with open(input_filename,'rU') as input_file:
		# Remove all data following //
		for full_line in input_file:
			if remove_comments:
				full_line = full_line.split('//')[0]

			# Read line and replace spaces and tabs
			reduced_line = full_line.replace(' ','').replace('\t','')

			# Only add rows with text, covers comment lines and initally blank lines
			if reduced_line != '\n':
				out.write(reduced_line)

	out.close()

		











