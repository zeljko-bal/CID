import textwrap
from functools import reduce
from os.path import join, dirname, realpath

from jinja2 import Environment, FileSystemLoader
from textx.exceptions import TextXSemanticError

from cid.common.utils import element_type


_cli_templates_path = join(dirname(realpath(__file__)), 'templates')


# ------------------------------- CLI MODEL PROCESSORS -------------------------------

class ParameterProcessor:
    def __init__(self):
        self.all_prefixes = []

    def process_parameter(self, parameter):
        self.transform(parameter)
        self.defaults(parameter)
        self.check(parameter)

    @staticmethod
    def transform(parameter):
        # fill parameter.prefixes, parameter.pos_prefixes, parameter.neg_prefixes
        if parameter.nonpositional:
            str_patterns = [p for p in parameter.all_patterns if element_type(p) == 'StringParamPattern']
            pos_patterns = [p for p in parameter.all_patterns if
                            element_type(p) in ['BoolWithPositivePattern', 'BoolNegativeOnlyPattern'] and p.positive]
            neg_patterns = [p for p in parameter.all_patterns if
                            element_type(p) in ['BoolWithPositivePattern', 'BoolNegativeOnlyPattern'] and p.negative]

            if parameter.type == 'Bool':
                parameter.pos_prefixes = [p.positive for p in pos_patterns]
                parameter.neg_prefixes = [p.negative for p in neg_patterns]
                parameter.prefixes = parameter.pos_prefixes + parameter.neg_prefixes
            else:
                parameter.prefixes = [p.prefix for p in str_patterns]

        # fill parameter.usage_repr
        if parameter.nonpositional:
            if pos_patterns:
                repr_pattern = max(pos_patterns, key=lambda p: len(p.positive))  # longest positive
                parameter.usage_repr, _ = cli_pattern_repr(repr_pattern)
            elif neg_patterns:
                repr_pattern = max(neg_patterns, key=lambda p: len(p.negative))  # longest negative
                _, parameter.usage_repr = cli_pattern_repr(repr_pattern)
            elif str_patterns:
                repr_pattern = max(str_patterns, key=lambda p: len(p.prefix))  # longest prefix
                parameter.usage_repr = cli_pattern_repr(repr_pattern)
        else:
            parameter.usage_repr = "<{name}>{mult}".format(name=parameter.name.upper(), mult='...' if parameter.multiplicity == '*' else '')

    @staticmethod
    def defaults(parameter):
        if '{default_desc}' in parameter.description:
            pretty_type = {
                "Str": "String",
                "Num": "Number",
                "Bool": "Boolean",
                "Date": "Date",
                "File": "File",
                "Choice": "Choice",
            }[parameter.type]
            default_description = "Data type: {}.".format(pretty_type)
            if parameter.default:
                default_description += " Default value: {}.".format(
                    "'{}'".format(parameter.default) if isinstance(parameter.default, str) else parameter.default)
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

    def check(self, parameter):
        if parameter.nonpositional:
            # check for duplicate prefixes
            for prefix in parameter.prefixes:
                if prefix in self.all_prefixes:
                    raise TextXSemanticError("Found duplicate cli prefixes for parameter: '{}'.".format(parameter.id))
                self.all_prefixes.append(prefix)
        else:
            if parameter.type == 'Bool':
                raise TextXSemanticError("Found positional parameter of type 'Bool': '{}'.".format(parameter.id))


def cli_pattern_repr(pattern):
    if element_type(pattern) == 'StringParamPattern':
        if pattern.count_char:
            return '{pref}{count_char}'.format(pref=pattern.prefix, count_char=pattern.count_char)
        else:
            if pattern.vars:
                type_str = ' '.join(pattern.vars)
            else:
                type_str = pattern.parent.type
            if pattern.count and not pattern.vars:
                type_str = ' '.join([type_str] * pattern.count)
            if pattern.count_many:
                if pattern.separator:
                    count_repr = '...[{separator}]'.format(separator=pattern.separator)
                else:
                    count_repr = '...'
            else:
                count_repr = ''
            return '{pref}{space}<{type}{count}>'.format(
                pref=pattern.prefix, space=pattern.white_space * ' ', type=type_str.upper(), count=count_repr)
    else:
        if pattern.positive and pattern.negative:
            return pattern.positive, pattern.negative
        elif pattern.positive:
            return pattern.positive, None
        elif pattern.negative:
            return None, pattern.negative


_parameter_processor_visitor = {'Parameter': ParameterProcessor().process_parameter}


# -------------------------------

def get_group_elements_usage_repr(group):
    return [el.string_repr if hasattr(el, 'string_repr') else el.usage_repr for el in group.elements]


def cli_structure_usage_repr(group):
    str_elements = get_group_elements_usage_repr(group)
    group.string_repr = ' '.join(str_elements) + (' <sub_command>' * group.has_subcommand)


def cli_group_usage_repr(group):
    str_elements = get_group_elements_usage_repr(group)
    group.string_repr = '(' + ' '.join(str_elements) + ')'


def cli_optional_group_usage_repr(group):
    str_elements = get_group_elements_usage_repr(group)
    group.string_repr = '[' + ' '.join(str_elements) + ']'


def cli_or_group_usage_repr(group):
    str_elements = get_group_elements_usage_repr(group)
    group.string_repr = '|'.join(str_elements)


_usage_repr_visitor = {'CliStructure': cli_structure_usage_repr, 'CliGroup': cli_group_usage_repr,
                       'CliOptionalGroup': cli_optional_group_usage_repr, 'CliOrGroup': cli_or_group_usage_repr}


