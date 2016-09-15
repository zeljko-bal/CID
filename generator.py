
from textx.metamodel import metamodel_from_file
from jinja2 import Environment, FileSystemLoader
from collections import namedtuple, defaultdict
from modelprinter import print_model
from functools import reduce
from inspect import getfullargspec
from types import MethodType, BuiltinMethodType
import textwrap

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
	
def rightmost_positional_elements(element):
	if hasattr(element, 'elements'):
		if element_type(element) == 'CliOrGroup':
			ret = []
			for or_el in element:
				rightmost = rightmost_positional_elements(or_el)
				if rightmost:
					ret += rightmost
			return ret
		else:
			if element.elements:
				for i in reversed(range(0, len(element.elements))):
					rightmost = rightmost_positional_elements(element.elements[i])
					if rightmost:
						return rightmost
	elif element_type(element) == 'Parameter' and not element.nonpositional:
		return [element]
	
	return []

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

def process_import_statement(import_statement):
	if not import_statement.alias:
		import_statement.alias = import_statement.path
	
	import_statement.alias = import_reference_path(import_statement.alias)
	import_statement.file_path, import_statement.element_name = split_import_path(import_statement.path)
	
def process_import_reference(import_reference):
	if import_reference.imported:
		import_reference.imported = import_reference_path(import_reference.imported)

class CommandProcessor:
	def __init__(self):
		self.all_defined_commands = []
		
	def process_command(self, command):
		self.transform(command)
		self.defaults(command)
		self.check(command)
		self.all_defined_commands.append(command)

	def transform(self, command):
		# transform multiline usages
		if command.usages:
			command.usages = [usage.body for usage in command.usages]
		elif command.usage:
			command.usages = [command.usage]
			del command.usage
		
	def defaults(self, command):
		if not command.cli_command:
			command.cli_command = command.name
		
		if not command.title:
			command.title = command.name.replace('_', ' ').replace('-', ' ').strip().title()
	
	def check(self, command):
		if contains_duplicate_names(command.parameters):
			raise Exception('same_name_params_check')
			
		if contains_duplicate_names(command.sub_commands):
			raise Exception('same_name_commands_check')
		
