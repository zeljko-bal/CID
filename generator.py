
from textx.metamodel import metamodel_from_file
from jinja2 import Environment, FileSystemLoader
from collections import namedtuple, defaultdict
from modelprinter import print_model
from functools import reduce
from inspect import getfullargspec
from types import MethodType, BuiltinMethodType
import textwrap

script = """

Bool option1 "option1":
	cli: "--option1", "-o1|-no1"
	default: "False"

Cmd command1 "Command1":
	help: "help"
	parameters:
	{
		Str par0:
			default: "asd"
		
		option1
			
		Str par2:
			default: "asd"
			
		Str par1:
			cli: "--par1 {5}", "-p1 {}"
			default: "asd"
			
		Str par3:
			multiplicity: 2
			default: "asd"
	}
	commands:
	{
		Sub sub1:
			parameters:
			{
				option1
			}
			usage: option1
		Sub sub2:
			parameters:
			{
				option1
				Bool help:
					cli: "--help", "-h"
					default: "False"
			}
			cli_command: "subcommand2"
		Sub sub3
	}
	usage: 
		- [option1] par1 
		- option1 {sub_command}
"""

args = ' --par1 a b d c a --option1'.split()
#args = "sub1 -h -a".split()

class ParameterReference:
	def __init__(self, value):
		self.value = value
		
class CliOptionalGroup:
	def __init__(self, elements):
		self.elements = elements
		
class CliStructure:
	def __init__(self, elements, has_options, has_subcommand):
		self.elements = elements
		self.has_options = has_options
		self.has_subcommand = has_subcommand

def element_type(element):
	return element.__class__.__name__
	
def parent_command(reference):
	parent = reference.parent
	while element_type(parent) != 'Command':
		if element_type(parent) == 'Script':
			return None
		parent = parent.parent
	return parent
	
def all_parent_commands(command):
	parent = parent_command(command)
	ret = []
	while parent:
		ret.append(parent)
		parent = parent_command(parent)
	return ret
	
def dereference(element):
	if element_type(element) in ['ParameterReference', 'CommandReference']:
		if hasattr(element, 'value'):
			return element.value
		elif element.local:
			return element.local
		elif element.imported:
			return element.imported
	else:
		return element

def contains_duplicate_names(lst):
	defined = [e.name for e in lst if not hasattr(e, 'imported') and not hasattr(e, 'local')]
	local = [e.local for e in lst if hasattr(e, 'local') and e.local]
	imported = [e.imported for e in lst if hasattr(e, 'imported') and e.imported]
	
	return len(defined) != len(set(defined)) or len(local) != len(set(local)) or len(imported) != len(set(imported))

def process_script(script):
	# check for duplicate free parameter names
	script.free_parameters = [p for p in script.elements if element_type(p) == 'Parameter']
	if contains_duplicate_names(script.free_parameters):
		raise Exception('same_name_params_check')
	
	# check for duplicate free command names
	script.free_commands = [p for p in script.elements if element_type(p) == 'Command']
	if contains_duplicate_names(script.free_commands):
		raise Exception('same_name_commands_check')
	
def process_cli_or_group(or_group):
	# transform the tree structure into a list
	or_group.elements = [or_group.lhs[0]]
	
	if element_type(or_group.rhs[0]) == 'CliOrGroup':
		or_group.elements += or_group.rhs[0].elements
	else:
		or_group.elements.append(or_group.rhs[0])
	del or_group.lhs
	del or_group.rhs
	
	# check for CliOptionalGroup in CliOrGroup
	for element in or_group.elements:
		if element_type(element) == 'CliOptionalGroup':
			print('warning: CliOptionalGroup in or_group')
	
class CommandProcessor:
	def __init__(self):
		self.all_defined_commands = []

	def transform_command(self, command):
		# transform multiline usages
		if command.usages:
			command.usages = [usage.body for usage in command.usages]
		elif command.usage:
			command.usages = [command.usage]
			del command.usage
		
		if not command.cli_command:
			command.cli_command = command.name
	
	def check_command(self, command):
		if contains_duplicate_names(command.parameters):
			raise Exception('same_name_params_check')
			
		if contains_duplicate_names(command.sub_commands):
			raise Exception('same_name_commands_check')
	
	def process_command(self, command):
		self.transform_command(command)
		self.check_command(command)
		self.all_defined_commands.append(command)

