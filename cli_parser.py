
'''
nadjem sve nepozicione koji postoje
matchujem sve positional/nonpositional redom dok ne matchujem subcommand
kad matchujem subcommand proveravam ovu, ako je ok prosledjujem ostatak argumenata procesoru za subcommand
cekiram dal je ok stablo za komandu:
	- group cekiram sve redom [v]
	- nonpositional cekiram dal je prisutan [v]
	- positional pretpostavim da je sledeci od prepoznatih, ako fali fail [v]
	- optional cekiram group, ako failuje ne puca, samo ignorise [v]
	- or expression idem redom i cekiram group, prvi koji uspe vratim, ako ne uspe ni jedan fail [v]
ako pukne sastavim poruku zasto je puklo i prosledim gore, ako pukne root ispisem poruku
ako ne pukne proverim dal ima viska nonpositional il positional, ako ima viska positional kazem unknown, ako ima viska nonpositional dodam u poruku wrong arguments i ispisem sve

multiplicity: number|'*'
string..:
	--nesto={}
	--nesto {}
	--nesto {n}
	--nesto {*}
	--nesto={*|separator}
boolean:
	--nesto|--not-nesto
	--nesto
	|--not-nesto
number:
	--nesto{count:c}
	

CliValue:
	(prefix=CliLiteral(basic?='{}')|('{*|'separator=CliLiteral'}')|(single_arg?='/\b/{}')|(multi_arg?='/\b/{'count=INT'}')|('{count:'count_char=Char'}')|('|'(sufix=CliLiteral)?))|('|'sufix=CliLiteral)
;
	
CliLiteral:
	/[a-zA-Z0-9-]+/
;

Char:
	/[a-zA-Z0-9]/
;

--par1 --par3 --par4
(--par1 [--par2 --par3] (--par4)|(--par5) [--par6])
(par --par [--par par] (--par par)|(--par))

(par par (par par)|(par par sub) [par par])|(par par)


TODO:
	- aliasi [v]
	- default vrednosti [v]
	- description i help [v]
	- ogranicenja []
'''
	
from collections import namedtuple
import datetime

class CommandParserModel:
	def __init__(self, parameter_models, usage_model, parameter_types, default_values, date_formats={}, 
			usage_help='', long_usage_help='', sub_commands=[], separators=['--'], builtin_help_params=['--help', '-h'], builtin_long_help_params=['--all', '-a']):
		self.parameter_models = parameter_models
		self.usage_model = usage_model
		self.parameter_types = parameter_types
		self.date_formats = date_formats
		self.sub_commands = sub_commands
		self.separators = separators
		self.default_values = default_values
		self.usage_help = usage_help
		self.long_usage_help = long_usage_help
		self.builtin_help_params = builtin_help_params
		self.builtin_long_help_params = builtin_long_help_params

class MatchedArgument:
	def __init__(self, name, value):
		self.name = name
		self.value = value
		
	def __eq__(self, other):
		return self.name == other.name
		
	def __repr__(self):
		if isinstance(self.value, str):
			val = "'{}'".format(self.value)
		elif self.value is None:
			val = 'None'
		else:
			val = self.value
		return "<{name} = {value}>".format(name=self.name, value=val)
		
def is_iterable(obj):
	return hasattr(obj, '__iter__') and not isinstance(obj, str)
		
def convert_data(data, type, date_format=''):
	if is_iterable(data):
		return [convert_data(element, type, date_format) for element in data]
	elif isinstance(data, str):
		if type == "Num":
			try:
				return int(data_str)
			except ValueError:
				return float(data_str)
		elif type == "Date":
			return datetime.strptime(data_str, date_format)
	else:
		return data
		
# --------------------- NONPOSITIONAL ARGUMENT PARSER ---------------------