class ParameterProcessor:
	def __init__(self, imported_prefixes=[]):
		self.all_prefixes = imported_prefixes
		self.all_defined_parameters = []
		
	def process_parameter(self, parameter):
		self.transform(parameter)
		self.defaults(parameter)
		self.check(parameter)
		self.all_defined_parameters.append(parameter)
		
	def transform(self, parameter):
		# set parameter.nonpositional
		parameter.nonpositional = parameter.cli and parameter.cli.cli_pattern
		
		# fill parameter.prefixes, parameter.pos_prefixes, parameter.neg_prefixes, parameter.all_patterns
		if parameter.nonpositional:
			parameter.all_patterns = [parameter.cli.cli_pattern]+parameter.cli_aliases
			str_patterns = [p for p in parameter.all_patterns if element_type(p) == 'StringParamPattern']
			pos_patterns = [p for p in parameter.all_patterns if element_type(p) in ['BoolWithPositivePattern', 'BoolNegativeOnlyPattern'] and p.positive]
			neg_patterns = [p for p in parameter.all_patterns if element_type(p) in ['BoolWithPositivePattern', 'BoolNegativeOnlyPattern'] and p.negative]
			
			if parameter.type == 'Bool':
				parameter.pos_prefixes = [p.positive for p in pos_patterns]
				parameter.neg_prefixes = [p.negative for p in neg_patterns]
				parameter.prefixes = parameter.pos_prefixes+parameter.neg_prefixes
			else:
				parameter.prefixes = [p.prefix for p in str_patterns]
			
			for prefix in parameter.prefixes:
				if prefix in self.all_prefixes:
					raise Exception('duplicate prefixes')
				self.all_prefixes.append(prefix)
		
		# fill parameter.usage_repr
		if parameter.nonpositional:
			if pos_patterns:
				repr_pattern = max(pos_patterns, key=lambda p: len(p.positive)) # longest positive
				parameter.usage_repr, _ = cli_pattern_repr(repr_pattern)
			elif neg_patterns:
				repr_pattern = max(neg_patterns, key=lambda p: len(p.negative)) # longest negative
				_, parameter.usage_repr = cli_pattern_repr(repr_pattern)
			elif str_patterns:
				repr_pattern = max(str_patterns, key=lambda p: len(p.prefix)) # longest prefix
				parameter.usage_repr = cli_pattern_repr(repr_pattern)
		else:
			parameter.usage_repr = "<{name}>{mult}".format(name=parameter.name.upper(), mult='...' if parameter.multiplicity == '*' else '')
		
	def defaults(self, parameter):
		if not parameter.title:
			parameter.title = parameter.name.replace('_', ' ').replace('-', ' ').strip().title()
			
		if not parameter.multiplicity:
			parameter.multiplicity = 1
			
		if not parameter.description:
			parameter.description = '{default_desc}'
		
		if '{default_desc}' in parameter.description:
			pretty_type = {
				 "Str":"String",
				 "Num":"Number",
				 "Bool":"Boolean",
				 "Date":"Date",
				 "File":"File",
				 "Choice":"Choice",
			}[parameter.type]
			default_description = "Data type: {}.".format(pretty_type)
			if parameter.default:
				default_description += " Default value: {}.".format("'{}'".format(parameter.default) if isinstance(parameter.default, str) else parameter.default)
			if parameter.type == 'Bool' and parameter.neg_prefixes:
				if parameter.pos_prefixes:
					default_description += " Parameters: {} represent True.".format(', '.join(parameter.pos_prefixes))
				default_description += " Parameters: {} represent False.".format(', '.join(parameter.neg_prefixes))
			if parameter.choices:
				default_description += " Choices: {}".format(parameter.choices)
			if parameter.date_format:
				default_description += " Date format: {}".format(parameter.date_format)
			if parameter.multiplicity != 1:
				if parameter.multiplicity == '*':
					default_description += " This parameter can appear an unlimited amount of times."
				else:
					default_description += " This parameter can appear at most {} times.".format(parameter.multiplicity)
			
			parameter.description = parameter.description.format(default_desc=default_description)
		
		if not parameter.default and not parameter.default_is_none:
			parameter.default = {
				"Str":"",
				"Num":0,
				"Bool":False,
				"Date":"",
				"File":".",
				"Choice":parameter.choices[0] if parameter.choices else None,
			}[parameter.type]
		
		if not parameter.none_value_allowed:
			parameter.none_value_allowed = 'Disallowed' if parameter.default is not None else 'Allowed'
			
		if not parameter.date_format and parameter.type == 'Date':
			parameter.date_format = "%d.%m.%Y"
		
	def check(self, parameter):
		if parameter.widget:
			supported_widgets = {
			 'Str':['password', 'text_field', 'text_area'],
			 'Choice':['dropdown', 'radio_buttons'],
			 'Num':['counter', 'slider'],
			}[element_type(parameter)]
			if parameter.widget not in supported_widgets:
				raise Exception('parameter.widget unsupported')
		
		if parameter.choices and not element_type(parameter) == 'Choice':
			raise Exception('choices in not Choice')
		
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
		
		if not parameter.none_value_allowed == 'Allowed' and parameter.default == 'None':
			raise Exception("parameter.none value disallowed and parameter.default == 'None'.")
			
		if parameter.default_is_none and parameter.default:
			raise Exception('parameter.default_is_none and parameter.default')
					
		if not parameter.multiplicity == '*' and parameter.multiplicity <= 0:
			raise Exception("Multiplicity must be greater than zero: {param}.".format(param=parameter.name))
		
		if not parameter.nonpositional and parameter.multiplicity not in [1, '*']:
			raise Exception("Multiplicity for positional parameters must be either 1 or '*': {param}.".format(param=parameter.name))
			
		if not parameter.multiplicity == 1 and parameter.type == "Bool":
			raise Exception("Multiplicity for Bool type parameters must be 1: {param}.".format(param=parameter.name))
			
		if parameter.nonpositional:
			count = None
			def get_count_value(pattern):
				if pattern.count_many:
					return '*'
				elif pattern.count:
					return pattern.count
				elif pattern.vars:
					return len(pattern.vars)
			
			for pattern in parameter.all_patterns:
				if element_type(pattern) == "StringParamPattern":
					if parameter.type == "Bool":
						raise Exception('Non boolean cli pattern in Bool type parameter: {param}.'.format(param=parameter.name))
					if pattern.count_char and not parameter.type == "Num":
						raise Exception('Counter pattern in non Num type parameter: {param}.'.format(param=parameter.name))
					if count and count != get_count_value(pattern):
						raise Exception('Different parameter count values encountered in cli patterns for parameter: {param}'.format(param=parameter.name))
					else:
						count = get_count_value(pattern)
				elif not parameter.type == "Bool":
					raise Exception('Boolean cli pattern in non Bool type parameter: {param}.'.format(param=parameter.name))
		
