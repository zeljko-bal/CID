from textx.exceptions import TextXSemanticError

from cid.parser.model import ParameterCliValue, BoolWithPositivePattern
from cid.common.utils import get_cli_pattern_count, is_iterable, element_type


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


# ------------------------------- PRE PROCESSING -------------------------------

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


# -------------------------------

object_processors = {
    'Script': process_script,
    'ImportStatement': process_import_statement,
    'ParameterReference': process_import_reference,
    'CommandReference': process_import_reference,
    'Command': process_command,
    'Parameter': process_parameter,
    'CliOrGroup': process_cli_or_group,
}
