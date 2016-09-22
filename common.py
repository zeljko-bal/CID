
def element_type(element):
	return element.__class__.__name__
	
def parent_command(element):
	parent = element.parent
	while element_type(parent) != 'Command':
		if element_type(parent) == 'Script':
			return None
		parent = parent.parent
	return parent
	
def all_parent_commands(element):
	parent = parent_command(element)
	ret = []
	while parent:
		ret.append(parent)
		parent = parent_command(parent)
	return ret

def get_cli_pattern_count(pattern):
	if element_type(pattern) == 'StringParamPattern':
		if pattern.count_many:
			return '*'
		elif pattern.count:
			return pattern.count
		elif pattern.vars:
			return len(pattern.vars)
	return 1
		
def element_id(element_name, parents=[]):
	return '/'+'/'.join(parents+[element_name])
	
class ElementExtractor():
	def __init__(self):
		self.all_commands = []
		self.all_parameters = []
		self.extract_command = lambda c: self.all_commands.append(c)
		self.extract_parameter = lambda p: self.all_parameters.append(p)
		self.visitor = {'Command':self.extract_command, 'Parameter':self.extract_parameter}
	