def cli_pattern_repr(pattern):
	if element_type(pattern) == 'StringParamPattern':
		if pattern.count_char:
			return '{pref}{count_char}'.format(pref=pattern.prefix, count_char=pattern.count_char)
		else:
			if pattern.vars:
				type_str = ' '.join(pattern.vars)
			else:
				type_str = pattern.parent.type if hasattr(pattern.parent, 'type') else pattern.parent.parent.type
			if pattern.count:
				type_str = ' '.join([type_str]*pattern.count)
			if pattern.count_many:
				if pattern.separator:
					count_repr = '...[{separator}]'.format(separator=pattern.separator)
				else:
					count_repr  = '...'
			else:
				count_repr = ''
			return '{pref}{space}<{type}{count}>'.format(pref=pattern.prefix, space=pattern.white_space*' ', type=type_str.upper(), count=count_repr)
	else:
		if pattern.positive and pattern.negative:
			return pattern.positive, pattern.negative
		elif pattern.positive:
			return pattern.positive, None
		elif pattern.negative:
			return None, pattern.negative
			
def process_cli_or_group(or_group):
	# transform the tree structure into a list
	or_group.elements = [or_group.lhs[0]]
	
	if element_type(or_group.rhs[0]) == 'CliOrGroup':
		or_group.elements += or_group.rhs[0].elements
	else:
		or_group.elements.append(or_group.rhs[0])
	del or_group.lhs
	del or_group.rhs
	
	# moze i drugi pass TODO, da ne ispisuje i za importovane skripte ako se komanda ne koristi
	# check for CliOptionalGroup in CliOrGroup
	for element in or_group.elements:
		if element_type(element) == 'CliOptionalGroup':
			print('warning: CliOptionalGroup in or_group')
			
def process_cli_separator(cli_separator):
	cli_separator.value = cli_separator.value[0]
	cli_separator.usage_repr = cli_separator.value
	cmd = parent_command(cli_separator)
	if not hasattr(cmd, 'cli_separators'):
		cmd.cli_separators = []
	cmd.cli_separators.append(cli_separator.value)
	
def process_string_param_pattern(pattern):
	if pattern.vars:
		pattern.vars = [v.value for v in pattern.vars]

# ------------------------------- ModelProcessor -------------------------------

