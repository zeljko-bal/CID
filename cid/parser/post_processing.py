from textx.exceptions import TextXSemanticError

from cid.parser.model import CliStructure, CliOptionalGroup
from cid.common.utils import parent_command, element_id, element_type, all_parent_commands


# ------------------------------- POST PROCESSING -------------------------------


def process_cli_separator(cli_separator):
    # usage_repr
    cli_separator.usage_repr = cli_separator.value

    # fill cmd.cli_separators
    command = parent_command(cli_separator)
    if not hasattr(command, 'cli_separators'):
        command.cli_separators = []
    command.cli_separators.append(cli_separator.value)


_cli_separator_visitor = {'CliSeparator': process_cli_separator}


# -------------------------------

def add_id(element):
    element.id = element_id(element.name, [e.name for e in all_parent_commands(element)])


_add_id_visitor = {'Command': add_id, 'Parameter': add_id}


# -------------------------------

def set_usage_defaults(command):
    if not command.usages:
        default_usage = CliStructure(
            command,
            sorted([parameter for parameter in command.parameters if not parameter.nonpositional],
                   key=lambda parameter: 0 if parameter.multiplicity != '*' else 1),
            has_options=True,
            has_subcommand=False)
        command.usages = [default_usage]

    if command.sub_commands and all([not usage.has_subcommand for usage in command.usages]):
        for usage in command.usages:
            usage.has_subcommand = True


_usage_defaults_visitor = {'Command': set_usage_defaults}


# -------------------------------

def numeric_value_constraint_message_defaults(constraint):
    if not constraint.message:
        if constraint.type == 'max':
            constraint.message = "Maximum value is {0}.".format(constraint.value)
        elif constraint.type == 'min':
            constraint.message = "Minimum value is {0}.".format(constraint.value)


def date_constraint_message_defaults(constraint):
    if not constraint.message:
        if constraint.type == 'max':
            constraint.message = "Maximum value is {0}.".format(constraint.value)
        elif constraint.type == 'min':
            constraint.message = "Minimum value is {0}.".format(constraint.value)


def length_constraint_message_defaults(constraint):
    if not constraint.message:
        if constraint.type == 'max_length':
            constraint.message = "Maximum length is {0}.".format(constraint.value)
        elif constraint.type == 'min_length':
            constraint.message = "Minimum length is {0}.".format(constraint.value)


def string_flag_constraint_message_defaults(constraint):
    if not constraint.message:
        if constraint.type == 'alphanumeric':
            constraint.message = "The value must be alphanumeric."


def number_flag_constraint_message_defaults(constraint):
    if not constraint.message:
        if constraint.type == 'integer':
            constraint.message = "The value must be an integer."


def file_flag_constraint_message_defaults(constraint):
    if not constraint.message:
        if constraint.type == 'exists':
            constraint.message = "The provided file doesn't exist."
        elif constraint.type == 'doesnt_exist':
            constraint.message = "The provided file already exists."
        elif constraint.type == 'is_file':
            constraint.message = "The provided path is not a file."
        elif constraint.type == 'is_directory':
            constraint.message = "The provided path is not a directory."


def regex_constraint_message_defaults(constraint):
    if not constraint.message:
        constraint.message = "The value must satisfy the following regular expression: /{0}/.".format(constraint.value)


_constraint_message_defaults_visitor = {
    'NumericValueConstraint': numeric_value_constraint_message_defaults,
    'DateConstraint': date_constraint_message_defaults,
    'LengthConstraint': length_constraint_message_defaults,
    'StringFlagConstraint': string_flag_constraint_message_defaults,
    'NumberFlagConstraint': number_flag_constraint_message_defaults,
    'FileFlagConstraint': file_flag_constraint_message_defaults,
    'RegexConstraint': regex_constraint_message_defaults
}


# -------------------------------

def gather_usage_sub_elements(cli_element, parents):
    if not hasattr(cli_element, 'sub_elements'):
        cli_element.sub_elements = set()

    for group_element in cli_element.elements:
        if hasattr(group_element, 'sub_elements'):
            if not cli_element.sub_elements.isdisjoint(group_element.sub_elements) and not element_type(cli_element) == 'CliOrGroup':
                raise TextXSemanticError('Found duplicate elements in usage.')
            cli_element.sub_elements.update(group_element.sub_elements)
        elif element_type(group_element) == 'Parameter':
            if group_element in cli_element.sub_elements and not element_type(cli_element) == 'CliOrGroup':
                raise TextXSemanticError("Found duplicate element '{}' in usage for command: '{}'.".format(group_element.name, [p.name for p in parents if element_type(p) == 'Command']))
            cli_element.sub_elements.add(group_element)
        elif element_type(group_element) == 'CliSeparator':
            if hasattr(cli_element, 'has_cli_separator'):
                raise TextXSemanticError('Found duplicate argument separator.')
            cli_element.has_cli_separator = True


