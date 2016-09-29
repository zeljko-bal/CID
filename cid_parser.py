
from textx.metamodel import metamodel_from_file

from model_processor import ModelProcessor, ProcessorInvoker
from common import *

invoker = ProcessorInvoker()

class CliOptionalGroup:
	def __init__(self, parent, elements):
		self.parent = parent
		self.elements = elements
		
class CliStructure:
	def __init__(self, parent, elements, has_options, has_subcommand):
		self.parent = parent
		self.elements = elements
		self.has_options = has_options
		self.has_subcommand = has_subcommand

# ------------------------------- HELPER FUNCTIONS -------------------------------

def contains_duplicate_names(lst):
	defined = [e.name for e in lst if not hasattr(e, 'imported') and not hasattr(e, 'local')]
	local = [e.local for e in lst if hasattr(e, 'local') and e.local]
	imported = [e.imported for e in lst if hasattr(e, 'imported') and e.imported]
	
	return len(defined) != len(set(defined)) or len(local) != len(set(local)) or len(imported) != len(set(imported))
	
def split_import_path(import_path):
	return '/'.join(import_path.elements[:-1])+'.cid', import_path.elements[-1]
	
def import_reference_path(ref):
	return '/'+'/'.join(ref.elements)
	
# ------------------------------- FIRST PASS -------------------------------

def process_script(script):
	# check for duplicate free parameter names
	script.free_parameters = [p for p in script.elements if element_type(p) == 'Parameter']
	if contains_duplicate_names(script.free_parameters):
		raise Exception('same_name_params_check')
	
	# check for duplicate free command names
	script.free_commands = [p for p in script.elements if element_type(p) == 'Command']
	if contains_duplicate_names(script.free_commands):
		raise Exception('same_name_commands_check')
		
	# check for duplicate import paths
	if len(script.imports) != len(set([imp.path for imp in script.imports])):
		raise Exception('duplicate path in imports')
		
	# check for duplicate import aliases
	if len(script.imports) != len(set([imp.alias for imp in script.imports])):
		raise Exception('duplicate alias in imports')

# -------------------------------

def process_import_statement(import_statement):
	if not import_statement.alias:
		import_statement.alias = import_statement.path
	
	import_statement.alias = import_reference_path(import_statement.alias)
	import_statement.file_path, import_statement.element_name = split_import_path(import_statement.path)

# -------------------------------

def process_import_reference(import_reference):
	if import_reference.imported:
		import_reference.imported = import_reference_path(import_reference.imported)
		
# -------------------------------

class CommandProcessor:
	def __init__(self):
		self.all_defined_commands = []
		
	@invoker.processor(type='Command', name='process_command', attrs=[], adds=[], dels=['command.usage'], requires=[])
	def process_command(self, command):
		self.transform(command)
		self.defaults(command)
		self.check(command)
		self.all_defined_commands.append(command)
	
	# command.usages = all usages
	# del command.usage
	def transform(self, command):
		# transform multiline usages
		if command.usages:
			command.usages = [usage.body for usage in command.usages]
		elif command.usage:
			command.usages = [command.usage]
			del command.usage
		
	def defaults(self, command):
		if not command.title:
			command.title = command.name.replace('_', ' ').replace('-', ' ').strip().title()
	
	def check(self, command):
		if contains_duplicate_names(command.parameters):
			raise Exception('same_name_params_check')
			
		if contains_duplicate_names(command.sub_commands):
			raise Exception('same_name_commands_check')
			
		if command.type == 'Cmd' and element_type(command.parent) != 'Script':
			print('Warning: command {} of type Cmd found as a sub command.'.format(command.name))
	
# -------------------------------


		
		
		
		