class NonpositionalArgumentParser:
	def __init__(self, parameter_models=[], sub_commands=[], separators=['--']):
		self.parameter_models = parameter_models
		self.sub_commands = {}
		for sub_command in sub_commands:
			if isinstance(sub_command, str):
				self.sub_commands[sub_command] = sub_command
			elif isinstance(sub_command, tuple):
				name, cli_value = sub_command
				self.sub_commands[cli_value] = name
			else:
				raise ValueError('NonpositionalArgumentParser: Internal error, sub_command must be either string or tuple.')
		self.separators = separators
	
	def match_separator(self, args):
		for separator in self.separators:
			if args[0] == separator:
				return args[1:], separator, []
		return None, None, args
	
	def match_nonpositional(self, args):
		for model in self.parameter_models:
			match, args_to_match = model.match(args, self)
			if match is not None:
				return MatchedArgument(model.name, match), args_to_match
		return None, args
		
	def match_sub_command(self, args):
		arg = args[0]
		if arg in self.sub_commands:
			return self.sub_commands[arg], args[1:]
		else:
			return None, args
			
	def matches_anything(self, args):
		_, separator, _ = self.match_separator(args)
		if separator:
			return True
		matched, _ = self.match_nonpositional(args)
		if matched:
			return True
		matched, _ = self.match_sub_command(args)
		if matched:
			return True
		return False
	
	def parse_arguments(self, args):
		args_to_match = args
		matched_nonpositionals = []
		positionals = []
		separator = None
		sub_command = None
		while args_to_match:
			matched, separator, args_to_match = self.match_separator(args_to_match)
			if separator: # if separator:
				positionals += matched
				break
			matched, args_to_match = self.match_nonpositional(args_to_match)
			if matched: # elif nonpositional:
				matched_nonpositionals.append(matched)
				continue
			matched, args_to_match = self.match_sub_command(args_to_match)
			if matched: # elif sub command:
				sub_command = matched
				break
			# else positional:
			positionals.append(args_to_match[0])
			args_to_match = args_to_match[1:]
		return matched_nonpositionals, positionals, separator, sub_command, args_to_match
	
# --------------------- NONPOSITIONAL PARAMETERS MODEL ---------------------
	
def startswith_any(arg, prefixes):
	for prefix in prefixes:
		if arg.startswith(prefix):
			return prefix

def equals_any(arg, prefixes):
	for prefix in prefixes:
		if arg == prefix:
			return prefix
	
class BasicNonpositional:
	def __init__(self, name, prefixes):
		self.name = name
		if isinstance(prefixes, str):
			self.prefixes = [prefixes]
		else:
			self.prefixes = sorted(prefixes, key=len, reverse=True)
	
	def match(self, args, parser):
		arg = args[0]
		prefix = startswith_any(arg, self.prefixes)
		if prefix:
			return arg[len(prefix):], args[1:]
		else:
			return None, args
	
class MultiArgNonpositional:
	def __init__(self, name, prefixes, vars=[], count=1):
		self.name = name
		if isinstance(prefixes, str):
			self.prefixes = [prefixes]
		else:
			self.prefixes = prefixes
		self.vars = vars
		if vars:
			if count != 1 and count != len(vars):
				print('MultiArgNonpositional: warning, internal error, vars list provided, count argument will be ignored.')
			self.count = len(vars)
			self.data_tuple = namedtuple(name, vars)
		else:
			self.count = count
	
	def match(self, args, parser):
		if equals_any(args[0], self.prefixes):
			if self.count == '*':
				if not args[1:]:
					raise Exception('No arguments for <{}>, required at least one.'.format(self.name))
				ret = [args[1]] # take the second arg as ret value
				for idx, arg in enumerate(args[2:]): # for all after the second
					if parser.matches_anything(args[2+idx:]): # break if they match anything
						break
					ret.append(arg) # add to ret value
			else:
				if len(args) < self.count+1:
					raise Exception('Not enough arguments for <{}>, found: {}, required: {}.'.format(self.name, self.count+1 - len(args), self.count))
				if self.count > 1:
					ret = args[1:self.count+1]
				else:
					ret = args[1]
				if self.vars:
					ret = self.data_tuple(*ret)
			matched_count = 1 if self.count == 1 else len(ret)
			return ret, args[matched_count+1:]
		else:
			return None, args
	
