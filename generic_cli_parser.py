
'''
nadjem sve nepozicione koji postoje
matchujem sve positional/nonpositional redom dok ne matchujem subcommand
kad matchujem subcommand proveravam ovu, ako je ok prosledjujem ostatak argumenata procesoru za subcommand
cekiram dal je ok stablo za komandu:
	- group cekiram sve redom [v]
	- nonpositional cekiram dal je prisutan [v]
	- positional pretpostavim da je sledeci od prepoznatih, ako fali exception [v]
	- optional cekiram group, ako failuje ne puca, samo ignorise [v]
	- or expression idem redom i cekiram group, prvi koji uspe vratim, ako ne uspe ni jedan exception [v]
ako pukne sastavim poruku zasto je puklo i prosledim gore, ako pukne root ispisem poruku
ako ne pukne proverim dal ima viska nonpositional il positional, ako ima viska positional kazem unknown, ako ima viska nonpositional dodam u poruku wrong arguments i ispisem sve

multiplicity: number|'*'
string..:
	--nesto={}
	--nesto {}
	--nesto {n}
	--nesto {*}
	--nesto={*|separator}
	--nesto {'x', 'y'}
boolean:
	--nesto|--not-nesto
	--nesto
	|--not-nesto
number:
	--nesto{count:c}

TODO:
	- aliasi [v]
	- default vrednosti [v]
	- description i help [v]
	- ogranicenja []
'''
	
from collections import namedtuple
from datetime import datetime
from functools import reduce
from operator import add
from inspect import getfullargspec
from types import MethodType, BuiltinMethodType

class CommandParserModel:
	def __init__(self, id, name, cli_command, parameter_models=[], usage_model=None, usage_help='', long_usage_help='', sub_commands=[], 
			separators=['--'], builtin_help_params=['--help', '-h'], builtin_long_help_params=['--all', '-a']):
		self.id = id
		self.name = name
		self.cli_command = cli_command
		self.parameter_models = {m.name:m for m in parameter_models}
		nonpositional_models = [p.parser_models for p in parameter_models if p.parser_models]
		self.parameter_parser_models = reduce(add, [p.parser_models for p in parameter_models if p.parser_models]) if nonpositional_models else []
		self.usage_model = usage_model
		self.sub_commands = sub_commands
		self.separators = separators
		self.usage_help = usage_help
		self.long_usage_help = long_usage_help
		self.builtin_help_params = builtin_help_params
		self.builtin_long_help_params = builtin_long_help_params
		
class ParameterModel:
	def __init__(self, name, type, usage_model, default, parser_models=None, date_format=None, cli_pattern_vars=[]):
		self.name = name
		self.type = type
		self.usage_model = usage_model
		self.default = default
		self.parser_models = parser_models
		self.date_format = date_format
		self.cli_pattern_vars = cli_pattern_vars
		
class MatchedArgument:
	def __init__(self, name, value):
		self.name = name
		self.value = value
		
	def __eq__(self, other):
		return self.name == other.name
		
	def __repr__(self):
		if isinstance(self.value, str):
			val = "'{}'".format(self.value)
		else:
			val = self.value
		return "<{name} = {value}>".format(name=self.name, value=val)
		
# --------------------- NONPOSITIONAL ARGUMENT PARSER ---------------------

class NonpositionalArgumentParser:
	def __init__(self, parameter_parser_models=[], sub_commands={}, separators=['--']):
		self.parameter_parser_models = parameter_parser_models
		self.sub_commands = sub_commands
		self.separators = separators
	
	def match_separator(self, args):
		for separator in self.separators:
			if args[0] == separator:
				return args[1:], separator, []
		return None, None, args
	
	def match_nonpositional(self, args):
		for model in self.parameter_parser_models:
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
	def __init__(self, name, prefixes, count=1):
		self.name = name
		if isinstance(prefixes, str):
			self.prefixes = [prefixes]
		else:
			self.prefixes = prefixes
		self.count = count
	
	def match(self, args, parser):
		if equals_any(args[0], self.prefixes):
			if self.count == '*':
				if not args[1:]:
					raise ArgumentRequired('No arguments for <{}>, required at least one.'.format(self.name))
				ret = [args[1]] # take the second arg as ret value
				for idx, arg in enumerate(args[2:]): # for all after the second
					if parser.matches_anything(args[2+idx:]): # break if they match anything
						break
					ret.append(arg) # add to ret value
			else:
				if len(args) < self.count+1:
					raise ArgumentRequired('Not enough arguments for <{}>, found: {}, required: {}.'.format(self.name, self.count+1 - len(args), self.count))
				if self.count > 1:
					ret = args[1:self.count+1]
				else:
					ret = args[1]
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

class CommandUsageProcessorContext:
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
		elif self.multiplicity == '*':
			ctx.match_remaining_positionals(self.name)
		else:
			raise Exception("PositionalParameter: Internal error, positional multiplicity can be either 1 or '*'.")
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