def cli_pattern_repr(pattern):
	if element_type(pattern) == 'StringParamPattern':
		if pattern.count_char:
			return '{pref}{count_char}'.format(pref=repr_pattern.prefix, count_char=repr_pattern.count_char)
		else:
			space = ' ' if pattern.white_space else ''
			if pattern.count:
				count_repr = '...{}'.format(pattern.count)
			elif pattern.count_many:
				if pattern.separator:
					count_repr = '...[{}]'.format(pattern.separator)
				else:
					count_repr  = '...'
			else:
				count_repr = ''
			return '{pref}{space}<{count}>'.format(pref=pattern.prefix, space=space, count=count_repr)
	else:
		if pattern.positive and pattern.negative:
			return pattern.positive, pattern.negative
		elif pattern.positive:
			return pattern.positive, None
		elif pattern.negative:
			return None, pattern.negative
		
class ParameterProcessor:
	def __init__(self, imported_prefixes=[]):
		self.all_prefixes = imported_prefixes
		self.all_defined_parameters = []
		
	def process_parameter(self, parameter):
		if parameter.widget:
			supported_widgets = {
			 'Str':['password', 'text_field', 'text_area', ],
			 'Choice':['dropdown', 'radio_buttons'],
			 'Num':['counter', 'slider'],
			}[element_type(parameter)]
			if parameter.widget not in supported_widgets:
				raise Exception('parameter.widget unsupported')
		
		if parameter.choices and not element_type(parameter) == 'Choice':
			raise Exception('choices in not Choice')
		
		if element_type(parameter) == 'Choice' and not parameter.choices:
			raise Exception('choices required in Choice')
		
		if parameter.date_format and not element_type(parameter) == 'Date':
			raise Exception('date_format in not Date')
		
		for constraint in parameter.constraints:
			supported_constraints = {
			 'Str':[],
			 'Choice':[],
			 'Num':[],
			}[element_type(parameter)]
			if constraint.type not in supported_constraints:
				raise Exception('constraint.type unsupported')
		
		if not parameter.none_value_allowed == 'Allowed' and parameter.default == 'None':
			raise Exception("parameter.none value disallowed and parameter.default == 'None'")
			
		if parameter.default_is_none and parameter.default:
			raise Exception('parameter.default_is_none and parameter.default')
			
		parameter.nonpositional = True if parameter.cli and parameter.cli.cli_pattern else False
		if parameter.nonpositional:
			parameter.prefixes = []
			if parameter.type == 'Bool':
				parameter.pos_prefixes = []
				parameter.neg_prefixes = []
			str_patterns = []
			pos_patterns = []
			neg_patterns = []
			for pattern in [parameter.cli.cli_pattern]+parameter.cli_aliases:
				if element_type(pattern) == 'StringParamPattern':
					parameter.prefixes.append(pattern.prefix)
					str_patterns.append(pattern)
				else:
					if pattern.positive:
						parameter.prefixes.append(pattern.positive)
						parameter.pos_prefixes.append(pattern.positive)
						pos_patterns.append(pattern)
					if pattern.negative:
						parameter.prefixes.append(pattern.negative)
						parameter.neg_prefixes.append(pattern.negative)
						neg_patterns.append(pattern)
			for prefix in parameter.prefixes:
				if prefix in self.all_prefixes:
					raise Exception('duplicate prefixes')
				self.all_prefixes.append(prefix)
		
		if parameter.nonpositional:
			if str_patterns:
				repr_pattern = max(str_patterns, key=lambda p: len(p.prefix)) # longest prefix
				parameter.usage_repr = cli_pattern_repr(repr_pattern)
			elif pos_patterns or neg_patterns:
				if pos_patterns:
					repr_pattern = max(pos_patterns, key=lambda p: len(p.positive)) # longest positive
					parameter.usage_repr, _ = cli_pattern_repr(repr_pattern)
				elif neg_patterns:
					repr_pattern = max(neg_patterns, key=lambda p: len(p.negative)) # longest negative
					_, parameter.usage_repr = cli_pattern_repr(repr_pattern)
		else:
			parameter.usage_repr = "<{}{}>".format(parameter.name.upper(), '...' if parameter.multiplicity == '*' else '')
		
		self.all_defined_parameters.append(parameter)

# ------------------------------- JINJA FILTERS -------------------------------