_gather_usage_sub_elements_visitor = {
    'CliStructure': gather_usage_sub_elements,
    'CliGroup': gather_usage_sub_elements,
    'CliOptionalGroup': gather_usage_sub_elements,
    'CliOrGroup': gather_usage_sub_elements
}


# -------------------------------

def gather_gui_group_sub_elements(gui_group):
    gui_group.sub_elements = set()

    for element in gui_group.elements:
        if hasattr(element, 'sub_elements'):
            if element_type(gui_group) != 'GuiSectionGroup' or not gui_group.exclusive:
                if not gui_group.sub_elements.isdisjoint(element.sub_elements):
                    raise TextXSemanticError("Found duplicate elements in gui structure.")
            gui_group.sub_elements.update(element.sub_elements)
        elif element_type(element) == 'Parameter':
            if element in gui_group.sub_elements:
                raise TextXSemanticError("Found duplicate elements in gui structure.")
            gui_group.sub_elements.add(element)


def gather_gui_element_sub_elements(gui_element):
    gui_element.sub_elements = gui_element.body.sub_elements


_gather_gui_sub_elements_visitor = {
    'GuiStructure': gather_gui_group_sub_elements,
    'GuiTabs': gather_gui_group_sub_elements,
    'GuiSectionGroup': gather_gui_group_sub_elements,
    'GuiSection': gather_gui_element_sub_elements,
    'GuiGrid': gather_gui_group_sub_elements,
    'GuiTab': gather_gui_element_sub_elements,
    'GuiGridRow': gather_gui_group_sub_elements,
}


# -------------------------------

def expand_options_shortcut(command):
    for usage in command.usages:
        if usage.has_options:
            options = [parameter for parameter in command.parameters if parameter.nonpositional and parameter not in usage.sub_elements]
            usage.elements = [CliOptionalGroup(usage, [parameter], [parameter]) for parameter in options] + usage.elements
            usage.sub_elements = set(options).union(usage.sub_elements)


_expand_options_shortcut_visitor = {'Command': expand_options_shortcut}


# -------------------------------

def validate_command(command, parents):
    script = parents[0]
    for parameter in command.parameters:
        if parameter.name in [p.name for p in script.free_parameters] and not parameter in script.free_parameters:
            raise TextXSemanticError('Parameter name collision between {cmd}.{param} and a top level free parameter.'.format(
                cmd=command.name, param=parameter.name))

    for sub_command in command.sub_commands:
        if sub_command.name in [c.name for c in script.free_commands] and not sub_command in script.free_commands:
            raise TextXSemanticError('Command name collision between {cmd}.{sub} and a top level free command.'.format(cmd=command.name, sub=sub_command.name))

    parameter_declaration_check(command)


def parameter_declaration_check(command):
    if command.gui:
        declared_names = [p.name for p in command.parameters]
        for element in command.gui.sub_elements:
            if element.name not in declared_names:
                raise TextXSemanticError('Undeclared parameter: {param} in command gui struture: {cmd}.'.format(param=element.name, cmd=command.name))

    usage_sub_elements = set()
    for usage in command.usages:
        usage_sub_elements.update(usage.sub_elements)

    declared_names = [p.name for p in command.parameters]
    for element in usage_sub_elements:
        if element.name not in declared_names:
            raise TextXSemanticError('Undeclared parameter: {param} in command: {cmd}.'.format(param=element.name, cmd=command.name))

    all_sub_elements = usage_sub_elements
    if command.gui:
        all_sub_elements.update(command.gui.sub_elements)

    for parameter in command.parameters:
        if parameter not in all_sub_elements:
            print("Warning: parameter {} declared, but not referenced in command: {}.".format(parameter.name, command.id))


_validation_visitor = {'Command': validate_command}


# -------------------------------

model_visitors = [
    _cli_separator_visitor,
    _add_id_visitor,
    _usage_defaults_visitor,
    _constraint_message_defaults_visitor,
    _gather_usage_sub_elements_visitor,
    _gather_gui_sub_elements_visitor,
    _expand_options_shortcut_visitor,
    _validation_visitor,
]