class ModelProcessor:
	def __init__(self, callbacks, allow_revisiting=False):
		if isinstance(callbacks, list):
			self.callbacks = callbacks[0]
			for cb in callbacks[1:]:
				for key, value in cb.items():
					if key in self.callbacks:
						existing = self.callbacks[key]
						if isinstance(existing, list):
							existing.append(value)
						else:
							existing = [existing, value]
					else:
						self.callbacks[key] = value
		else:
			self.callbacks = callbacks
		self.allow_revisiting = allow_revisiting
		self.parent_stack = []
		self.visited = []
		
	def invoke(self, element):
		if not self.allow_revisiting and element in self.visited:
			return
		callback_container = self.callbacks.get(element_type(element))
		if callback_container:
			callbacks = callback_container if isinstance(callback_container, list) else [callback_container]
			for callback in callbacks:
				args_count = len(getfullargspec(callback).args)
				if isinstance(callback, (MethodType, BuiltinMethodType)):
					args_count -= 1
				if args_count == 1:
					callback(element)
				else:
					callback(element, self.parent_stack)
			self.visited.append(element)
	
	def process_model(self, model):
		self.parent_stack.append(model)
		for import_statement in model.imports:
			self.invoke(import_statement)
		for element in model.elements:
			if element_type(element) == 'Parameter':
				self.process_parameter(element)
			elif element_type(element) == 'Command':
				self.process_command(element)
		self.parent_stack.pop()
		self.invoke(model)
		
	def process_parameter(self, parameter):
		self.parent_stack.append(parameter)
		for choice in parameter.choices:
			self.invoke(choice)
		if parameter.cli:
			if parameter.cli.cli_pattern:
				self.invoke(parameter.cli.cli_pattern)
			elif parameter.cli.code_block:
				self.invoke(parameter.cli.cli_pattern)
		for cli_alias in parameter.cli_aliases:
			self.invoke(cli_alias)
		for constraint in parameter.constraints:
			self.invoke(constraint)
		self.parent_stack.pop()
		self.invoke(parameter)
		
	def process_command(self, command):
		self.parent_stack.append(command)
		for parameter in command.parameters:
			if element_type(parameter) == 'Parameter':
				self.process_parameter(parameter)
			elif element_type(parameter) == 'ParameterReference':
				self.invoke(parameter)
		for subcommand in command.sub_commands:
			if element_type(subcommand) == 'Command':
				self.process_command(subcommand)
			elif element_type(subcommand) == 'CommandReference':
				self.invoke(subcommand)
		if command.constraints:
			self.invoke(command.constraints)
		for usage in command.usages:
			self.process_cli_group(usage)
		if command.gui:
			self.process_gui_structure(command.gui)
		self.parent_stack.pop()
		self.invoke(command)
				
	def process_cli_group(self, group):
		self.parent_stack.append(group)
		for element in group.elements:
			if hasattr(element, 'elements'):
				self.process_cli_group(element)
			else:
				self.invoke(element)
		self.parent_stack.pop()
		self.invoke(group)
		
	def process_gui_structure(self, gui_structure):
		print('ModelProcessor.process_gui_structure: not implemented!!!!!!!!')

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
			file_path, el_name = self.import_paths[parameter_reference.imported]
			if el_name in [p.name for p in parameter_reference.parent.parameters if element_type(p) == 'Parameter']:
				raise Exception('Parameter name collision between {cmd}.{param} and an imported parameter from {path}.'.format(cmd=parameter_reference.parent.name, param=el_name, path=file_path))
			imported_model = self.imported_models[file_path]
			for instance in imported_model.elements:
				if element_type(instance) == 'Parameter' and instance.name == el_name:
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

						return
			else:
				raise Exception("Unresolved local reference: {}".format(command_reference.local))
		else:
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
			
	def replace_command_reference(command_reference, instance):
		idx = command_reference.parent.sub_commands.index(command_reference)
		command_reference.parent.sub_commands[idx] = instance
		
def add_id(element):
	element.id = '/'+'/'.join([e.name for e in all_parent_commands(element)+[element]])
	
def set_usage_defaults(command):
	if not command.usages:
		default_usage = CliStructure(command, sorted([p for p in command.parameters if not p.nonpositional], key=lambda p: 0 if p.multiplicity != '*' else 1),
									has_options=True, has_subcommand=False)
		command.usages = [default_usage]
		
	if command.sub_commands and all([not usage.has_subcommand for usage in command.usages]):
		for usage in command.usages:
			usage.has_subcommand = True

def group_cli_sub_elements(cli_element, parents):
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

_usage_tree_processor_visitor = {'CliStructure':group_cli_sub_elements, 'CliGroup':group_cli_sub_elements, 'CliOptionalGroup':group_cli_sub_elements, 'CliOrGroup':group_cli_sub_elements}

def expand_options_shortcut(command):
	for usage in command.usages:
		if usage.has_options:
			options = [p for p in command.parameters if p.nonpositional and p not in usage.sub_elements]
			usage.elements = [CliOptionalGroup(usage, [p]) for p in options] + usage.elements
			usage.sub_elements = set(options).union(usage.sub_elements)

def parameter_declaration_check(cli_structure):
	parent_cmd = parent_command(cli_structure)
	declared_names = [p.name for p in parent_cmd.parameters]
	for element in cli_structure.sub_elements:
		if element.name not in declared_names:
			raise Exception('Undeclared parameter: {param} in command: {cmd}.'.format(param=element.name, cmd=parent_cmd.name))
			
