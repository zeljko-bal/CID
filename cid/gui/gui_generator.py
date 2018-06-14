from collections import defaultdict
from os.path import join, dirname, realpath, isdir
from shutil import rmtree, copytree

from jinja2 import Environment, FileSystemLoader

from cid.gui import gui_post_processing
from cid.gui.gui_model_specs import GuiModelSpecs
from cid.gui.utils import html_id
from cid.parser.cid_parser import parse
from cid.common.cid_model_processor import CidModelProcessor
from cid.common.utils import *


_gui_templates_path = join(dirname(realpath(__file__)), 'templates')
_gui_framework_path = join(dirname(realpath(__file__)), 'framework')


# ------------------------------- JINJA FILTERS -------------------------------

class UniqueIdGenerator:
    def __init__(self):
        self.id_counts = defaultdict(int)

    def make_new(self, id, id_format='{id}_{count}'):
        self.id_counts[id] += 1
        return self.get_current(id, id_format)

    def get_current(self, id, id_format='{id}_{count}'):
        return id_format.format(id=id, count=self.id_counts[id])


def get_gui_id(element, parent, base_id):
    idx = parent.elements.index(element)
    id = '{idx}_{base}'.format(idx=idx, base=base_id)
    current = parent

    while element_type(current.parent) != 'Command':
        if hasattr(current.parent, 'elements'):
            idx = current.parent.elements.index(current)
            id = '{idx}_{prev}'.format(idx=idx, prev=id)
        current = current.parent
    return '{cmd_id}_{prev}'.format(cmd_id=html_id(current.parent.id), prev=id)


def js_bool_filter(val):
    if val:
        return 'true'
    else:
        return 'false'


def get_first_positive_cli_pattern(bool_param):
    for pattern in bool_param.all_patterns:
        if pattern.positive:
            return pattern.positive
    else:
        return ''


def get_first_negative_cli_pattern(bool_param):
    for pattern in bool_param.all_patterns:
        if pattern.negative:
            return pattern.negative
    else:
        return ''


def get_first_cli_pattern(param):
    return param.all_patterns[0]
    

def has_directory_constraint_filter(param):
    return 'is_directory' in [constraint.type for constraint in param.constraints if element_type(constraint) == 'FileFlagConstraint']


# ------------------------------- GENERATOR FUNCTIONS -------------------------------

def process_model(model):
    for visitor in gui_post_processing.model_visitors:
        CidModelProcessor(visitor).process_model(model)

    CidModelProcessor(GuiModelSpecs().visitor).process_model(model)


def render_gui_code(model, root_command_name, dest_path):
    # EXTRACT DATA ---------------------
    model_extractor = ElementExtractor()
    CidModelProcessor(model_extractor.visitor).process_model(model)

    all_commands = model_extractor.all_commands
    all_parameters = model_extractor.all_parameters

    # RENDER GUI HTML ---------------------
    unique_id_generator = UniqueIdGenerator()
    env = Environment(loader=FileSystemLoader(_gui_templates_path))

    env.filters['all_parent_commands'] = all_parent_commands
    env.filters['element_type'] = element_type
    env.filters['new_unique_id'] = unique_id_generator.make_new
    env.filters['current_unique_id'] = unique_id_generator.get_current
    env.filters['tab_indent'] = tab_indent_filter
    env.filters['stringify'] = stringify_filter
    env.filters['gui_id'] = get_gui_id
    env.filters['js_bool'] = js_bool_filter
    env.filters['first_positive_cli_pattern'] = get_first_positive_cli_pattern
    env.filters['first_negative_cli_pattern'] = get_first_negative_cli_pattern
    env.filters['first_cli_pattern'] = get_first_cli_pattern
    env.filters['has_directory_constraint'] = has_directory_constraint_filter

    index_template = env.get_template('index.html.template')

    index_rendered = index_template.render(root_command_name=root_command_name, root_command_id=html_id(element_id(root_command_name)), commands=all_commands, parameters=all_parameters)
    
    with open(join(dest_path, root_command_name + '_gui', "index.html"), "w") as text_file:
        text_file.write(index_rendered)
    
    # RENDER ELECTRON PACKAGE ---------------------
    package_template = env.get_template('electron_package.json.template')

    package_rendered = package_template.render(command_name=root_command_name)
    
    with open(join(dest_path, root_command_name + '_gui', "package.json"), "w") as text_file:
        text_file.write(package_rendered)


def copy_framework(dest_path, root_command_name):
    gui_app_path = join(dest_path, root_command_name + '_gui')
    gui_temp_dir = join(dest_path, root_command_name + '_gui_temp')
    custom_dir_path = join(gui_app_path, 'custom')
    
    if isdir(gui_app_path):
        if isdir(custom_dir_path):
            if isdir(gui_temp_dir):
                rmtree(gui_temp_dir)
             
            copytree(custom_dir_path, gui_temp_dir)
            
        rmtree(gui_app_path)
    
    copytree(join(_gui_framework_path, 'app'), gui_app_path)
    
    if isdir(gui_temp_dir):
        rmtree(custom_dir_path)
        copytree(gui_temp_dir, custom_dir_path)
        rmtree(gui_temp_dir)


def render_runner_script(dest_path, root_command_name):
    env = Environment(loader=FileSystemLoader(_gui_templates_path))
    template = env.get_template('windows_gui_runner.template')
    rendered = template.render(gui_app_path=root_command_name + '_gui')
    
    with open(join(dest_path, root_command_name + "_gui.bat"), "w") as text_file:
        text_file.write(rendered)

        
def is_root_command_defined(model, root_command_name):
    model_extractor = ElementExtractor()
    CidModelProcessor(model_extractor.visitor).process_model(model)

    return root_command_name in [command.name for command in model_extractor.all_commands]
    

def generate_gui(cid_file, root_command_name, dest_path):
    model = parse(cid_file)
    if not is_root_command_defined(model, root_command_name):
        print("Error: The specified root command is not defined.")
        return

    process_model(model)

    copy_framework(dest_path, root_command_name)

    render_gui_code(model, root_command_name, dest_path)
    render_runner_script(dest_path, root_command_name)

    print("Generated gui successfully.")