class SeparatedNonpositional:
	def __init__(self, name, prefixes, separator=','):
		self.name = name
		if isinstance(prefixes, str):
			self.prefixes = [prefixes]
		else:
			self.prefixes = sorted(prefixes, key=len, reverse=True)
		self.separator = separator
	
	def match(self, args, parser):
		arg = args[0]
		prefix = startswith_any(arg, self.prefixes)
		if prefix:
			value = arg[len(prefix):]
			return value.split(self.separator), args[1:]
		else:
			return None, args
			
class CounterNonpositional:
	def __init__(self, name, prefixes, count_char):
		self.name = name
		if isinstance(prefixes, str):
			self.prefixes = [prefixes]
		else:
			self.prefixes = sorted(prefixes, key=len, reverse=True)
		self.count_char = count_char
	
	def match(self, args, parser):
		arg = args[0]
		prefix = startswith_any(arg, [p+self.count_char for p in self.prefixes])
		if prefix:
			to_count = arg[len(prefix):]
			if len(to_count) == to_count.count(self.count_char): # no other chars
				return len(to_count)+1, args[1:]
		return None, args
	
class BooleanNonpositional:
	def __init__(self, name, positives=[], negatives=[]):
		self.name = name
		if not positives and not negatives:
			raise ValueError('BooleanNonpositional: Internal error, neither positive nor negative string supplied.')
		if isinstance(positives, str):
			self.positives = [positives]
		else:
			self.positives = positives
		if isinstance(negatives, str):
			self.negatives = [negatives]
		else:
			self.negatives = negatives
	
	def match(self, args, parser):
		arg = args[0]
		if equals_any(args[0], self.positives):
			return True, args[1:]
		elif equals_any(args[0], self.negatives):
			return False, args[1:]
		else:
			return None, args

# --------------------- USAGE MODEL ---------------------

class InvalidUsageException(Exception):
	pass
	
class ArgumentRequired(InvalidUsageException):
	pass
	
class InvalidArguments(InvalidUsageException):
	pass
	
class DuplicateArgument(Exception):
	pass

class CommandUsageProcessorContext: # TODO looks bloated, refactor
	def __init__(self, matched_nonpositionals, positional_args, separator, has_subcommand, positionals_to_match=None, checked_nonpositionals=[], matched_positionals=[], subcommand_checked=False):
		self.matched_nonpositionals = matched_nonpositionals # matched_nonpositionals
		self.positional_args = positional_args # positional_args values
		self.positionals_to_match = len(positional_args) if positionals_to_match is None else positionals_to_match
		self.has_subcommand = has_subcommand # True if a subcommand was matched
		self.checked_nonpositionals = checked_nonpositionals # checked nonpositionals names
		self.matched_positionals = matched_positionals # found list of positional MatchedArgument
		self.separator = separator
		self.subcommand_checked = subcommand_checked
	
	def clone(self):
		return CommandUsageProcessorContext(self.matched_nonpositionals, self.positional_args, 
											self.separator, self.has_subcommand, self.positionals_to_match, 
											self.checked_nonpositionals.copy(), self.matched_positionals.copy(), 
											self.subcommand_checked)
	
	def match_next_positional(self, name):
		index = len(self.matched_positionals)
		self.matched_positionals.append(MatchedArgument(name, self.positional_args[index]))
		self.positionals_to_match -= 1
		
	def match_remaining_positionals(self, name):
		index = len(self.matched_positionals)
		self.matched_positionals.append(MatchedArgument(name, self.positional_args[index:]))
		self.positionals_to_match = 0