def validate_command(command, parents):
	script = parents[0]
	for parameter in command.parameters:
		if parameter.name in [p.name for p in script.free_parameters] and not parameter in script.free_parameters:
			raise Exception('Parameter name collision between {cmd}.{param} and a top level free parameter.'.format(cmd=command.name, param=parameter.name))
			
		if parameter.default_is_none:
			if all([is_parameter_required(u, parameter) for u in parameter.usages]):
				print('Warning: parameter.default == None and parameter is required in all usage patterns.')
	
	for sub_command in command.sub_commands:
		if sub_command.name in [c.name for c in script.free_commands] and not sub_command in script.free_commands:
			raise Exception('Command name collision between {cmd}.{sub} and a top level free command.'.format(cmd=command.name, sub=sub_command.name))
			
	for usage in command.usages:
		rightmost = rightmost_positional_elements(usage)
		for element in usage.sub_elements:
			if element_type(element) == "Parameter" and not element.nonpositional and element.multiplicity == '*' and element not in rightmost:
				raise Exception("A positional parameter with multiplicity '*' must be the rightmost one: {}.".format(element.name))
				
def is_parameter_required(usage, parameter):
	if parameter not in usage.sub_elements:
		return False
	for element in usage.elements:
		if element is parameter:
			return True
		if element_type(element) == 'CliGroup':
			if is_parameter_required(element, parameter):
				return True
		if element_type(element) == 'CliOrGroup':
			if all([is_parameter_required(el, parameter) for el in element]):
				return True
	return False

_validator_visitor = {'CliStructure':parameter_declaration_check, 'Command':validate_command}

def get_group_elements_usage_repr(group):
	return [el.string_repr if hasattr(el, 'string_repr') else el.usage_repr for el in group.elements]
	
def cli_structure_usage_repr(group):
	str_elements = get_group_elements_usage_repr(group)
	group.string_repr = ' '.join(str_elements)
	
def cli_group_usage_repr(group):
	str_elements = get_group_elements_usage_repr(group)
	group.string_repr = '('+' '.join(str_elements)+')'
	
def cli_optional_group_usage_repr(group):
	str_elements = get_group_elements_usage_repr(group)
	group.string_repr = '['+' '.join(str_elements)+']'
	
def cli_or_group_usage_repr(group):
	str_elements = get_group_elements_usage_repr(group)
	group.string_repr = '|'.join(str_elements)
	
_usage_repr_visitor = {'CliStructure':cli_structure_usage_repr, 'CliGroup':cli_group_usage_repr, 'CliOptionalGroup':cli_optional_group_usage_repr, 'CliOrGroup':cli_or_group_usage_repr}

def add_builtin_help(command, parent_elements):
	if not command.help_params:
		command.help_params = ['-h', '--help']
		
	if not command.long_help_params:
		command.long_help_params = ['-a', '--all']
		
	resolve_builtin_help_params(command)
	
	parent_commands = [parent for parent in parent_elements if element_type(parent) == 'Command']
	command.usage_help = generate_usage_help(command, parent_commands)
	command.long_usage_help = generate_usage_help(command, parent_commands, long=True)

def resolve_builtin_help_params(command):
	for param in command.parameters: # remove all help params with the same prefixes as other already existing params
		if param.nonpositional:
			for pattern in param.all_patterns:
				if element_type(pattern) == 'StringParamPattern' and pattern.prefix in command.help_params:
					command.help_params.remove(pattern.prefix)
				if element_type(pattern) == 'StringParamPattern' and pattern.prefix in command.long_help_params:
					command.long_help_params.remove(pattern.prefix)
				elif element_type(pattern) in ['BoolWithPositivePattern', 'BoolNegativeOnlyPattern']:
					if pattern.positive in command.help_params:
						command.help_params.remove(pattern.positive)
					if pattern.negative in command.help_params:
						command.help_params.remove(pattern.negative)
					if pattern.positive in command.long_help_params:
						command.long_help_params.remove(pattern.positive)
					if pattern.negative in command.long_help_params:
						command.long_help_params.remove(pattern.negative)
					