class ParameterProcessor:
	def __init__(self, imported_prefixes=[]):
		self.all_defined_parameters = []
		
	def process_parameter(self, parameter):
		self.transform(parameter)
		self.defaults(parameter)
		self.check(parameter)
		self.all_defined_parameters.append(parameter)
	
	def transform(self, parameter):
		'''
		add parameter.nonpositional
		fix parameter.default
		add parameter.all_patterns
		add parameter.cli_pattern_vars
		add parameter.cli_pattern_count
		del parameter.empty_str_disallowed
		add parameter.none_allowed
		'''
		# set parameter.nonpositional
		parameter.nonpositional = parameter.cli and parameter.cli.cli_pattern
		
		# fix parameter.default model structure
		if len(parameter.default) == 1:
			parameter.default = parameter.default[0]
		
		if parameter.nonpositional:
			# set parameter.all_patterns 
			parameter.cli.cli_pattern.parent = parameter
			parameter.all_patterns = [parameter.cli.cli_pattern]+parameter.cli_aliases
			
			# set parameter.cli_pattern_vars
			for pattern in parameter.all_patterns:
				if hasattr(pattern, 'vars') and pattern.vars:
					pattern.vars = [v.value for v in pattern.vars]
					
					if not hasattr(parameter, 'cli_pattern_vars'):
						parameter.cli_pattern_vars = pattern.vars
			
			# set parameter.cli_pattern_count
			parameter.cli_pattern_count = get_cli_pattern_count(parameter.all_patterns[0])
			
			# del parameter.empty_str_disallowed
			if (parameter.empty_str_allowed or parameter.empty_str_disallowed) and parameter.type != 'Str':
				raise Exception("empty_str_allowed or empty_str_disallowed in non Str")
			
			if parameter.default == '' and parameter.empty_str_disallowed:
				raise Exception("parameter.empty_str_disallowed and parameter.default == ''")
			
			# add parameter.none_allowed
			if parameter.type == 'Bool':
				parameter.none_allowed = [p for p in parameter.all_patterns if p.positive] and [p for p in parameter.all_patterns if p.negative]
			else:
				parameter.none_allowed = True
			
			del parameter.empty_str_disallowed
		
	def defaults(self, parameter):
		if not parameter.title:
			parameter.title = parameter.name.replace('_', ' ').replace('-', ' ').strip().title()
			
		if not parameter.multiplicity:
			parameter.multiplicity = 1
			
		if not parameter.description:
			parameter.description = '{default_desc}'
		
		if not parameter.default:
			if parameter.default_is_none:
				parameter.default = None
			else:
				if parameter.type == 'Bool':
					# if parameter doesnt contain both positive and negative patterns
					if not ([p for p in parameter.all_patterns if p.positive] and [p for p in parameter.all_patterns if p.negative]):
						# set to False by default
						parameter.default = 'False'
					# else: leave None (for a case where neither positive nor negative arg is provided)
			
		if parameter.default == '':
			parameter.empty_str_allowed = True
			
		if parameter.nonpositional and not parameter.default_is_none and not isinstance(parameter.default, list):
			if parameter.cli_pattern_count not in [1, '*']:
				parameter.default = [parameter.default]*parameter.cli_pattern_count
			
		if not parameter.date_format and parameter.type == 'Date':
			parameter.date_format = "%d.%m.%Y"
	
	def check(self, parameter):
		if parameter.choices and not parameter.type == 'Choice':
			raise Exception('choices in not Choice parameter: {}'.format(parameter.name))
		
		if element_type(parameter) == 'Choice' and not parameter.choices:
			raise Exception('choices required in Choice')
		
		for constraint in parameter.constraints:
			supported_constraints = {
			 'Str':[],
			 'Choice':[],
			 'Num':[],
			}[element_type(parameter)]
			if constraint.type not in supported_constraints:
				raise Exception('constraint.type unsupported')
			
		if parameter.default_is_none and parameter.default:
			raise Exception('parameter.default_is_none and parameter.default')
			
		if parameter.type == 'Bool' and parameter.default and parameter.default.lower() not in ['true', 'false']:
			raise Exception("parameter.default not true or false and parameter.type == Bool")
			
		if not parameter.multiplicity == '*' and parameter.multiplicity <= 0:
			raise Exception("Multiplicity must be greater than zero: {param}.".format(param=parameter.name))
		
		if not parameter.nonpositional and parameter.multiplicity not in [1, '*']:
			raise Exception("Multiplicity for positional parameters must be either 1 or '*': {param}.".format(param=parameter.name))
			
		if not parameter.multiplicity == 1 and parameter.type == "Bool":
			raise Exception("Multiplicity for Bool type parameters must be 1: {param}.".format(param=parameter.name))
			
		# requires [nonpositional, cli_pattern_count, all_patterns, cli_pattern_vars]
		if parameter.nonpositional:
			if parameter.cli_pattern_count not in [1, '*'] and len(parameter.default) != parameter.cli_pattern_count:
				raise Exception("Parameter pattern count and default values count do not match.")
			for pattern in parameter.all_patterns:
				if element_type(pattern) == "StringParamPattern":
					if parameter.type == "Bool":
						raise Exception('Non boolean cli pattern in Bool type parameter: {param}.'.format(param=parameter.name))
					if pattern.count_char and not parameter.type == "Num":
						raise Exception('Counter pattern in non Num type parameter: {param}.'.format(param=parameter.name))
					if parameter.cli_pattern_count != get_cli_pattern_count(pattern):
						raise Exception('Different parameter count values encountered in cli patterns for parameter: {param}'.format(param=parameter.name))
					if pattern.vars:
						if not (len(parameter.cli_pattern_vars) == len(pattern.vars) and 
								all([parameter.cli_pattern_vars[i] == pattern.vars[i] for i in range(0,len(pattern.vars))])):
							raise Exception("Different argument names found for patterns in parameter: {}".format(parameter.name))
				elif element_type(pattern) in ['BoolWithPositivePattern', 'BoolNegativeOnlyPattern'] and not parameter.type == "Bool":
					raise Exception('Boolean cli pattern in non Bool type parameter: {param}.'.format(param=parameter.name))
		
