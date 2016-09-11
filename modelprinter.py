
from collections import OrderedDict

PRIMITIVE_PYTHON_TYPES = [int, float, str, bool]

class ModelPrinter:
	def __init__(self, omitted_attributes=[], primitive_types=[int, float, str, bool], indent_str='    ', indent_separator='|', name_attr='name', parent_attr='parent', 
						print_empty_attrs=False, print_empty_lists=False, print_list_index=False):
		self.printed = []
		self.omitted_attributes = [parent_attr, name_attr] + omitted_attributes
		self.primitive_types = primitive_types
		self.indent_str = indent_str
		self.indent_separator = indent_separator
		self.name_attr = name_attr
		self.parent_attr = parent_attr
		self.print_empty_attrs = print_empty_attrs
		self.print_empty_lists = print_empty_lists
		self.print_list_index = print_list_index
	
	def indent(self, level=0):
		return self.indent_separator.join(level*[self.indent_str])
		
	def multiline_indent(self, text, level=0, start_from=1):
		return '\n'.join([self.indent(level)+line if idx+1 >= start_from else line for idx, line in enumerate(text.split('\n'))])
	
	def model_path(self, model):
		name = getattr(model, self.name_attr) if hasattr(model, self.name_attr) else model.__class__.__name__
		if hasattr(model, self.parent_attr):
			parent_path = self.model_path(getattr(model, self.parent_attr))
			return parent_path+'/'+name
		else:
			return '/'+name
	
	def printmodel(self, model):
		self.printed = []
		self._printmodel(model)
	
	def _printmodel(self, model, name=None, indent_level=0):
		
		if (isinstance(model, list) and not self.print_empty_lists and not model) or (not self.print_empty_attrs and not model):
			return
		
		has_name = name is not None
		if not name and hasattr(model, self.name_attr):
			name = getattr(model, self.name_attr)
		if isinstance(model, (list, set)):
			print(self.indent(indent_level)+'{name}({length}):'.format(name=name, length=len(model)))
			for idx, el in enumerate(model):
				if self.print_list_index:
					print(self.indent(indent_level+1)+'[{index}] ----'.format(index=idx))
				self._printmodel(el, None, indent_level+1)
				if not self.print_list_index and idx < len(model)-1:
					print(self.indent(indent_level+1)+'----')
		elif type(model) in self.primitive_types:
			if isinstance(model, str):
				if '\n' in model:
					model = '\n'+self.multiline_indent("\"\"\"\n{text}\n\"\"\"".format(text=model), indent_level+1)
				else:
					model = "'{string}'".format(string=model)
			if name:
				print(self.indent(indent_level)+'{name}={value}'.format(name=name, value=model))
			else:
				print(self.indent(indent_level)+str(model))
		else:
			if model in self.printed:
				if model is None:
					print(self.indent(indent_level)+'{name}=None'.format(name=name))
				else:
					if has_name:
						print(self.indent(indent_level)+'{name}=[{path}]'.format(name=name, path=self.model_path(model)))
					else:
						print(self.indent(indent_level)+'[{path}]'.format(path=self.model_path(model)))
			else:
				self.printed.append(model)
				all_attrs = OrderedDict([attr, getattr(model, attr)] for attr in dir(model) if not attr.startswith('_') and not callable(getattr(model, attr)))
				inline_repr = repr(model) if not all_attrs else ''
				if name:
					print(self.indent(indent_level)+'{name}({cls}):{inline}'.format(name=name, cls=model.__class__.__name__, inline=inline_repr))
				else:
					print(self.indent(indent_level)+'{cls}:{inline}'.format(cls=model.__class__.__name__, inline=inline_repr))
				if all_attrs:
					for k,v in all_attrs.items():
						if k not in self.omitted_attributes:
							self._printmodel(v, k, indent_level+1)
						
def print_model(model, *args, **kwargs):
	ModelPrinter(*args, **kwargs).printmodel(model)
	