def generate_usage_help(command, parents, long=False):
	# this command followed by all the parent commands
	command_str = ' '.join([c.cli_command for c in parents + [command]])
	# a set of built in help parameters common to all subcommands
	common_subcommand_help_params = reduce(lambda x,y: x.intersection(y), [set(c.help_params) for c in command.sub_commands]) if command.sub_commands else set()
	common_subcommand_help = common_subcommand_help_params.pop() if common_subcommand_help_params else None
	
	return _usage_help_template.render(command=command, parents=parents, long=long, command_str=command_str, common_subcommand_help=common_subcommand_help)

def generate_parameters_usage_help(command, long, command_str):
	rows = []
	col_length = 0
	desc_col_width = 50 # TODO config za width
	
	parameters = reduce(lambda x,y: x.union(y), [u.sub_elements for u in command.usages])
	
	for param in parameters:
		param_patterns_repr = generate_param_patterns_repr(param)
		col_length = max(len(param_patterns_repr), col_length)
		desc_lines = textwrap.wrap(param.description, desc_col_width)
		rows.append((param_patterns_repr, desc_lines[0]))
		for desc_line in desc_lines[1:]:
			rows.append(('', desc_line))
		if long and param.help:
			help_lines = textwrap.wrap(param.help, desc_col_width)
			for help_line in help_lines:
				rows.append(('', help_line))
	
	if command.help_params:
		help_params_repr = ', '.join(command.help_params)
		col_length = max(len(help_params_repr), col_length)
		if command.long_help_params:
			if long:
				long_help_desc = " For this help message type: {cmd} {help_p} {long_help_p}.".format(cmd=command_str, help_p=command.help_params[0], long_help_p=command.long_help_params[0])
				if len(command.long_help_params) > 1:
					long_help_desc += " All detailed help parameters: {long_help_p}.".format(long_help_p=', '.join(command.long_help_params))
			else:
				long_help_desc = " For more detailed help type: {cmd} {help_p} {long_help_p}.".format(cmd=command_str, help_p=command.help_params[0], long_help_p=command.long_help_params[0])
		if long:
			help_desc = "Shows a shorter help message."
		else:
			help_desc = "Shows this help message."
		desc_lines = textwrap.wrap(help_desc+long_help_desc, desc_col_width)
		rows.append((help_params_repr, desc_lines[0]))
		for desc_line in desc_lines[1:]:
			rows.append(('', desc_line))
	
	row_format = '  {:'+str(col_length)+'}  {}'
	return '\n'.join([row_format.format(*row) for row in rows])
	
def generate_param_patterns_repr(parameter):
	if parameter.nonpositional:
		repr_list = []
		for pattern_repr in [cli_pattern_repr(p) for p in parameter.all_patterns]:
			if isinstance(pattern_repr, tuple):
				pos, neg = pattern_repr
				if pos:
					repr_list.append(pos)
				if neg:
					repr_list.append(neg)
			else:
				repr_list.append(pattern_repr)
		return ', '.join(repr_list)
	else:
		return "<{}>".format(parameter.name.upper())
	
def generate_subcommands_usage_help(command, common_subcommand_help, parents):
	rows = []
	col_length = 0
	for subcommand in command.sub_commands:
		col_length = max(len(subcommand.cli_command), col_length)
		row = [subcommand.cli_command, '']
		rows.append(row)
		if subcommand.description:
			desc_lines = textwrap.wrap(subcommand.description, 50)
			row[1] = desc_lines[0]
			for desc_line in desc_lines[1:]:
				rows.append(['', desc_line])
		if not common_subcommand_help and subcommand.help_params:
			subcommand_str = ' '.join([c.cli_command for c in parents + [command, subcommand]])
			more_help_str = "For more help type: {} {}.".format(subcommand_str, subcommand.help_params[0])
			if not row[1]:
				row[1] = more_help_str
			else:
				rows.append(['', more_help_str])
	row_format = '  {:'+str(col_length)+'}  {}'
	return '\n'.join([row_format.format(*row) for row in rows])

_usage_help_jinja_env = Environment(loader=FileSystemLoader('.'))
_usage_help_jinja_env.filters['parameters_usage_help'] = generate_parameters_usage_help
_usage_help_jinja_env.filters['subcommands_usage_help'] = generate_subcommands_usage_help
_usage_help_template = _usage_help_jinja_env.get_template('usage_help.template')

