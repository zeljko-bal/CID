from os.path import realpath, join, dirname

from textx.exceptions import TextXSemanticError
from textx.metamodel import metamodel_from_file

from cid.cid_model_specs import CidModelSpecs
from cid.utils.cid_model_processor import CidModelProcessor
from cid.utils.reference_resolver import ReferenceResolver, ImportedReferenceDefinition
from cid.utils.common import *


class CliOptionalGroup:
    def __init__(self, parent, elements, sub_elements):
        self.parent = parent
        self.elements = elements
        self.sub_elements = sub_elements


class CliStructure:
    def __init__(self, parent, elements, has_options, has_subcommand):
        self.parent = parent
        self.elements = elements
        self.has_options = has_options
        self.has_subcommand = has_subcommand
        self.sub_elements = set()
        
 
class ParameterCliValue:
    def __init__(self, cli_pattern):
        self.cli_pattern = cli_pattern
        

class BoolWithPositivePattern:
    def __init__(self, positive, negative=None):
        self.positive = positive
        self.negative = negative


# ------------------------------- HELPER FUNCTIONS -------------------------------

def contains_duplicate_names(lst):
    defined = [e.name for e in lst if not hasattr(e, 'imported') and not hasattr(e, 'local')]
    local = [e.local for e in lst if hasattr(e, 'local') and e.local]
    imported = [e.imported for e in lst if hasattr(e, 'imported') and e.imported]

    return len(defined) != len(set(defined)) or len(local) != len(set(local)) or len(imported) != len(set(imported))


def split_import_path(import_path):
    return './' + ('/'.join(import_path.elements[:-1])) + '.cid', import_path.elements[-1]


def import_reference_path(ref):
    return '/' + '/'.join(ref.elements)


# ------------------------------- FIRST PASS -------------------------------

def process_script(script):
    # check for duplicate free parameter names
    script.free_parameters = [parameter for parameter in script.elements if element_type(parameter) == 'Parameter']
    if contains_duplicate_names(script.free_parameters):
        raise TextXSemanticError("Found duplicate free parameter names.")

    # check for duplicate free command names
    script.free_commands = [command for command in script.elements if element_type(command) == 'Command']
    if contains_duplicate_names(script.free_commands):
        raise TextXSemanticError("Found duplicate free command names.")

    # check for duplicate import paths
    if len(script.imports) != len(set([imp.path for imp in script.imports])):
        raise TextXSemanticError("Found duplicate import paths.")

    # check for duplicate import aliases
    if len(script.imports) != len(set([imp.alias for imp in script.imports])):
        raise TextXSemanticError("Found duplicate import aliases.")


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

def process_command(command):
    """
    Model structure changes:
        del command.usage
    """

    # command.usages = all usages
    if command.usages:
        command.usages = [usage.body for usage in command.usages]
    elif command.usage:
        command.usages = [command.usage]
    del command.usage

    command.description = ' '.join(command.description.split())  # reduce excess white space
    command.help = ' '.join(command.help.split())  # reduce excess white space
    
    # defaults --------------

    if not command.title:
        command.title = command.name.replace('_', ' ').replace('-', ' ').strip().title()

    if not command.cli_command:
        command.cli_command = command.name

    # additional checks --------------

    if contains_duplicate_names(command.parameters):
        raise TextXSemanticError("Found parameters with duplicate names in command: '{}'".format(command.name))

    if contains_duplicate_names(command.sub_commands):
        raise TextXSemanticError("Found sub commands with duplicate names in command: '{}'".format(command.name))


# -------------------------------