# -------------------------------

def add_builtin_help(command, parent_elements):
    if not command.help_params and not command.no_help:
        command.help_params = ['-h', '--help']

    if not command.long_help_params and not command.no_long_help:
        command.long_help_params = ['-a', '--all']

    if not set(command.help_params).isdisjoint(set(command.long_help_params)):
        raise TextXSemanticError("Found same parameters in help_params and long_help_params for command: '{}'".format(command.id))

    resolve_builtin_help_params(command)

    parent_commands = [parent for parent in parent_elements if element_type(parent) == 'Command']
    command.usage_help = generate_usage_help(command, parent_commands)
    command.long_usage_help = generate_usage_help(command, parent_commands, long=True)


def resolve_builtin_help_params(command):
    for param in command.parameters:  # remove all help params with the same prefixes as other already existing params
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
    common_subcommand_help_params = reduce(lambda x, y: x.intersection(y), [set(c.help_params) for c in command.sub_commands]) if command.sub_commands else set()
    common_subcommand_help = common_subcommand_help_params.pop() if common_subcommand_help_params else None

    return _usage_help_template.render(command=command, parents=parents, long=long, command_str=command_str, common_subcommand_help=common_subcommand_help)


def generate_parameters_usage_help(command, long, command_str):
    rows = []
    # col_length = 0
    # desc_col_width = 50  # TODO config for width or dynamic width

    parameters = reduce(lambda x, y: x.union(y), [u.sub_elements for u in command.usages])

    for param in parameters:
        param_patterns_repr = generate_param_patterns_repr(param)
        rows.append((param_patterns_repr, param.description))
        if long and param.help:
            rows.append(('', param.help))

    if command.help_params:
        help_params_repr = ', '.join(command.help_params)
        # col_length = max(len(help_params_repr), col_length)
        if command.long_help_params:
            if long:
                long_help_desc = " For this help message type: {cmd} {help_p} {long_help_p}."\
                    .format(cmd=command_str, help_p=command.help_params[0], long_help_p=command.long_help_params[0])
                if len(command.long_help_params) > 1:
                    long_help_desc += " All detailed help parameters: {long_help_p}.".format(
                        long_help_p=', '.join(command.long_help_params))
            else:
                long_help_desc = " For more detailed help type: {cmd} {help_p} {long_help_p}."\
                    .format(cmd=command_str, help_p=command.help_params[0], long_help_p=command.long_help_params[0])
        else:
            long_help_desc = ''

        if long:
            help_desc = "Shows a shorter help message."
        else:
            help_desc = "Shows this help message."
        rows.append((help_params_repr, help_desc + long_help_desc))

    return wrap_lines(rows)


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
            row[1] = subcommand.description
        if not common_subcommand_help and subcommand.help_params:
            subcommand_str = ' '.join([c.cli_command for c in parents + [command, subcommand]])
            more_help_str = "For more help type: {} {}.".format(subcommand_str, subcommand.help_params[0])
            if not row[1]:
                row[1] = more_help_str
            else:
                rows.append(['', more_help_str])
    return wrap_lines(rows)


def usage_lines_repr_filter(usages, command_str):
    rows = []
    if len(usages) == 1:
        rows.append((command_str, usages[0].string_repr))
    else:
        rows.append(('', ''))
        for usage in usages:
            rows.append((command_str, usage.string_repr))
    return wrap_lines(rows, row_format='  {0} {1}')


def wrap_lines(rows, col_width=80, row_format='  {0}  {1}'):
    first_col_width = reduce(max, [len(row[0]) for row in rows])
    second_col_width = max(col_width - first_col_width, 10)

    _row_format = row_format.format('{{:{col_width}}}'.format(col_width=first_col_width), '{}')

    _rows = []
    for row in rows:
        wrapped_lines = textwrap.wrap(row[1], second_col_width)
        if not wrapped_lines:
            wrapped_lines = ['']
        _rows.append((row[0], wrapped_lines[0]))
        for line in wrapped_lines[1:]:
            _rows.append(('', line))

    return '\n'.join([_row_format.format(*row) for row in _rows])


_usage_help_jinja_env = Environment(loader=FileSystemLoader(_cli_templates_path))
_usage_help_jinja_env.filters['parameters_usage_help'] = generate_parameters_usage_help
_usage_help_jinja_env.filters['subcommands_usage_help'] = generate_subcommands_usage_help
_usage_help_jinja_env.filters['usage_lines_repr'] = usage_lines_repr_filter
_usage_help_template = _usage_help_jinja_env.get_template('usage_help.template')


_builtin_help_visitor = {'Command': add_builtin_help}


# -------------------------------

def validate_command(command):
    # validate the position of parameters with multiplicity = '*'
    for usage in command.usages:
        rightmost = rightmost_positional_elements(usage)
        for element in usage.sub_elements:
            if element_type(element) == "Parameter" and not element.nonpositional and element.multiplicity == '*' and element not in rightmost:
                raise TextXSemanticError("A positional parameter with multiplicity '*' must be the rightmost one: '{}'.".format(element.name))


def rightmost_positional_elements(element):
    if hasattr(element, 'elements'):
        if element_type(element) == 'CliOrGroup':
            ret = []
            for or_el in element.elements:
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


_validation_visitor = {'Command': validate_command}


# -------------------------------

model_visitors = [
    _parameter_processor_visitor,
    _usage_repr_visitor,
    _builtin_help_visitor,
    _validation_visitor,
]