# ------------------------------- DATA EXTRACTORS -------------------------------

def get_default_values(commands):
	return {cmd.name : {param.name : param.default for param in cmd.parameters} for cmd in commands}
	
def get_cli_separators(commands):
	return {cmd.name : cmd.cli_separators if hasattr(cmd, 'cli_separators') else [] for cmd in commands}
	
def get_parameter_types(commands):
	return {cmd.name : {param.name : param.type for param in cmd.parameters} for cmd in commands}
	
def get_date_formats(commands):
	return {cmd.name : {param.name : param.date_format for param in cmd.parameters if param.date_format} for cmd in commands}
	
class ElementExtractor():
	def __init__(self):
		self.all_commands = []
		self.all_parameters = []
		self.extract_command = lambda c: self.all_commands.append(c)
		self.extract_parameter = lambda p: self.all_parameters.append(p)
		self.visitor = {'Command':self.extract_command, 'Parameter':self.extract_parameter}
	
# ------------------------------- JINJA FILTERS -------------------------------

def parameter_model_filter(parameter):
	print_list = lambda lst: str(lst) if len(lst) > 1 else "'{}'".format(lst[0])
	
	if parameter.type == 'Bool':
		positives = [p.positive for p in parameter.all_patterns if p.positive]
		negatives = [p.negative for p in parameter.all_patterns if p.negative]
		
		positives_str = ", positives={prefixes}".format(prefixes=print_list(positives)) if positives else ''
		negatives_str = ", negatives={prefixes}".format(prefixes=print_list(negatives)) if negatives else ''
		
		return "BooleanNonpositional('{name}'{positives}{negatives}),".format(name=parameter.name, positives=positives_str, negatives=negatives_str)
	else:
		ret = []
		classified = defaultdict(lambda: defaultdict(set))
		for pattern in parameter.all_patterns:
			if pattern.white_space:
				if pattern.vars:
					count_str = ", vars={vars}".format(vars=pattern.vars)
				elif pattern.count:
					count_str = ", count={count}".format(count=pattern.count)
				elif pattern.count_many:
					count_str = ", count='*'"
				else:
					count_str = ''
				classified['MultiArgNonpositional'][count_str].add(pattern)
			else:
				if pattern.count_many:
					if pattern.separator:
						separator_str = ", '{}'".format(pattern.separator)
					else:
						separator_str = ''
					classified['SeparatedNonpositional'][separator_str].add(pattern)
				elif pattern.count_char:
					classified['CounterNonpositional'][pattern.count_char].add(pattern)
				else:
					classified['BasicNonpositional']['_'].add(pattern)
		
		if classified['MultiArgNonpositional']:
			for count_str, patterns in classified['MultiArgNonpositional'].items():
				prefixes = [p.prefix for p in patterns]
				ret.append("MultiArgNonpositional('{name}', {prefixes}{count_str})".format(name=parameter.name, prefixes=print_list(prefixes), count_str=count_str))
		if classified['SeparatedNonpositional']:
			for separator_str, patterns in classified['SeparatedNonpositional'].items():
				prefixes = [p.prefix for p in patterns]
				ret.append("SeparatedNonpositional('{name}', {prefixes}{separator_str})".format(name=parameter.name, prefixes=print_list(prefixes), separator_str=separator_str))
		if classified['CounterNonpositional']:
			for count_char, patterns in classified['CounterNonpositional'].items():
				prefixes = [p.prefix for p in patterns]
				ret.append("CounterNonpositional('{name}', {prefixes}, '{count_char}'), ".format(name=parameter.name, prefixes=print_list(prefixes), count_char=count_char))
		if classified['BasicNonpositional']:
			for _, patterns in classified['BasicNonpositional'].items():
				prefixes = [p.prefix for p in patterns]
				ret.append("BasicNonpositional('{name}', {prefixes})".format(name=parameter.name, prefixes=print_list(prefixes)))
		return ', '.join(ret)
		
def tab_indent_filter(text, level=1, start_from=1):
	return '\n'.join([(level*'\t')+line if idx+1 >= start_from else line for idx, line in enumerate(text.split('\n'))])
	
def raise_exception_helper(msg):
	raise Exception(msg)
	
def stringify_filter(value):
	if isinstance(value, str):
		return "'{}'".format(value)
	else:
		return value