# -------------------------------

def process_cli_or_group(or_group):
	or_group.lhs = or_group.lhs[0]
	or_group.rhs = or_group.rhs[0]
	
	# transform the tree structure into a list
	or_group.elements = [or_group.lhs]
	
	if element_type(or_group.rhs) == 'CliOrGroup':
		or_group.elements += or_group.rhs.elements
		for el in or_group.rhs.elements:
			el.parent = or_group
	else:
		or_group.elements.append(or_group.rhs)
	del or_group.lhs
	del or_group.rhs
	
	# check for CliOptionalGroup in CliOrGroup
	for element in or_group.elements:
		if element_type(element) == 'CliOptionalGroup':
			print('warning: CliOptionalGroup in or_group')

# ------------------------------- SECOND PASS -------------------------------

class ReferenceResolver:
	def __init__(self, parameter_instances, command_instances, imports):
		self.parameter_instances = parameter_instances
		self.command_instances = command_instances
		self.import_paths = {_import.alias:(_import.file_path, _import.element_name) for _import in imports}
		self.imported_models = {file_path:parse('./'+file_path) for _, (file_path, _) in self.import_paths.items()}
		
		self.visitor = {'ParameterReference':self.resolve_parameter_reference, 'CommandReference':self.resolve_command_reference}
	
	def resolve_parameter_reference(self, parameter_reference):
		if parameter_reference.local:
			for instance in self.parameter_instances:
				if instance.name == parameter_reference.local:
					# if the instance is defined as a free parameter or in the enclosing command
					if element_type(instance.parent) == 'Script' or instance.parent.name == parent_command(parameter_reference).name:
						# replace the reference with the actual instance
						self.replace_parameter_reference(parameter_reference, instance)
						return
			else:
				raise Exception("Unresolved local reference: {}".format(parameter_reference.local))
		else:
			if parameter_reference.imported not in self.import_paths:
				raise Exception("Unresolved imported reference: {}".format(parameter_reference.imported))
			file_path, el_name = self.import_paths[parameter_reference.imported]
			imported_model = self.imported_models[file_path]
			for instance in imported_model.elements:
				if element_type(instance) == 'Parameter' and instance.name == el_name:
					# check for name collision
					for resolved in [p for p in parent_command(parameter_reference).parameters if element_type(p) == 'Parameter']:
						if resolved.name == el_name and resolved is not instance:
							raise Exception('Parameter name collision between {cmd}.{param} and an imported parameter from {path}.'.format(cmd=parent_command(parameter_reference).name, param=el_name, path=file_path))
					# replace the reference with the actual instance
					self.replace_parameter_reference(parameter_reference, instance)
					return
			else:
				raise Exception("Unresolved imported reference: {}".format(parameter_reference.imported))
			
	def resolve_command_reference(self, command_reference):
		if command_reference.local:
			for instance in self.command_instances:
				if instance.name == command_reference.local:
					# if the instance is defined as a free command or in the enclosing command
					if element_type(instance.parent) == 'Script' or instance.parent.name == parent_command(command_reference).name:
						# replace the reference with the actual instance
						self.replace_command_reference(command_reference, instance)
						return
			else:
				raise Exception("Unresolved local reference: {}".format(command_reference.local))
		else:
			if parameter_reference.imported not in self.import_paths:
				raise Exception("Unresolved imported reference: {}".format(parameter_reference.imported))
			file_path, el_name = self.import_paths[command_reference.imported]
			if el_name in [c.name for c in command_reference.parent.sub_commands]:
				raise Exception('Command name collision between {cmd}.{subcmd} and an imported command from {path}.'.format(cmd=parameter_reference.parent.name, subcmd=el_name, path=file_path))
			imported_model = self.imported_models[file_path]
			for instance in imported_model.elements:
				if element_type(instance) == 'Command' and instance.name == el_name:
					# replace the reference with the actual instance
					self.replace_command_reference(command_reference, instance)
					return
			else:
				raise Exception("Unresolved imported reference: {}".format(parameter_reference.imported))
			
	def replace_parameter_reference(self, parameter_reference, instance):
		if hasattr(parameter_reference.parent, 'parameters'):
			idx = parameter_reference.parent.parameters.index(parameter_reference)
			parameter_reference.parent.parameters[idx] = instance
		elif hasattr(parameter_reference.parent, 'elements'):
			idx = parameter_reference.parent.elements.index(parameter_reference)
			parameter_reference.parent.elements[idx] = instance
		else:
			raise Exception("Internal error: ReferenceResolver.replace_parameter_reference: wrong parent type.")
			
	def replace_command_reference(command_reference, instance):
		idx = command_reference.parent.sub_commands.index(command_reference)
		command_reference.parent.sub_commands[idx] = instance
	