def parameter_model_filter(parameter):
	if parameter.nonpositional:
		def print_list(lst):
			return str(lst) if len(lst) > 1 else "'{}'".format(lst[0])
		
		if parameter.type == 'Bool':
			positives = []
			negatives = []
			
			for pattern in ([parameter.cli.cli_pattern] if parameter.cli.cli_pattern else []) + parameter.cli_aliases:
				if pattern.positive:
					positives.append(pattern.positive)
				if pattern.negative:
					negatives.append(pattern.negative)
			
			if not positives and not negatives:
				return ''
			
			if positives:
				positives_str = ", positives={}".format(print_list(positives))
			else:
				positives_str=''

			if negatives:
				negatives_str = ", negatives={}".format(print_list(negatives))
			else:
				negatives_str=''
			
			return "BooleanNonpositional('{name}'{positives}{negatives}),".format(name=parameter.name, positives=positives_str, negatives=negatives_str)
		else:
			ret = []
			classified = defaultdict(lambda: defaultdict(set))
			for pattern in ([parameter.cli.cli_pattern] if parameter.cli.cli_pattern else []) + parameter.cli_aliases:
				if pattern.white_space:
					if pattern.count:
						count_str = ", {}".format(pattern.count)
					elif pattern.count_many:
						count_str = ", '*'"
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
						classified['CounterNonpositional'][count_char].add(pattern)
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
					ret.append("CounterNonpositional('{name}', {prefixes}'{count_char}'), ".format(name=parameter.name, prefixes=print_list(prefixes), count_char=count_char))
			if classified['BasicNonpositional']:
				for _, patterns in classified['BasicNonpositional'].items():
					prefixes = [p.prefix for p in patterns]
					ret.append("BasicNonpositional('{name}', {prefixes})".format(name=parameter.name, prefixes=print_list(prefixes)))
			return ', '.join(ret)
	else:
		return ''
		
def tab_indent_filter(text, level=1, start_from=1):
	return '\n'.join([(level*'\t')+line if idx+1 >= start_from else line for idx, line in enumerate(text.split('\n'))])

def raise_exception_helper(msg):
	raise Exception(msg)
	
# ------------------------------- ModelProcessor -------------------------------

class ModelProcessor:
	def __init__(self, callbacks):
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
		self.parent_stack = []
		
	def invoke(self, element):
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
	
class ReferenceResolver:
	def __init__(self, parameter_instances, command_instances):
		self.parameter_instances = parameter_instances
		self.command_instances = command_instances
		self.visitor = {'ParameterReference':self.resolve_parameter_reference, 'CommandReference':self.resolve_command_reference, 'Command':self.create_resolved_list_attribute}
	
	def resolve_parameter_reference(self, parameter_reference):
		if parameter_reference.local:
			for instance in self.parameter_instances:
				if instance.name == parameter_reference.local:
					if element_type(instance.parent) == 'Script' or instance.parent.name == parent_command(parameter_reference).name:
						parameter_reference.value = instance
						break
			else:
				raise Exception("Unresolved reference: {}".format(parameter_reference.local))
		else:
			pass # TODO imported reference
			
	def resolve_command_reference(self, command_reference):
		if command_reference.local:
			for instance in self.command_instances:
				if instance.name == command_reference.local:
					if element_type(instance.parent) == 'Script' or instance.parent.name == parent_command(command_reference).name:
						command_reference.value = instance
						break
			else:
				raise Exception("Unresolved reference: {}".format(command_reference.local))
		else:
			pass # TODO imported reference
			
	def create_resolved_list_attribute(self, command):
		command.resolved_parameters = [dereference(p) for p in command.parameters]
		command.resolved_commands = [dereference(c) for c in command.sub_commands]
	
def process_cli_separator(cli_separator):
	cli_separator.value = cli_separator.value[0]
	cmd = parent_command(cli_separator)
	if not hasattr(cmd, 'cli_separators'):
		cmd.cli_separators = []
	cmd.cli_separators.append(cli_separator.value)
	
def gather_cli_sub_elements(cli_element):
	if not hasattr(cli_element, 'sub_elements'):
		cli_element.sub_elements = set()
	
	for group_element in cli_element.elements:
		if hasattr(group_element, 'sub_elements'):
			if not cli_element.sub_elements.isdisjoint(group_element.sub_elements) and not element_type(cli_element) == 'CliOrGroup':
				raise Exception('duplicate element in usage')
			cli_element.sub_elements.update(group_element.sub_elements)
		elif hasattr(group_element, 'value') and not element_type(group_element) == 'CliSeparator':
			if group_element.value in cli_element.sub_elements and not element_type(cli_element) == 'CliOrGroup':
				raise Exception('duplicate element in usage')
			cli_element.sub_elements.add(group_element.value)