# ------------------------------- MAIN -------------------------------

def parse(script_path):
	metamodel = metamodel_from_file('cid_grammar.tx', classes=[])
	
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
		'CliSeparator':process_cli_separator,
		'StringParamPattern':process_string_param_pattern,
	})
	
	model = metamodel.model_from_file(script_path)
	
	all_defined_commands = command_processor.all_defined_commands
	all_defined_parameters = parameter_processor.all_defined_parameters
	
	# dereferencing ---------------------
	
	ModelProcessor(ReferenceResolver(all_defined_parameters, all_defined_commands, model.imports).visitor).process_model(model)
	ModelProcessor({'Command':add_id, 'Parameter':add_id}).process_model(model)
	
	return model
	
if __name__ == '__main__':
	model = parse('./example1.cid')
	
	# second pass ---------------------
	
	ModelProcessor({'Command':set_usage_defaults}).process_model(model)
	ModelProcessor(_usage_tree_processor_visitor).process_model(model)
	ModelProcessor({'Command':expand_options_shortcut}).process_model(model)
	ModelProcessor(_validator_visitor).process_model(model)
	ModelProcessor(_usage_repr_visitor).process_model(model)
	ModelProcessor({'Command':add_builtin_help}).process_model(model)
	
	model_extractor = ElementExtractor()
	ModelProcessor(model_extractor.visitor).process_model(model)
	
	all_commands = model_extractor.all_commands
	all_parameters = model_extractor.all_parameters
	
	default_values = get_default_values(all_commands)
	builtin_help_params = {cmd.name : cmd.help_params for cmd in all_commands}
	builtin_long_help_params = {cmd.name : cmd.long_help_params for cmd in all_commands}
	cli_separators = get_cli_separators(all_commands)
	parameter_types = get_parameter_types(all_commands)
	date_formats = get_date_formats(all_commands)
	
	# print model ---------------------
	
	print_model(model, print_empty_attrs=False, print_empty_lists=True, omitted_attributes=[ 
		#'usage_help', 'long_usage_help', 
		'all_patterns', 
		'sub_elements',
	])
	
	# --------------------- RENDER CLI TEMPLATE ---------------------
	env = Environment(loader=FileSystemLoader('.'))
	env.filters['parameter_model'] = parameter_model_filter
	env.filters['element_type'] = element_type
	env.filters['tab_indent'] = tab_indent_filter
	env.filters['stringify'] = stringify_filter
	env.globals['raise'] = raise_exception_helper
	
	template = env.get_template('cli_parser_config.py.template')
	
	rendered = template.render(root_command_name='command1', commands=all_commands, default_values=default_values, parameter_types=parameter_types, date_formats=date_formats, 
		builtin_help_params=builtin_help_params, builtin_long_help_params=builtin_long_help_params, cli_separators=cli_separators)
	#print(rendered)

	with open("command1_cli_config.py", "w") as text_file:
		text_file.write(rendered)
	
	from command1_cli_config import root_command_name, command_models
	from cli_parser import parse_cli_args, invoke_commands
	
	# matched_args = parse_cli_args(root_command_name, command_models, args)
	# print(matched_args, '\n\n')
	def dummy_print_callback(name):
		return lambda args, sub_command: print(name, 'callback:', '\n\t'+str(args), '\n\tsub_command: {}'.format(sub_command))
	
	args = 'p3 --par1 x y -vvv -- p2'.split()
	#args = "sub1 -h -a".split()
	
	invoke_commands({'command1':dummy_print_callback('command1'), 'sub1':dummy_print_callback('sub1'), 'sub2':dummy_print_callback('sub2'), 'sub3':dummy_print_callback('sub3'),}, root_command_name, command_models, args)
	


# custom -h --help -a i --all [v]
# zavrsiti checkove [-]
# {options} [v]
# importovanje [v]
# konverzija tipova u invoke [v]
# razdvojiti u fajlove sta je zajednicko / sta je samo za cli []
# da moze u description da se ubaci generisani desc sa {default} pa onda .format(description=generated_desc) [v]
# replace reference with real object [v]
# choices custom code []
# kad se importuje skripta u procesorima da se preskacu elementi koji se ne koriste []