# -------------------------------

def add_id(element):
	element.id = element_id(element.name, [e.name for e in all_parent_commands(element)])
	
# -------------------------------

def set_usage_defaults(command):
	if not command.usages:
		default_usage = CliStructure(command, sorted([p for p in command.parameters if not p.nonpositional], key=lambda p: 0 if p.multiplicity != '*' else 1),
									has_options=True, has_subcommand=False)
		command.usages = [default_usage]
		
	if command.sub_commands and all([not usage.has_subcommand for usage in command.usages]):
		for usage in command.usages:
			usage.has_subcommand = True

# -------------------------------	

def gather_usage_sub_elements(cli_element, parents):
	if not hasattr(cli_element, 'sub_elements'):
		cli_element.sub_elements = set()
	
	for group_element in cli_element.elements:
		if hasattr(group_element, 'sub_elements'):
			if not cli_element.sub_elements.isdisjoint(group_element.sub_elements) and not element_type(cli_element) == 'CliOrGroup':
				raise Exception('duplicate element in usage')
			cli_element.sub_elements.update(group_element.sub_elements)
		elif element_type(group_element) == 'Parameter':
			if group_element in cli_element.sub_elements and not element_type(cli_element) == 'CliOrGroup':
				raise Exception('duplicate element {} in usage for command: {}'.format(group_element.name, [p.name for p in parents if element_type(p) == 'Command']))
			cli_element.sub_elements.add(group_element)
		elif  element_type(group_element) == 'CliSeparator':
			if hasattr(cli_element, 'has_cli_separator'):
				raise Exception('Duplicate argument separator.')
			cli_element.has_cli_separator = True

_gather_usage_sub_elements_visitor = {'CliStructure':gather_usage_sub_elements, 'CliGroup':gather_usage_sub_elements, 'CliOptionalGroup':gather_usage_sub_elements, 'CliOrGroup':gather_usage_sub_elements}

# -------------------------------

def gather_gui_group_sub_elements(gui_group):
	gui_group.sub_elements = set()
	
	for element in gui_group.elements:
		if hasattr(element, 'sub_elements'):
			if element_type(gui_group) != 'GuiSectionGroup' or not gui_group.exclusive:
				if not gui_group.sub_elements.isdisjoint(element.sub_elements):
					raise Exception('duplicate element in gui structure')
			gui_group.sub_elements.update(element.sub_elements)
		elif element_type(element) == 'Parameter':
			if element in gui_group.sub_elements:
				raise Exception('duplicate element in gui structure')
			gui_group.sub_elements.add(element)

def gather_gui_element_sub_elements(gui_element):
	gui_element.sub_elements = gui_element.body.sub_elements
	
_gather_gui_sub_elements_visitor = {
	'GuiStructure':gather_gui_group_sub_elements,
	'GuiTabs':gather_gui_group_sub_elements,
	'GuiSectionGroup':gather_gui_group_sub_elements,
	'GuiSection':gather_gui_element_sub_elements,
	'GuiGrid':gather_gui_group_sub_elements,
	'GuiTab':gather_gui_element_sub_elements,
	'GuiGridRow':gather_gui_group_sub_elements,
	'GuiGridCell':gather_gui_element_sub_elements,
}