def process_parameter(parameter):
    """
    Model structure changes:
        add parameter.nonpositional
        fix parameter.default
        add parameter.all_patterns
        add parameter.cli_pattern_vars
        add parameter.cli_pattern_count
        del parameter.empty_str_disallowed
        add parameter.none_allowed
        del parameter.default_is_none
    Checks performed: TODO
    Model changes: TODO
    """

    # set default bool cli pattern
    if parameter.type == 'Bool' and not parameter.cli:
        parameter.cli = ParameterCliValue(BoolWithPositivePattern('--{name}'.format(name=parameter.name)))
        
    # set parameter.nonpositional
    parameter.nonpositional = parameter.cli and parameter.cli.cli_pattern

    # fix parameter.default model structure
    if len(parameter.default) == 0:
        parameter.default = None
    elif len(parameter.default) == 1:
        parameter.default = parameter.default[0]

    if parameter.nonpositional:
        # set parameter.all_patterns
        parameter.cli.cli_pattern.parent = parameter
        parameter.all_patterns = [parameter.cli.cli_pattern] + parameter.cli_aliases

        # set parameter.cli_pattern_count
        parameter.cli_pattern_count = get_cli_pattern_count(parameter.all_patterns[0])
        
        # all_patterns
        for pattern in parameter.all_patterns:

            if hasattr(pattern, 'vars') and pattern.vars:
                # transform vars into a list of strings
                pattern.vars = [v.value for v in pattern.vars]

                # set pattern.count
                pattern.count = len(pattern.vars)

                # set parameter.cli_pattern_vars
                if not hasattr(parameter, 'cli_pattern_vars'):
                    parameter.cli_pattern_vars = pattern.vars
                else:
                    if not (len(parameter.cli_pattern_vars) == len(pattern.vars) and
                                all([parameter.cli_pattern_vars[i] == pattern.vars[i] for i in range(0, len(pattern.vars))])):
                        raise TextXSemanticError("Different argument names found for patterns in parameter: '{}'".format(parameter.name))

            # StringParamPattern checks
            if element_type(pattern) == "StringParamPattern":
                if parameter.type == "Bool":
                    raise TextXSemanticError("Non boolean cli pattern in Bool type parameter: '{}'.".format(parameter.name))
                if pattern.count_char and not parameter.type == "Num":
                    raise TextXSemanticError("Counter pattern in non Num type parameter: '{}'.".format(parameter.name))
                if parameter.cli_pattern_count != get_cli_pattern_count(pattern):
                    raise TextXSemanticError("Different parameter count values encountered in cli patterns for parameter: '{}'".format(parameter.name))
            elif element_type(pattern) in ['BoolWithPositivePattern', 'BoolNegativeOnlyPattern'] and not parameter.type == "Bool":
                raise TextXSemanticError("Boolean cli pattern in non Bool type parameter: '{}'.".format(parameter.name))
    else:
        parameter.cli_pattern_count = 1

        # empty_str_allowed
        if (parameter.empty_str_allowed or parameter.empty_str_disallowed) and parameter.type != 'Str':
            raise TextXSemanticError("Found empty_str_allowed or empty_str_disallowed in non Str parameter: '{}'".format(parameter.name))

        if parameter.default == '' and parameter.empty_str_disallowed:
            raise TextXSemanticError("Found empty_str_disallowed and default value is an empty string for parameter: '{}'.".format(parameter.name))

        del parameter.empty_str_disallowed

    # title
    if not parameter.title:
        parameter.title = parameter.name.replace('_', ' ').replace('-', ' ').strip().title()

    # multiplicity
    if not parameter.multiplicity:
        parameter.multiplicity = 1

    if parameter.multiplicity != '*' and parameter.multiplicity <= 0:
        raise TextXSemanticError("Multiplicity must be greater than zero for: '{}'.".format(parameter.name))

    if not parameter.nonpositional and parameter.multiplicity not in [1, '*']:
        raise TextXSemanticError("Multiplicity for positional parameters must be either 1 or '*': '{}'.".format(parameter.name))

    if not parameter.multiplicity == 1 and parameter.type == "Bool":
        raise TextXSemanticError("Multiplicity for Bool type parameters must be 1: '{}'.".format(parameter.name))

    # help
    parameter.help = ' '.join(parameter.help.split())  # reduce excess white space
        
    # description
    parameter.description = ' '.join(parameter.description.split())  # reduce excess white space
    
    if not parameter.description:
        parameter.description = '{default_desc}'

    # default
    if parameter.default_is_none:
        if parameter.type == 'Bool':
            raise TextXSemanticError("Found default_is_none and parameter type is 'Bool': '{}'".format(parameter.name))
        if parameter.default:
            raise TextXSemanticError("Found default_is_none and parameter has a default defined: '{}'.".format(parameter.name))

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

    del parameter.default_is_none

    if parameter.default:
        if parameter.cli_pattern_count not in [1, '*']:
            if not is_iterable(parameter.default) or len(parameter.default) != parameter.cli_pattern_count:
                raise TextXSemanticError("Parameter '{}' with {} values must have that many default values defined.".format(parameter.name, parameter.cli_pattern_count))
        else:
            if is_iterable(parameter.default):
                raise TextXSemanticError("Parameter '{}' should only have a single default value.".format(parameter.name))
    
    if parameter.default == '':
        parameter.empty_str_allowed = True

    if parameter.nonpositional and parameter.default is not None:
        if parameter.cli_pattern_count not in [1, '*']:
            if not isinstance(parameter.default, list):
                parameter.default = [parameter.default] * parameter.cli_pattern_count
            elif len(parameter.default) != parameter.cli_pattern_count:
                raise TextXSemanticError("Parameter pattern count and default values count do not match: '{}'.".format(parameter.name))

    if parameter.type == 'Bool':
        if parameter.default and parameter.default.lower() not in ['true', 'false']:
            raise TextXSemanticError("Default value is not true or false and parameter type is 'Bool': '{}'".format(parameter.name))

        # add parameter.none_allowed
        parameter.none_allowed = parameter.default is None or [p for p in parameter.all_patterns if p.positive] and [p for p in parameter.all_patterns if p.negative]

    # date_format
    if not parameter.date_format and parameter.type == 'Date':
        parameter.date_format = "dd.MM.yyyy"

    # choices
    if parameter.choices and not parameter.type == 'Choice':
        raise TextXSemanticError("Choices found in non 'Choice' parameter: '{}'.".format(parameter.name))

    if parameter.type == 'Choice' and not parameter.choices:
        raise TextXSemanticError("Choices are required in 'Choice' parameter: '{}'".format(parameter.name))

    # constraints
    for constraint in parameter.constraints:
        supported_constraints = {
            'Str': ['LengthConstraint', 'StringFlagConstraint', 'RegexConstraint', 'CodeConstraint'],
            'Choice': ['CodeConstraint'],
            'Num': ['NumericValueConstraint', 'NumberFlagConstraint', 'CodeConstraint'],
            'Bool': ['CodeConstraint'],
            'Date': ['DateConstraint', 'CodeConstraint'],
            'File': ['FileFlagConstraint', 'CodeConstraint', 'RegexConstraint'],
        }[parameter.type]
        if element_type(constraint) not in supported_constraints:
            raise TextXSemanticError("Constraint type '{}' is unsupported for parameter type '{}': '{}'.".format(element_type(constraint), parameter.type, parameter.name))


