
from inspect import getfullargspec
from types import MethodType, BuiltinMethodType
from contextlib import contextmanager
from collections import namedtuple, defaultdict
from operator import add
from functools import reduce

from common import *

'''
@total_ordering
class ProcessorFunction:
	def __init__(self, name, func, attrs=[], adds=[], dels=[], requires=[]):
		if isinstance(type, list):
			self.type = type
		else:
			self.type = [type]
		self.name = name
		add_attrs = lambda attr_list, type_list: reduce(add, [['{}.{}'.format(t, attr) for attr in attr_list] for t in type_list])
		self.attrs = add_attrs(attrs, self.type)
		self.adds = add_attrs(adds, self.type)
		self.dels = add_attrs(dels, self.type)
		self.requires = requires
		
	def __call__(self, *args, **kwargs):
		return self.func(*args, **kwargs)
		
	def __eq__(self, other):
		if self.name == other.name:
			return True
		# True if self and other are not in each others requires list and there is no intersection between what self and other add or remove and what they require
		return self.name not in other.requires and other.name not in self.requires \
			and set(self.attrs).isdisjoint(set(other.adds)) and set(other.attrs).isdisjoint(set(self.adds)) \
			and set(self.attrs).isdisjoint(set(other.dels)) and set(other.attrs).isdisjoint(set(self.dels))
		
	def __lt__(self, other):
		# True if self has to go before other or self adds any of others required attrs or other deletes any of self required attrs
		return self.name in other.requires or any([a in self.adds for a in other.attrs]) or any([a in other.dels for a in self.attrs])
		
class ProcessorInvoker:
	def __init__(self, callbacks=[]):
		self.callbacks = callbacks
		
	def invoke(model):
		sorted_callbacks = sorted(self.callbacks)
		partitioned_callbacks = [[]]
		for callback in sorted_callbacks:
			last_partition = partitioned_callbacks[-1]
			if not last_partition or all(callback == c for c in last_partition):
				last_partition.append(callback)
			else:
				partitioned_callbacks.append([callback])
		
		for partition in partitioned_callbacks:
			partitioned_by_type = defaultdict(list)
			for callback in partition:
				for type in callback.type:
					partitioned_by_type[type].append(callback)
			ModelProcessor(partitioned_by_type).process_model(model)
			
	def add_callback(self, func, type, name, attrs=[], adds=[], dels=[], requires=[]):
		self.processor(type, name, attrs, adds, dels, requires)(func)
	
	def processor(self, type, name=None, attrs=[], adds=[], dels=[], requires=[]):
		def processor_decorator(func):
			if not name:
				name = func.__name__
			wrapped_func = ProcessorFunction(name, func, attrs, adds, dels requires)
			self.callbacks.append(wrapped_func)
			return wrapped_func
		return processor_decorator
'''		
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
							self.callbacks[key] = [existing, value]
					else:
						self.callbacks[key] = value
		else:
			self.callbacks = callbacks
		
		self.allow_revisiting = allow_revisiting
		self.parent_stack = []
		self.visited = []
		
	@contextmanager
	def parent(self, model):
		self.parent_stack.append(model)
		yield model
		self.parent_stack.pop()
		
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
		with self.parent(model):
			for import_statement in model.imports:
				self.invoke(import_statement)
			for element in model.elements:
				if element_type(element) == 'Parameter':
					self.process_parameter(element)
				elif element_type(element) == 'Command':
					self.process_command(element)
		self.invoke(model)
		
	def process_parameter(self, parameter):
		with self.parent(parameter):
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
		self.invoke(parameter)
		
	def process_command(self, command):
		with self.parent(command):
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
		self.invoke(command)
				
	def process_cli_group(self, group):
		with self.parent(group):
			for element in group.elements:
				if hasattr(element, 'elements'):
					self.process_cli_group(element)
				else:
					self.invoke(element)
		self.invoke(group)
		
	def process_gui_structure(self, gui_structure):
		with self.parent(gui_structure):
			for element in gui_structure.elements:
				self.process_gui_element(element)
		self.invoke(gui_structure)
		
	def process_gui_element(self, gui_element):
		with self.parent(gui_element):
			if element_type(gui_element) == 'GuiTabs':
				for tab in gui_element.elements:
					self.process_gui_tab(tab)
			elif element_type(gui_element) == 'GuiSectionGroup':
				for section in gui_element.elements:
					self.process_gui_element(section)
			elif element_type(gui_element) == 'GuiSection':
				self.process_gui_structure(gui_element.body)
			elif element_type(gui_element) == 'GuiGrid':
				for row in gui_element.elements:
					self.process_gui_grid_row(row)
			elif element_type(gui_element) == 'GuiGridRow':
				self.process_gui_grid_row(gui_element)
			elif element_type(gui_element) == 'Parameter':
				self.process_parameter(gui_element)
			elif element_type(gui_element) == 'ParameterReference':
				self.invoke(gui_element)
		self.invoke(gui_element)
		
	def process_gui_grid_row(self, gui_grid_row):
		with self.parent(gui_grid_row):
			for element in gui_grid_row.elements:
				if element_type(element) == 'Parameter':
					self.process_parameter(element)
				elif element_type(element) == 'ParameterReference':
					self.invoke(element)
		self.invoke(gui_grid_row)
		
	def process_gui_tab(self, gui_tab):
		with self.parent(gui_tab):
			self.process_gui_structure(gui_tab.body)
		self.invoke(gui_tab)
		