from collections import namedtuple

from textx.exceptions import TextXSemanticError

from cid.common.cid_model_processor import CidModelProcessor
from cid.common.utils import element_type, parent_command
from cid.gui.model import GuiGrid, GuiStructure, GuiSectionGroup, GuiSection
from cid.gui.utils import html_id


GuiRowDimensions = namedtuple('GuiRowDimensions', ['colspan', 'width'])


# ------------------------------- GUI MODEL PROCESSORS -------------------------------

def convert_row_to_grid(row):
    if not element_type(row.parent) == 'GuiGrid':
        idx = row.parent.elements.index(row)
        grid = GuiGrid(row.parent, [row])
        row.parent.elements[idx] = grid
        row.parent = grid


_row_to_grid_visitor = {'GuiGridRow': convert_row_to_grid}


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


_add_default_gui_structure_visitor = {
    'CliStructure': usage_group_gui_structure,
    'CliGroup': usage_group_gui_structure,
    'CliOrGroup': usage_or_group_gui_structure,
    'CliOptionalGroup': usage_optional_group_gui_structure
}


# -------------------------------

def gui_structure_defaults(command):
    if not command.gui:
        for usage in command.usages:
            CidModelProcessor(_add_default_gui_structure_visitor).process_cli_group(usage)

        if len(command.usages) == 1:
            command.gui = command.usages[0].gui_structure
            command.gui.parent = command
        else:
            section_group = GuiSectionGroup(parent=command, elements=[], exclusive=True)

            for idx, usage in enumerate(command.usages):
                section = GuiSection(parent=section_group, title='Variant: {}'.format(idx + 1), body=None, expanded=idx == 0, optional=False)
                section.body = usage.gui_structure
                section.body.parent = section
                section_group.elements.append(section)

            command.gui = GuiStructure(parent=command, elements=[section_group])


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


def parameter_description_defaults(parameter):
    # nothing to put in gui default description since gui is mostly self describing
    parameter.description = parameter.description.format(default_desc='')


def gui_section_group_defaults(section_group):
    if all([not section.expanded for section in section_group.elements]):
        section_group.elements[0].expanded = True


_defaults_visitor = {
    'GuiSectionGroup': gui_section_group_defaults,
    'Command': gui_structure_defaults,
    'GuiGridRow': add_gui_grid_row_dimensions,
    'Parameter': parameter_description_defaults,
}


# -------------------------------

def convert_id(element):
    element.id = html_id(element.id)


_convert_id_visitor = {'Command': convert_id, 'Parameter': convert_id}


# -------------------------------

def check_gui_grid(grid):
    row_length = None
    for row in grid.elements:
        if row_length and row_length != len(row.elements):
            raise TextXSemanticError("Inconsistent row length in gui grid for command: '{}'".format(parent_command(grid).id))
        else:
            row_length = len(row.elements)


def check_gui_section_group(section_group):
    # check for two expanded sections
    found_expanded = False
    for section in section_group.elements:
        if section.expanded:
            if found_expanded:
                raise TextXSemanticError("Two expanded sections in gui section group for command: '{}'".format(parent_command(section_group).id))
            elif section.expanded:
                found_expanded = True

    # check for optional sections
    if any([section.optional for section in section_group.elements]):
        raise TextXSemanticError("Optional section in section group for command: '{}'.".format(parent_command(section_group).id))


_validation_visitor = {'GuiGrid': check_gui_grid, 'GuiSectionGroup': check_gui_section_group}


# -------------------------------

model_visitors = [
    _row_to_grid_visitor,
    _defaults_visitor,
    _convert_id_visitor,
    _validation_visitor,
]