class ParameterGroup:
	def __init__(self, elements=[]):
		self.elements = elements
	
	def process(self, ctx):
		ctx = ctx.clone() # clone the received context so we can change it without changing the parent element's context
		for element in self.elements:
			ctx = element.process(ctx) # give new context to each sub element
		return ctx

class OrGroup:
	def __init__(self, elements=[]):
		self.elements = elements
	
	def process(self, ctx):
		error_message = "Invalid arguments, errors encountered in mutually exclusive usage patterns:"
		for element in self.elements:
			try:
				return element.process(ctx)
			except InvalidUsageException as ex:
				error_message+='\n\t'+str(ex)
		raise InvalidArguments(error_message)
	
class OptionalElement:
	def __init__(self, element):
		self.element = element
		
	def process(self, ctx):
		try:
			return self.element.process(ctx)
		except InvalidUsageException:
			return ctx

class NonPositionalParameter:
	def __init__(self, name, multiplicity=1):
		self.name = name
		self.multiplicity = multiplicity
	
	def process(self, ctx):
		ctx = ctx.clone()
		matched_args = []
		for idx, matched_arg in enumerate(ctx.matched_nonpositionals):
			if self.name == matched_arg.name:
				matched_args.append((idx, matched_arg))
		if matched_args:
			if not self.multiplicity == '*': # if multiplicity is an int, check if it is exceeded
				if len(matched_args) > self.multiplicity:
					raise DuplicateArgument('Too many arguments <{}>, found {}, maximum {} allowed.'.format(self.name, len(matched_args), self.multiplicity))
			if self.multiplicity != 1: # if multiplicity is more than 1, merge the values into one MatchedArgument
				_, first = matched_args[0] # take first
				first.value = [first.value] # make its value a list
				for i, (idx, arg) in enumerate(matched_args[1:]): # for the rest
					first.value.append(arg.value) # merge with the first one
					del ctx.matched_nonpositionals[idx-i]
			ctx.checked_nonpositionals.append(self.name)
			return ctx
		else:
			raise ArgumentRequired('Argument required: {}'.format(self.name))
	
class PositionalParameter:
	def __init__(self, name, multiplicity=1):
		self.name = name
		self.multiplicity = multiplicity
	
	def process(self, ctx):
		ctx = ctx.clone()
		if not ctx.positionals_to_match > 0:
			raise ArgumentRequired('Argument required: {}'.format(self.name))
		if self.multiplicity == 1:
			ctx.match_next_positional(self.name)
		else: # multiplicity == '*':
			ctx.match_remaining_positionals(self.name)
		return ctx
		
class ParameterSeparator:
	def __init__(self, value):
		self.value = value
	
	def process(self, ctx):
		if self.value == ctx.separator:
			return ctx
		else:
			raise ArgumentRequired('Separator required: {}'.format(self.value))
		
class SubCommand:
	def process(self, ctx):
		ctx = ctx.clone()
		if ctx.has_subcommand:
			ctx.subcommand_checked = True
			return ctx
		else:
			raise ArgumentRequired('Subcommand required')

# --------------------- USAGE MODEL PROCESSOR ---------------------

def process_cli_usage_model(model, matched_nonpositionals, positional_args, separator, sub_command):
	ctx = model.process(CommandUsageProcessorContext(matched_nonpositionals, positional_args, separator, True if sub_command else False))
	if ctx.positionals_to_match:
		raise InvalidArguments('Unknown arguments: {}'.format(ctx.positional_args[-ctx.positionals_to_match:]))
	if len(ctx.matched_nonpositionals) > len(ctx.checked_nonpositionals):
		superfluous_args = [arg for arg in ctx.matched_nonpositionals if arg.name not in ctx.checked_nonpositionals]
		raise InvalidArguments('Invalid arguments, usage pattern recognized, but some arguments are superfluous: {}.\nRecognised parameters: {}'.format(superfluous_args, ctx.checked_nonpositionals + [p.name for p in ctx.matched_positionals]))
	if not ctx.subcommand_checked and ctx.has_subcommand:
		raise InvalidArguments('Invalid arguments, subcommand: <{}> not expected in combination with given arguments.'.format(sub_command))
	return ctx.matched_positionals

