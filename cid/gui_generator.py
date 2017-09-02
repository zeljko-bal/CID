from os.path import join, split, dirname, realpath, isdir
from shutil import copy, rmtree, copytree
from collections import defaultdict, namedtuple
from jinja2 import Environment, FileSystemLoader

from cid_parser import parse
from utils.model_processor import ModelProcessor
from utils.common import *


_gui_templates_path = join(dirname(realpath(__file__)), 'templates', 'gui')
_gui_framework_path = join(dirname(realpath(__file__)), 'framework', 'gui')


class GuiStructure:
    def __init__(self, parent, elements):
        self.parent = parent
        self.elements = elements


class GuiSectionGroup:
    def __init__(self, parent, elements, exclusive):
        self.parent = parent
        self.elements = elements
        self.exclusive = exclusive


class GuiSection:
    def __init__(self, parent, title, body, expanded, optional):
        self.parent = parent
        self.title = title
        self.body = body
        self.expanded = expanded
        self.optional = optional


class GuiGrid:
    def __init__(self, parent, elements):
        self.parent = parent
        self.elements = elements


GuiRowDimensions = namedtuple('GuiRowDimensions', ['colspan', 'width'])


def html_id(id):
    return id.replace('/', '_')


# ------------------------------- GUI MODEL PROCESSORS -------------------------------

_supported_widgets_by_type = {
    'Str': ['text_field', 'password'],
}

def convert_row_to_grid(row):
    if not element_type(row.parent) == 'GuiGrid':
        idx = row.parent.elements.index(row)
        grid = GuiGrid(row.parent, [row])
        row.parent.elements[idx] = grid
        row.parent = grid


def check_parameter_widget(parameter):
    if parameter.widget:
        supported_widgets = _supported_widgets_by_type[parameter.type]
        if parameter.widget not in supported_widgets:
            raise Exception('parameter.widget unsupported')


# -------------------------------

def usage_group_gui_structure(usage_group):  # TODO refactor
    usage_group.gui_structure = GuiStructure(parent=None, elements=[])

    for element in usage_group.elements:
        if element_type(element) == 'Parameter':
            usage_group.gui_structure.elements.append(element)
        elif element_type(element) in ['CliOptionalGroup', 'CliOrGroup']:
            usage_group.gui_structure.elements.append(element.gui_structure)
            element.gui_structure.parent = usage_group.gui_structure


def usage_or_group_gui_structure(or_group):
    or_group.gui_structure = GuiSectionGroup(parent=None, elements=[], exclusive=True)

    for idx, or_element in enumerate(or_group.elements):
        section = GuiSection(parent=or_group.gui_structure, title='Variant: {}'.format(idx + 1), body=None, expanded=idx == 0, optional=False)
        if element_type(or_element) == 'Parameter':
            section.body = GuiStructure(parent=section, elements=[or_element])
        else:
            section.body = or_element.gui_structure
            section.body.parent = section
        or_group.gui_structure.elements.append(section)


def usage_optional_group_gui_structure(optional_group):
    if len(optional_group.elements) == 1:
        element = optional_group.elements[0]
        if element_type(element) == 'Parameter':
            optional_group.gui_structure = element
        elif element_type(element) in ['CliOptionalGroup', 'CliOrGroup']:
            optional_group.gui_structure = element.gui_structure
            element.gui_structure.parent = optional_group.gui_structure
    else:
        optional_group.gui_structure = GuiSection(parent=None, title='Optional', body=None, expanded=False, optional=True)
        optional_group.gui_structure.body = GuiStructure(parent=optional_group.gui_structure, elements=[])

        for element in optional_group.elements:
            if element_type(element) == 'Parameter':
                optional_group.gui_structure.body.elements.append(element)
            else:
                optional_group.gui_structure.body.elements.append(element.gui_structure)
                element.gui_structure.parent = optional_group.gui_structure.body


_add_default_gui_structure_visitor = {'CliStructure': usage_group_gui_structure, 'CliGroup': usage_group_gui_structure, 'CliOrGroup': usage_or_group_gui_structure, 'CliOptionalGroup': usage_optional_group_gui_structure}


