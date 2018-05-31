from collections import OrderedDict

PRIMITIVE_PYTHON_TYPES = [int, float, str, bool]


class ModelPrinter:
    def __init__(self, omitted_attributes=[], primitive_types=PRIMITIVE_PYTHON_TYPES, indent_str='    ', indent_separator='|', name_attr='name', parent_attr='parent',
                 print_empty_attrs=False, print_empty_lists=False, print_list_index=False, print_parent_attr=False, print_func=print):
        self.printed = []
        self.omitted_attributes = omitted_attributes + [name_attr]
        if not print_parent_attr:
            self.omitted_attributes.append(parent_attr)
        self.primitive_types = primitive_types
        self.indent_str = indent_str
        self.indent_separator = indent_separator
        self.name_attr = name_attr
        self.parent_attr = parent_attr
        self.print_empty_attrs = print_empty_attrs
        self.print_empty_lists = print_empty_lists
        self.print_list_index = print_list_index
        self.print = print_func

    def indent(self, level=0):
        return self.indent_separator.join(level * [self.indent_str])

    def multiline_indent(self, text, level=0, start_from=1):
        return '\n'.join([self.indent(level) + line if idx + 1 >= start_from else line for idx, line in enumerate(text.split('\n'))])

    def model_path(self, model):
        name = self.get_attr_name(model) or model.__class__.__name__

        if hasattr(model, self.parent_attr):
            parent_path = self.model_path(getattr(model, self.parent_attr))
            return parent_path + '/' + name
        else:
            return '/' + name

    def get_attr_name(self, model):
        if hasattr(model, self.name_attr):
            return getattr(model, self.name_attr)

    def print_model(self, model):
        self.printed = []
        self._print_model(model)

    def _print_model(self, model, external_name=None, indent_level=0):

        # if the model is an empty list and we should not print empty lists
        # or the model is None and we should not print empty attributes, just return
        if (isinstance(model, list) and not model and not self.print_empty_lists) or (not self.print_empty_attrs and not model):
            return

        name = external_name or self.get_attr_name(model) or ''

        if model is None:
            self.print(self.indent(indent_level) + '{name}None'.format(name=name+'=' if name else ''))
        elif isinstance(model, (list, set)):
            self.print(self.indent(indent_level) + '{name}([{length}]):'.format(name=name, length=len(model)))
            for idx, element in enumerate(model):
                if self.print_list_index:
                    self.print(self.indent(indent_level + 1) + '[{index}] ----'.format(index=idx))
                self._print_model(element, indent_level=indent_level + 1)
                if not self.print_list_index and idx < len(model) - 1:
                    self.print(self.indent(indent_level + 1) + '----')
        elif type(model) in self.primitive_types:
            if isinstance(model, str):
                if '\n' in model:
                    model = '\n' + self.multiline_indent("\"\"\"\n{text}\n\"\"\"".format(text=model), indent_level + 1)
                else:
                    model = "'{string}'".format(string=model)
                    self.print(self.indent(indent_level) + '{name}{value}'.format(name=name+'=' if name else '', value=model))
        else:
            if model in self.printed:
                self.print(self.indent(indent_level) + '{name}[{path}]'.format(name=external_name+'=' if external_name else '', path=self.model_path(model)))
            else:
                self.printed.append(model)
                all_attrs = OrderedDict([attr_name, getattr(model, attr_name)] for attr_name in dir(model) if not attr_name.startswith('_') and not callable(getattr(model, attr_name)))
                inline_repr = repr(model) if not all_attrs else ''
                self.print(self.indent(indent_level) + '{name}({cls}):{inline}'.format(name=name, cls=model.__class__.__name__, inline=inline_repr))
                if all_attrs:
                    for attr_name, attr_value in all_attrs.items():
                        if attr_name not in self.omitted_attributes:
                            self._print_model(attr_value, attr_name, indent_level + 1)


def print_model(model, *args, **kwargs):
    ModelPrinter(*args, **kwargs).print_model(model)
