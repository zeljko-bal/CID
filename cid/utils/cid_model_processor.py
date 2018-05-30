from cid.utils.common import element_type
from cid.utils.model_processor import ModelProcessor


class CidModelProcessor(ModelProcessor):
    def element_type_name(self, element):
        return element_type(element)

    @ModelProcessor.depth_first
    def process_model(self, model):
        for import_statement in model.imports:
            self.invoke(import_statement)
        for element in model.elements:
            if element_type(element) == 'Parameter':
                self.process_parameter(element)
            elif element_type(element) == 'Command':
                self.process_command(element)

    @ModelProcessor.depth_first
    def process_parameter(self, parameter):
        for choice in parameter.choices:
            self.invoke(choice)
        if parameter.cli:
            if parameter.cli.cli_pattern:
                self.invoke(parameter.cli.cli_pattern)
        for cli_alias in parameter.cli_aliases:
            self.invoke(cli_alias)
        for constraint in parameter.constraints:
            self.invoke(constraint)

    @ModelProcessor.depth_first
    def process_command(self, command):
        for parameter in command.parameters:
            if element_type(parameter) == 'Parameter':
                self.process_parameter(parameter)
            elif element_type(parameter) == 'ParameterReference':
                self.invoke(parameter)
        for subcommand in command.sub_commands:
            if element_type(subcommand) == 'Command':
                self.process_command(subcommand)
            elif element_type(subcommand) == 'CommandReference':
                self.invoke(subcommand)
        if command.constraints:
            self.invoke(command.constraints)
        for usage in command.usages:
            self.process_cli_group(usage)
        if command.gui:
            self.process_gui_structure(command.gui)

    @ModelProcessor.depth_first
    def process_cli_group(self, group):
        for element in group.elements:
            if hasattr(element, 'elements'):
                self.process_cli_group(element)
            else:
                self.invoke(element)

    @ModelProcessor.depth_first
    def process_gui_structure(self, gui_structure):
        for element in gui_structure.elements:
            self.process_gui_element(element)

    @ModelProcessor.depth_first
    def process_gui_element(self, gui_element):
        if element_type(gui_element) == 'GuiTabs':
            for tab in gui_element.elements:
                self.process_gui_tab(tab)
        elif element_type(gui_element) == 'GuiSectionGroup':
            for section in gui_element.elements:
                self.process_gui_element(section)
        elif element_type(gui_element) == 'GuiSection':
            self.process_gui_structure(gui_element.body)
        elif element_type(gui_element) == 'GuiGrid':
            for row in gui_element.elements:
                self.process_gui_grid_row(row)
        elif element_type(gui_element) == 'GuiGridRow':
            self.process_gui_grid_row(gui_element)
        elif element_type(gui_element) == 'Parameter':
            self.process_parameter(gui_element)
        elif element_type(gui_element) == 'ParameterReference':
            self.invoke(gui_element)

    @ModelProcessor.depth_first
    def process_gui_grid_row(self, gui_grid_row):
        for element in gui_grid_row.elements:
            if element_type(element) == 'Parameter':
                self.process_parameter(element)
            elif element_type(element) == 'ParameterReference':
                self.invoke(element)

    @ModelProcessor.depth_first
    def process_gui_tab(self, gui_tab):
        self.process_gui_structure(gui_tab.body)