# --------------------- CLI ARGS PARSER ---------------------

def parse_cli_args(root_command_name, command_models, args):
	ClassifiedCommandArgs = namedtuple('ClassifiedCommandArgs', ['name', 'matched_nonpositionals', 'positional_args', 'separator', 'sub_command'])
	CommandArgs = namedtuple('CommandArgs', ['args', 'sub_command'])
	args_to_match = args
	commands = []
	command_name = root_command_name
	matched_args = {}
	
	# classify all args into subcommands, and further into matched nonpositionals and positionals that are left to be matched
	while command_name:
		if args_to_match: # there are more arguments
			command_model = command_models[command_name]
			parser = NonpositionalArgumentParser(command_model.parameter_models, command_model.sub_commands, command_model.separators)
			matched_nonpositionals, positional_args, separator, sub_command, args_to_match = parser.parse_arguments(args_to_match)
		else: # no more arguments, just add the last command and finish
			matched_nonpositionals = []
			positional_args = []
			separator = None
			sub_command = None
		
		commands.append(ClassifiedCommandArgs(command_name, matched_nonpositionals, positional_args, separator, sub_command))
		command_name = sub_command
	
	# traverse the cli model tree, check if nonpositionals satisfy the constraints, pair the positionals accordingly
	for command in commands:
		command_name = command.name
		command_model = command_models[command_name]
		
		matched_positionals = process_cli_usage_model(command_model.usage_model, command.matched_nonpositionals, command.positional_args, command.separator, command.sub_command)
		
		all_matched_args = command.matched_nonpositionals + matched_positionals # matched positional and nonpositional args
		matched_names = [matched.name for matched in all_matched_args] # names of all matched args
		for missing_arg in [arg_name for arg_name in command_model.default_values if arg_name not in matched_names]: # for all args in defaults not present in matched args
			all_matched_args.append(MatchedArgument(missing_arg, command_model.default_values[missing_arg])) # add default values
		
		all_matched_args = [convert_data(arg, command_model.parameter_types[arg.name], command_model.date_formats.get(arg.name, None)) for arg in all_matched_args]
		
		matched_args[command_name] = CommandArgs(all_matched_args, command.sub_command)
	
	return matched_args
	
def print_builtin_help(root_command_name, command_models, args):
	if not args:
		return False
	
	command_name = root_command_name
	command_model = command_models[command_name]
	if len(args) > 1:
		for arg in args[:-2]: # match commands until the last two args
			if arg in command_model.sub_commands:
				command_name = arg
				command_model = command_models[command_name]
			else:
				return False
		
		if args[-2] in command_model.sub_commands: # check if the second last arg is a command
			command_name = args[-2]
			command_model = command_models[command_name]
			help_arg = args[-1] # the last one should be a help arg
			long_help_arg = None # there is no long help arg
		else:
			help_arg = args[-2] # the second last should be help arg
			long_help_arg = args[-1] # the last arg should be long help arg
	else:
		help_arg = args[0]
		long_help_arg = None
	
	if help_arg in command_model.builtin_help_params and (not long_help_arg or long_help_arg in command_model.builtin_long_help_params): # check help_arg and long_help_arg if present
		if long_help_arg:
			print(command_model.long_usage_help)
		else:
			print(command_model.usage_help)
		return True
	else:
		return False
	