_duplicate_usage_elements_visitor = {'CliStructure':gather_cli_sub_elements, 'CliGroup':gather_cli_sub_elements, 'CliOptionalGroup':gather_cli_sub_elements, 'CliOrGroup':gather_cli_sub_elements}
	
def get_group_elements_usage_repr(group):
	return [el.string_repr if hasattr(el, 'string_repr') else el.value.usage_repr for el in group.elements]
	
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
	
def resolve_help_params(command):
	for param in command.resolved_parameters: # remove all help params with the same prefixes as already existing params
		patterns = list(param.cli_aliases)
		if param.cli and param.cli.cli_pattern:
			patterns.append(param.cli.cli_pattern)
		for pattern in patterns:
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

def generate_param_patterns_repr(parameter):
	if parameter.nonpositional:
		repr_list = []
		for pattern_repr in [cli_pattern_repr(p) for p in [parameter.cli.cli_pattern]+parameter.cli_aliases]:
			if isinstance(pattern_repr, tuple): # TODO ugly, refactor
				pos, neg = pattern_repr
				if pos:
					repr_list.append(pos)
				if neg:
					repr_list.append(neg)
			else:
				repr_list.append(pattern_repr)
		return ', '.join(repr_list)
	else:
		return "<{}>".format(parameter.name.upper(), parameter.description)

def generate_parameters_usage_help(command, long):
	rows = []
	col_length = 0
	for param in command.resolved_parameters:
		param_patterns_repr = generate_param_patterns_repr(param)
		col_length = max(len(param_patterns_repr), col_length)
		desc_lines = textwrap.wrap(param.description, 50)
		rows.append((param_patterns_repr, desc_lines[0]))
		for desc_line in desc_lines[1:]:
			rows.append(('', desc_line))
		if long and param.help:
			help_lines = textwrap.wrap(param.help, 50)
			for help_line in help_lines:
				rows.append(('', help_line))
	row_format = '  {:'+str(col_length)+'}  {}'
	return '\n'.join([row_format.format(*row) for row in rows])
	
def generate_subcommands_usage_help(command, common_subcommand_help, parents):
	rows = []
	col_length = 0
	for subcommand in command.resolved_commands:
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
	
def generate_usage_help(command, parents, long=False):
	command_str = ' '.join([c.cli_command for c in parents + [command]])
	common_subcommand_help = reduce(lambda x,y: x.intersection(y), [set(c.help_params) for c in command.resolved_commands]) if command.sub_commands else []
	
	return _usage_help_template.render(command=command, parents=parents, long=long, command_str=command_str, common_subcommand_help=common_subcommand_help)
	
def command_defaults(command, parent_elements):
	if not command.title:
		command.title = command.name.replace('_', ' ').replace('-', ' ').strip().title()
	
	if not command.usages:
		default_usage = CliStructure([ParameterReference(p) for p in command.resolved_parameters if not p.nonpositional]+
									  [CliOptionalGroup([ParameterReference(p)]) for p in command.resolved_parameters if p.nonpositional],
									  has_options=False, has_subcommand=True) # TODO maybe just has_options = True
		ModelProcessor(_usage_repr_visitor).process_cli_group(default_usage)
		command.usages = [default_usage]
		
	if command.sub_commands and all([not usage.has_subcommand for usage in command.usages]):
		for usage in command.usages:
			usage.has_subcommand = True
	
	if not command.help_params:
		command.help_params = ['-h', '--help']
		
	if not command.long_help_params:
		command.long_help_params = ['-a', '--all']
		
	resolve_help_params(command)
	
	parent_commands = [parent for parent in parent_elements if element_type(parent) == 'Command']
	#print(parent_commands, parent_elements)
	command.usage_help = generate_usage_help(command, parent_commands)
	command.long_usage_help = generate_usage_help(command, parent_commands, long=True)
	
