from collections import defaultdict
from os import makedirs
from os.path import realpath, join, dirname, isdir, exists
from shutil import copy

from jinja2 import Environment, FileSystemLoader

from cid.cli.cli_model_specs import CliModelSpecs
from cid.cli import cli_post_processing
from cid.parser.cid_parser import parse
from cid.common.cid_model_processor import CidModelProcessor
from cid.common.utils import *


_cli_templates_path = join(dirname(realpath(__file__)), 'templates')
_cli_framework_path = join(dirname(realpath(__file__)), 'framework')


# ------------------------------- JINJA FILTERS -------------------------------

def parameter_model_filter(parameter):
    def print_list(lst):
        return str(lst) if len(lst) > 1 else "'{}'".format(lst[0])

    if parameter.type == 'Bool':
        positives = [p.positive for p in parameter.all_patterns if p.positive]
        negatives = [p.negative for p in parameter.all_patterns if p.negative]

        positives_str = ", positives={prefixes}".format(prefixes=print_list(positives)) if positives else ''
        negatives_str = ", negatives={prefixes}".format(prefixes=print_list(negatives)) if negatives else ''

        return "BooleanNonpositional('{name}'{positives}{negatives})".format(
            name=parameter.name, positives=positives_str, negatives=negatives_str)
    else:
        ret = []
        classified = defaultdict(lambda: defaultdict(set))
        for pattern in parameter.all_patterns:
            if pattern.white_space:
                if pattern.count:
                    count_str = ", count={count}".format(count=pattern.count)
                elif pattern.count_many:
                    count_str = ", count='*'"
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
                    classified['CounterNonpositional'][pattern.count_char].add(pattern)
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
                ret.append("CounterNonpositional('{name}', {prefixes}, '{count_char}')".format(name=parameter.name, prefixes=print_list(prefixes), count_char=count_char))
        if classified['BasicNonpositional']:
            for _, patterns in classified['BasicNonpositional'].items():
                prefixes = [p.prefix for p in patterns]
                ret.append("BasicNonpositional('{name}', {prefixes})".format(name=parameter.name, prefixes=print_list(prefixes)))
        return ', '.join(ret)


def have_sub_commands_filter(commands):
    return any([c.sub_commands for c in commands])


# ------------------------------- GENERATOR FUNCTIONS -------------------------------

def process_model(model):
    for visitor in cli_post_processing.model_visitors:
        CidModelProcessor(visitor).process_model(model)

    CidModelProcessor(CliModelSpecs().visitor).process_model(model)


def render_cli_code(model, root_command_name, cli_app_path):
    # EXTRACT DATA ---------------------
    model_extractor = ElementExtractor()
    CidModelProcessor(model_extractor.visitor).process_model(model)

    all_commands = model_extractor.all_commands
    all_parameters = model_extractor.all_parameters

    # RENDER CLI PARSER ---------------------
    env = Environment(loader=FileSystemLoader(_cli_templates_path))

    env.filters['parameter_model'] = parameter_model_filter
    env.filters['element_type'] = element_type
    env.filters['tab_indent'] = tab_indent_filter
    env.filters['stringify'] = stringify_filter
    env.filters['have_sub_commands'] = have_sub_commands_filter

    env.globals['raise'] = raise_exception_helper

    parser_template = env.get_template('cli_parser.template')
    
    parser_rendered = parser_template.render(root_command_name=root_command_name, root_command_id=element_id(root_command_name),
                               commands=all_commands, parameters=all_parameters)

    with open(join(cli_app_path, root_command_name + "_cli_parser.py"), "w") as text_file:
        text_file.write(parser_rendered)
    
    # RENDER CLI COMMAND ---------------------
    command_file_path = join(cli_app_path, root_command_name + '_cli.py')
    
    if not exists(command_file_path):
        command_template = env.get_template('cli_command.template')
        
        command_rendered = command_template.render(root_command_name=root_command_name)
        
        with open(command_file_path, "w") as text_file:
            text_file.write(command_rendered)
    

def copy_framework(cli_app_path):
    if not isdir(cli_app_path):
        makedirs(cli_app_path)
    
    copy(join(_cli_framework_path, "generic_cli_parser.py"), cli_app_path)
    copy(join(_cli_framework_path, "js_date.py"), cli_app_path)
    

def render_runner_script(root_command_name, dest_path):
    env = Environment(loader=FileSystemLoader(_cli_templates_path))
    template = env.get_template('windows_cli_py_runner.template')
    rendered = template.render(command_path=join(root_command_name + '_cli', root_command_name + "_cli.py"))

    with open(join(dest_path, root_command_name + ".bat"), "w") as text_file:
        text_file.write(rendered)
        
        
def is_root_command_defined(model, root_command_name):
    model_extractor = ElementExtractor()
    CidModelProcessor(model_extractor.visitor).process_model(model)

    return root_command_name in [command.name for command in model_extractor.all_commands]
        
        
def generate_cli(cid_file, root_command_name, dest_path):
    cli_app_path = join(dest_path, root_command_name + "_cli")

    model = parse(cid_file)

    if not is_root_command_defined(model, root_command_name):
        print("Error: The specified root command is not defined.")
        return

    process_model(model)

    copy_framework(cli_app_path)

    render_cli_code(model, root_command_name, cli_app_path)
    render_runner_script(root_command_name, dest_path)

    print("Generated cli successfully.")