def invoke_commands(command_callbacks, root_command_name, command_models, args):
	if isinstance(command_callbacks, list):
		command_callbacks = {f.__name__ : f for f in command_callbacks}
	
	if print_builtin_help(root_command_name, command_models, args):
		return
	
	matched_args = parse_cli_args(root_command_name, command_models, args) # TODO convert to primitive values based on param type
	
	command_name = root_command_name
	while command_name:
		command = matched_args[command_name]
		command_model = command_models[command_name]
		if command:
			command_callbacks[command_name](command.args, command.sub_command)
			command_name = command.sub_command
		else:
			raise Exception('No callback provided for command: {}'.format(command_name))

	
# ------------------------------ TO BE GENERATED DATA ------------------------------
'''
root_command_name = 'root_command'
command_models = {
	'root_command' : CommandParserModel(
		parameter_models=[
			BooleanNonpositional('option1', ['--option1', '-o1']),
			BooleanNonpositional('option2', '--option2'),
			BooleanNonpositional('option3', '--option3'),
			BooleanNonpositional('option4', '--option4'),
			BooleanNonpositional('option5', '--option5'),
			BooleanNonpositional('option6', '--option6'),
			MultiArgNonpositional('param1', '--param1'),
		],
		usage_model=ParameterGroup([ # [--option1] [--option2] --param1 <param1-value> <positional1> (--option3 --option4 [<positional2>])|(--option5) [--option6 <subcommand>]
			OptionalElement(NonPositionalParameter('option1')), 
			OptionalElement(NonPositionalParameter('option2')), 
			NonPositionalParameter('param1', 2), 
			PositionalParameter('positional1'), 
			OrGroup([
				ParameterGroup([
					NonPositionalParameter('option3'),
					NonPositionalParameter('option4'),
					OptionalElement(PositionalParameter('positional2')), 
				]),
				NonPositionalParameter('option5'),
			]),
			OptionalElement(ParameterGroup([NonPositionalParameter('option6'), SubCommand()])),
		]),
		default_values={
			'option1' : False,
			'option2' : False,
			'option3' : False,
			'option4' : False,
			'option5' : False,
			'option6' : False,
			'param1' : "",
			'positional1' : "",
			'positional2' : "",
		},
		usage_help="root_command help",
		long_usage_help="root_command long_usage_help",
		sub_commands=['subcommand1', 'subcommand2'],
	),
	'subcommand1' : CommandParserModel(
		parameter_models=[
			BooleanNonpositional('option1', '--option1'),
			BooleanNonpositional('option2', '--option2'),
		],
		usage_model=ParameterGroup([
			NonPositionalParameter('option1'), 
			OptionalElement(NonPositionalParameter('option2')),
		]),
		default_values={
			'option1' : False,
			'option2' : False,
		},
		usage_help="subcommand1 help",
		long_usage_help="subcommand1 long_usage_help",
	),
	'subcommand2' : CommandParserModel(
		parameter_models=[
			BooleanNonpositional('option3', '--option3'),
			BooleanNonpositional('option4', '--option4'),
		],
		usage_model=ParameterGroup([
			NonPositionalParameter('option3'), 
			OptionalElement(NonPositionalParameter('option4')),
		]),
		default_values={
			'option3' : False,
			'option4' : False,
		},
		usage_help="subcommand2 help",
		long_usage_help="subcommand2 long_usage_help",
	),
}
# --------------------------------------------------------------

# -------------- TEST --------------
if __name__ == '__main__':
	args = "--param1 param1_value1 --param1 param1_value2 -o1 --option5 positional1 --option6 subcommand1 --option1".split()
	args_help = "subcommand1 -h".split()
	matched_args = parse_cli_args(root_command_name, command_models, args)
	print(matched_args, '\n\n')
	def dummy_print_callback(args, sub_command):
		print('dummy callback:\n\t', args, '\n\tsub_command: {}'.format(sub_command))
	invoke_commands({'root_command':dummy_print_callback, 'subcommand1':dummy_print_callback, 'subcommand2':dummy_print_callback}, root_command_name, command_models, args)
'''