def gui_structure_defaults(command):
    if not command.gui:
        for usage in command.usages:
            ModelProcessor(_add_default_gui_structure_visitor).process_cli_group(usage)

        if len(command.usages) == 1:
            command.gui = usage.gui_structure
            command.gui.parent = command
        else:
            section_group = GuiSectionGroup(parent=command, elements=[], exclusive=True)

            for idx, usage in enumerate(command.usages):
                section = GuiSection(parent=section_group, title='Variant: {}'.format(idx + 1), body=None, expanded=idx == 0, optional=False)
                section.body = usage.gui_structure
                section.body.parent = section
                section_group.elements.append(section)

            command.gui = GuiStructure(parent=command, elements=[section_group])


# -------------------------------

def add_gui_grid_row_dimensions(grid_row):
    grid_row.dimensions = []
    for idx, cell in enumerate(grid_row.elements):
        if element_type(cell) in ['Parameter', 'EmptyCell']:
            colspan = 1
            while idx + colspan < len(grid_row.elements) and element_type(grid_row.elements[idx + colspan]) == 'CellSpan':
                colspan += 1
            width = round((100 / len(grid_row.elements)) * colspan)
            grid_row.dimensions.append(GuiRowDimensions(colspan, width))
        else:
            grid_row.dimensions.append(None)


# -------------------------------

def parameter_description_defaults(parameter):
    # nothing to put in gui default description since gui is mostly self describing
    parameter.description = parameter.description.format(default_desc='')


def gui_widget_defaults(parameter):
    parameter_type = element_type(parameter)
    if parameter_type in _supported_widgets_by_type:
        supported_widgets = _supported_widgets_by_type[parameter_type]
        parameter.widget = supported_widgets[0]  # take first


# -------------------------------

def gui_section_group_defaults(section_group):
    if all([not section.expanded for section in section_group.elements]):
        section_group.elements[0].expanded = True


# -------------------------------

def convert_id(element):
    element.id = html_id(element.id)


_convert_id_visitor = {'Command': convert_id, 'Parameter': convert_id}


# -------------------------------

def check_gui_grid(grid):
    row_length = None
    for row in grid.elements:
        if row_length and row_length != len(row.elements):
            raise Exception("Inconsistent row length in gui grid for command: {}".format('TODO'))
        else:
            row_length = len(row.elements)


# -------------------------------

def check_gui_section_group(section_group):
    # check for two expanded sections
    found_expanded = False
    for section in section_group.elements:
        if section.expanded:
            if found_expanded:
                raise Exception("Two expanded sections in gui section group for command: {}".format('TODO'))
            elif section.expanded:
                found_expanded = True

    # check for optional sections
    if any([section.optional for section in section_group.elements]):
        raise Exception("Optional section in section group.")


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
    

# ------------------------------- GENERATOR FUNCTIONS -------------------------------

def process_model(model):
    ModelProcessor({'GuiGridRow': convert_row_to_grid});
    ModelProcessor([{'GuiSectionGroup': gui_section_group_defaults, 'Command': gui_structure_defaults, 'GuiGridRow': add_gui_grid_row_dimensions,
                     'Parameter': [parameter_description_defaults, gui_widget_defaults]}, _convert_id_visitor]).process_model(model)
    ModelProcessor({'Parameter': check_parameter_widget, 'GuiGrid': check_gui_grid, 'GuiSectionGroup': check_gui_section_group}).process_model(model)


def render_gui_code(model, root_command_name, dest_path):
    # EXTRACT DATA ---------------------
    model_extractor = ElementExtractor()
    ModelProcessor(model_extractor.visitor).process_model(model)

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

def generate_gui(cid_file, root_command_name, dest_path):
    model = parse(cid_file)
    process_model(model)
    copy_framework(dest_path, root_command_name)
    render_gui_code(model, root_command_name, dest_path)
    render_runner_script(dest_path, root_command_name)


# ------------------------------- MAIN -------------------------------

if __name__ == '__main__':
    generate_gui('D:/docs/FAX/master/projekat/cid/example1.cid', 'command1', 'D:/docs/FAX/master/projekat/dist')  # TODO src path as arg, # TODO root_command_name and dest path as args