# -------------------------------

def expand_options_shortcut(command):
	for usage in command.usages:
		if usage.has_options:
			options = [p for p in command.parameters if p.nonpositional and p not in usage.sub_elements]
			usage.elements = [CliOptionalGroup(usage, [p]) for p in options] + usage.elements
			usage.sub_elements = set(options).union(usage.sub_elements)

# -------------------------------
	
def validate_command(command, parents):
	script = parents[0]
	for parameter in command.parameters:
		if parameter.name in [p.name for p in script.free_parameters] and not parameter in script.free_parameters:
			raise Exception('Parameter name collision between {cmd}.{param} and a top level free parameter.'.format(cmd=command.name, param=parameter.name))
			
		if parameter.default_is_none:
			if all([is_parameter_required(parameter, u) for u in command.usages]):
				print('Warning: parameter.default == None and parameter is required in all usage patterns.')
	
	for sub_command in command.sub_commands:
		if sub_command.name in [c.name for c in script.free_commands] and not sub_command in script.free_commands:
			raise Exception('Command name collision between {cmd}.{sub} and a top level free command.'.format(cmd=command.name, sub=sub_command.name))
			
	parameter_declaration_check(command)
				
def is_parameter_required(parameter, usage):
	if hasattr(usage, 'elements'):
		if parameter not in usage.sub_elements:
			return False
		for element in usage.elements:
			if element is parameter:
				return True
			if element_type(element) == 'CliGroup':
				if is_parameter_required(parameter, element):
					return True
			if element_type(element) == 'CliOrGroup':
				if all([is_parameter_required(parameter, el) for el in element.elements]):
					return True
	return False
	
def parameter_declaration_check(command):
	if command.gui:
		declared_names = [p.name for p in command.parameters]
		for element in command.gui.sub_elements:
			if element.name not in declared_names:
				raise Exception('Undeclared parameter: {param} in command gui struture: {cmd}.'.format(param=element.name, cmd=command.name))
	
	usage_sub_elements = set()
	for usage in command.usages:
		usage_sub_elements.update(usage.sub_elements)
	
	declared_names = [p.name for p in command.parameters]
	for element in usage_sub_elements:
		if element.name not in declared_names:
			raise Exception('Undeclared parameter: {param} in command: {cmd}.'.format(param=element.name, cmd=command.name))
			
	all_sub_elements = usage_sub_elements
	if command.gui:
		all_sub_elements.update(command.gui.sub_elements)
		
	for parameter in command.parameters:
		if parameter not in all_sub_elements:
			print("Warning: parameter {} declared, but not referenced in command: {}.".format(parameter.name, command.id))

# ------------------------------- PARSER FUNCTIONS -------------------------------

def parse(script_path):
	
	metamodel = metamodel_from_file('cid_grammar.tx')
	
	# first pass ---------------------
	
	command_processor = CommandProcessor()
	parameter_processor = ParameterProcessor()
	
	metamodel.register_obj_processors({
		'Script':process_script,
		'ImportStatement':process_import_statement,
		'ParameterReference':process_import_reference,
		'CommandReference':process_import_reference,
		'Command':command_processor.process_command,
		'Parameter':parameter_processor.process_parameter,
		'CliOrGroup':process_cli_or_group,
	})
	
	model = metamodel.model_from_file(script_path)
	
	all_defined_commands = command_processor.all_defined_commands
	all_defined_parameters = parameter_processor.all_defined_parameters
	
	# dereferencing ---------------------
	
	ModelProcessor(ReferenceResolver(all_defined_parameters, all_defined_commands, model.imports).visitor).process_model(model)
	
	# second pass ---------------------
	
	ModelProcessor({'Command':add_id, 'Parameter':add_id}).process_model(model)
	ModelProcessor({'Command':set_usage_defaults}).process_model(model)
	ModelProcessor(_gather_usage_sub_elements_visitor).process_model(model)
	ModelProcessor(_gather_gui_sub_elements_visitor).process_model(model)
	ModelProcessor({'Command':expand_options_shortcut}).process_model(model)
	ModelProcessor({'Command':validate_command}).process_model(model)
	
	return model
	
	
# logicke checkove u defaults i transform, dodatne u check []