def parameter_defaults(parameter):
	if not parameter.title:
		parameter.title = parameter.name.replace('_', ' ').replace('-', ' ').strip().title()
		
	if not parameter.multiplicity:
		parameter.multiplicity = 1
		
	if not parameter.description:
		pretty_type = {
			 "Str":"String",
			 "Num":"Number",
			 "Bool":"Flag",
			 "Date":"Date",
			 "File":"File",
			 "Choice":"Choice",
		}[parameter.type]
		parameter.description = "Data type: {}.".format(pretty_type)
		if parameter.default:
			parameter.description += " Default value: {}.".format("'{}'".format(parameter.default) if isinstance(parameter.default, str) else parameter.default)
		if parameter.type == 'Bool' and parameter.neg_prefixes:
			if parameter.pos_prefixes:
				parameter.description += " Parameters {} represent True.".format(parameter.pos_prefixes)
			parameter.description += " Parameters {} represent False.".format(parameter.neg_prefixes)
		if parameter.choices:
			parameter.description += " Choices: {}".format(parameter.choices)
		if parameter.date_format:
			parameter.description += " Date format: {}".format(parameter.date_format)
		if parameter.multiplicity != 1:
			if parameter.multiplicity == '*':
				parameter.description += "This parameter can appear an unlimited amount of times."
			else:
				parameter.description += " This parameter can appear at most {} times.".format(parameter.multiplicity)
	
	
	
	
def import_statement_defaults(import_statement):
	if not import_statement.alias:
		import_statement.alias = import_statement.path
	
def get_default_values(commands):
	default_values = {}
	for cmd in commands:
		cmd_defaults = {}
		for param in cmd.resolved_parameters:
			cmd_defaults[param.name] = param.default
		default_values[cmd.name] = cmd_defaults
	return default_values
	
def get_cli_separators(commands):
	return {cmd.name : cmd.cli_separators if hasattr(cmd, 'cli_separators') else [] for cmd in commands}
	
# ------------------------------- MAIN -------------------------------

if __name__ == '__main__':
	metamodel = metamodel_from_file('cid_grammar.tx', classes=[])
	
	command_processor = CommandProcessor()
	parameter_processor = ParameterProcessor()
	
	metamodel.register_obj_processors({
		'Script':process_script,
		'Command':command_processor.process_command,
		'Parameter':parameter_processor.process_parameter,
		'CliOrGroup':process_cli_or_group,
		'CliSeparator':process_cli_separator,
	})
	
	model = metamodel.model_from_str(script)
	
	ModelProcessor(ReferenceResolver(parameter_processor.all_defined_parameters, command_processor.all_defined_commands).visitor).process_model(model)
	ModelProcessor(_duplicate_usage_elements_visitor).process_model(model)
	ModelProcessor(_usage_repr_visitor).process_model(model)
	ModelProcessor({'Command':command_defaults, 'Parameter':parameter_defaults, 'ImportStatement':import_statement_defaults}).process_model(model)
	
	default_values = get_default_values(command_processor.all_defined_commands)
	builtin_help_params = {cmd.name : cmd.help_params for cmd in command_processor.all_defined_commands}
	builtin_long_help_params = {cmd.name : cmd.long_help_params for cmd in command_processor.all_defined_commands}
	cli_separators = get_cli_separators(command_processor.all_defined_commands)
	
	print_model(model, omitted_attributes=['resolved_commands', 'resolved_parameters', 
	#'usage_help', 'long_usage_help'
	])
	
	# --------------------- RENDER TEMPLATE ---------------------
	env = Environment(loader=FileSystemLoader('.'))
	env.filters['parameter_model'] = parameter_model_filter
	env.filters['element_type'] = element_type
	env.filters['tab_indent'] = tab_indent_filter
	env.globals['raise'] = raise_exception_helper
	
	template = env.get_template('cli_parser_config.py.template')
	
	rendered = template.render(root_command_name='command1', commands=command_processor.all_defined_commands, default_values=default_values, builtin_help_params=builtin_help_params, builtin_long_help_params=builtin_long_help_params, cli_separators=cli_separators)
	#print(rendered)

	with open("command1_cli_config.py", "w") as text_file:
		text_file.write(rendered)
		
	from command1_cli_config import root_command_name, command_models
	from cli_parser import parse_cli_args, invoke_commands
	
	# matched_args = parse_cli_args(root_command_name, command_models, args)
	# print(matched_args, '\n\n')
	def dummy_print_callback(name):
		return lambda args, sub_command: print(name, 'callback:', '\n\t'+str(args), '\n\tsub_command: {}'.format(sub_command))
	
	invoke_commands({'command1':dummy_print_callback('command1'), 'sub1':dummy_print_callback('sub1'), 'sub2':dummy_print_callback('sub2')}, root_command_name, command_models, args)
	


# fill in script defaults []
# choices custom code []
# custom -h --help -a i --all