def process_cli_usage_model(model, matched_nonpositionals, positional_args, separator, sub_command_id):
	ctx = model.process(CommandUsageProcessorContext(matched_nonpositionals, positional_args, separator, True if sub_command_id else False))
	if ctx.positionals_to_match:
		raise InvalidArguments('Unknown arguments: {}'.format(ctx.positional_args[-ctx.positionals_to_match:]))
	if len(ctx.matched_nonpositionals) > len(ctx.checked_nonpositionals):
		superfluous_args = [arg for arg in ctx.matched_nonpositionals if arg.name not in ctx.checked_nonpositionals]
		raise InvalidArguments('Invalid arguments, usage pattern recognized, but some arguments are superfluous: {}.\nRecognised parameters: {}'.format(superfluous_args, ctx.checked_nonpositionals + [p.name for p in ctx.matched_positionals]))
	if not ctx.subcommand_checked and ctx.has_subcommand:
		raise InvalidArguments('Invalid arguments, subcommand: <{}> not expected in combination with given arguments.'.format(sub_command_id))
	return ctx.matched_positionals

# --------------------- CLI ARGS PARSER ---------------------

def parse_cli_args(root_command_id, command_models, args):
	ClassifiedCommandArgs = namedtuple('ClassifiedCommandArgs', ['model', 'matched_nonpositionals', 'positional_args', 'separator', 'sub_command_id'])
	CommandArgs = namedtuple('CommandArgs', ['args', 'sub_command_id'])
	args_to_match = args
	commands = []
	command_id = root_command_id
	matched_args = {}
	
	# classify all args into subcommands, and further into matched nonpositionals and (to be matched) positionals
	while command_id:
		command_model = command_models[command_id]
		if args_to_match: # there are more arguments
			sub_commands = {sc.cli_command:sc.id for sc in command_model.sub_commands}
			parser = NonpositionalArgumentParser(command_model.parameter_parser_models, sub_commands, command_model.separators)
			matched_nonpositionals, positional_args, separator, sub_command_id, args_to_match = parser.parse_arguments(args_to_match)
		else: # no more arguments, just add the last command and finish
			matched_nonpositionals = []
			positional_args = []
			separator = None
			sub_command_id = None
		
		commands.append(ClassifiedCommandArgs(command_model, matched_nonpositionals, positional_args, separator, sub_command_id))
		command_id = sub_command_id
	
	# traverse the cli model tree, check if nonpositionals satisfy the constraints, pair the positionals accordingly
	for command in commands:
		command_model = command.model
		
		matched_positionals = process_cli_usage_model(command_model.usage_model, command.matched_nonpositionals, command.positional_args, command.separator, command.sub_command_id)
		
		all_matched_args = command.matched_nonpositionals + matched_positionals # matched positional and nonpositional args
		matched_names = [matched.name for matched in all_matched_args] # names of all matched args
		for missing_arg in [p for p in command_model.parameter_models.values() if p.name not in matched_names]: # for all args not present in matched args
			all_matched_args.append(MatchedArgument(missing_arg.name, missing_arg.default)) # add default values
		
		for arg in all_matched_args:
			arg.value = convert_data(arg.value, command_model.parameter_models[arg.name])
		
		matched_args[command_model.id] = CommandArgs(all_matched_args, command.sub_command_id)
	
	return matched_args
	
def convert_data(data, model):
	if hasattr(data, '__iter__') and not isinstance(data, str):
		ret = [convert_data(element, model) for element in data]
		if model.cli_pattern_vars:
			ret = namedtuple(model.name, model.cli_pattern_vars)(*ret)
		return ret
	elif isinstance(data, str):
		if model.type == "Num":
			try:
				return int(data)
			except ValueError:
				return float(data)
		elif model.type == "Date":
			if not data:
				return datetime.now()
			return datetime.strptime(data, model.date_format)
		elif model.type == "Bool":
			return {"true":True, "false":False}[data.lower()]
	
	return data

def invoke_commands(command_callbacks, root_command_id, command_models, args):
	def get_cmd_callback(command_id, commands):
		val = commands.get(command_id, None)
		if not val:
			return None, None
		if isinstance(val, tuple):
			return val
		else:
			return val, None
	
	if print_builtin_help(root_command_id, command_models, args):
		return
	
	matched_args = parse_cli_args(root_command_id, command_models, args)
	
	cmd_callback, sub_commands = command_callbacks
	command_id = root_command_id
	
	while command_id:
		command = matched_args[command_id]
		
		args_count = len(getfullargspec(cmd_callback).args)
		if isinstance(cmd_callback, (MethodType, BuiltinMethodType)):
			args_count -= 1
		if args_count == 1:
			cmd_callback(command.args)
		else:
			cmd_callback(command.args, command.sub_command_id)
		
		if command.sub_command_id:
			cmd_callback, sub_commands = get_cmd_callback(command_models[command.sub_command_id].name, sub_commands)
			if not cmd_callback:
				raise Exception('No callback provided for command: {}'.format(command.sub_command_id))
			command_id = command.sub_command_id
		else:
			command_id = None
			
def print_builtin_help(root_command_id, command_models, args):
	if not args:
		return False
	
	command_id = root_command_id
	command_model = command_models[command_id]
	
	matched_sub_commands = []
	left_to_match = []
	
	for idx, arg in enumerate(args):
		for sub_command in command_model.sub_commands:
			if sub_command.cli_command == arg:
				matched_sub_commands.append(sub_command)
				left_to_match = []
				command_model = sub_command
				break
		else:
			left_to_match.append(arg)
	
	if any((p in left_to_match) for p in command_model.builtin_help_params):
		if any((p in left_to_match) for p in command_model.builtin_long_help_params):
			print(command_model.long_usage_help)
		else:
			print(command_model.usage_help)
		return True
	else:
		return False