# -------------------------------

def process_cli_or_group(or_group):
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
            print('warning: CliOptionalGroup in CliOrGroup')


# ------------------------------- SECOND PASS -------------------------------

def process_cli_separator(cli_separator):
    # usage_repr
    cli_separator.usage_repr = cli_separator.value

    # fill cmd.cli_separators
    command = parent_command(cli_separator)
    if not hasattr(command, 'cli_separators'):
        command.cli_separators = []
    command.cli_separators.append(cli_separator.value)


# -------------------------------

def add_id(element):
    element.id = element_id(element.name, [e.name for e in all_parent_commands(element)])


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


_constraint_message_defaults_visitor = {'NumericValueConstraint': numeric_value_constraint_message_defaults,
                                        'DateConstraint': date_constraint_message_defaults,
                                        'LengthConstraint': length_constraint_message_defaults,
                                        'StringFlagConstraint': string_flag_constraint_message_defaults,
                                        'NumberFlagConstraint': number_flag_constraint_message_defaults,
                                        'FileFlagConstraint': file_flag_constraint_message_defaults,
                                        'RegexConstraint': regex_constraint_message_defaults}


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


_gather_usage_sub_elements_visitor = {'CliStructure': gather_usage_sub_elements, 
                                      'CliGroup': gather_usage_sub_elements,
                                      'CliOptionalGroup': gather_usage_sub_elements,
                                      'CliOrGroup': gather_usage_sub_elements}


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


# ------------------------------- PARSER FUNCTIONS -------------------------------

def parse(script_path):
    grammar_path = join(dirname(realpath(__file__)), 'grammar', 'cid_grammar.tx')
    metamodel = metamodel_from_file(grammar_path, autokwd=True)
    
    # FIRST PASS ---------------------

    metamodel.register_obj_processors({
        'Script': process_script,
        'ImportStatement': process_import_statement,
        'ParameterReference': process_import_reference,
        'CommandReference': process_import_reference,
        'Command': process_command,
        'Parameter': process_parameter,
        'CliOrGroup': process_cli_or_group,
    })

    model = metamodel.model_from_file(script_path)

    # EXTRACT DATA ---------------------

    model_extractor = ElementExtractor()
    CidModelProcessor(model_extractor.visitor).process_model(model)

    all_defined_commands = model_extractor.all_commands
    all_defined_parameters = model_extractor.all_parameters

    # DEREFERENCE ---------------------

    parameter_instances = {instance.name: instance for instance in all_defined_parameters}
    command_instances = {instance.name: instance for instance in all_defined_commands}

    script_directory = dirname(script_path)
    external_models = {file_path: parse(join(script_directory, file_path)) for file_path in set([_import.file_path for _import in model.imports])}
    import_definitions = {_import.alias: ImportedReferenceDefinition(_import.alias, _import.element_name, external_models[_import.file_path], _import.file_path) for _import in model.imports}

    reference_resolver = ReferenceResolver(parameter_instances, command_instances, import_definitions)
    reference_resolver_visitor = {'ParameterReference': reference_resolver.resolve_parameter_reference, 'CommandReference': reference_resolver.resolve_command_reference}

    CidModelProcessor(reference_resolver_visitor).process_model(model)

    # SECOND PASS ---------------------

    CidModelProcessor({'CliSeparator': process_cli_separator}).process_model(model)
    CidModelProcessor({'Command': add_id, 'Parameter': add_id}).process_model(model)
    CidModelProcessor({'Command': set_usage_defaults}).process_model(model)
    CidModelProcessor(_constraint_message_defaults_visitor).process_model(model)
    CidModelProcessor(_gather_usage_sub_elements_visitor).process_model(model)
    CidModelProcessor(_gather_gui_sub_elements_visitor).process_model(model)
    CidModelProcessor({'Command': expand_options_shortcut}).process_model(model)
    CidModelProcessor({'Command': validate_command}).process_model(model)

    CidModelProcessor(CidModelSpecs().visitor).process_model(model)
    
    return model
