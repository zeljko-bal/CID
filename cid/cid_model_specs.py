from cid.utils.common import parent_command
from cid.utils.model_specs import ModelSpecs, spec, SpecModelNode


class CidModelSpecs(ModelSpecs):
    @spec('Script')
    def script_specs(self, script: SpecModelNode):
        script.should_have_filled('elements')
        script.should_have('imports')
        script.should_have('free_commands')
        script.should_have('free_parameters')

    @spec('Command')
    def command_specs(self, command: SpecModelNode):
        command.should_have_filled('id')
        command.should_have_filled('name')
        command.should_have_filled('title')
        command.should_have('description')
        command.should_have('help')
        command.should_have('parameters')
        command.should_have('sub_commands')
        command.should_have('constraints')
        command.should_have_filled('cli_command')
        command.should_have('help_params')
        command.should_have('no_help')
        command.should_have('long_help_params')
        command.should_have('no_long_help')
        command.should_have('usages')
        command.shouldnt_have('usage')
        command.should_have('gui')

    @spec('Parameter')
    def parameter_specs(self, parameter: SpecModelNode):
        parameter.should_have_filled('id')
        parameter.should_have_filled('type')
        parameter.should_have_filled('name')
        parameter.should_have_filled('title')
        parameter.should_have_filled('description')
        parameter.should_have('help')
        parameter.should_have('default')
        parameter.should_have('empty_str_allowed')
        parameter.should_have('cli')
        parameter.should_have('cli_aliases')
        if parameter.is_of_type('Bool'):
            parameter.should_have_filled('cli')
        parameter.should_have('constraints')
        parameter.should_have('nonpositional')
        if parameter.value.nonpositional:
            parameter\
                .should_have_filled('cli')\
                .should_have_filled('cli_pattern')\
                .should_have_filled('parent')
            parameter.should_have('all_patterns')
            for pattern in parameter.each('all_patterns'):
                if pattern.has_filled('vars'):
                    pattern.should_have('count')
                    parameter.should_have_filled('cli_pattern_vars')
            parameter.should_have('empty_str_disallowed')
        else:
            parameter.shouldnt_have('empty_str_disallowed')
        parameter.should_have('cli_pattern_count')
        parameter.should_have_filled('multiplicity')
        parameter.shouldnt_have('default_is_none')
        if parameter.is_of_type('Bool'):
            parameter.should_have('none_allowed')
        if parameter.is_of_type('Date'):
            parameter.should_have('date_format')
        if parameter.get('type').value == 'Choice':
            parameter.should_have_filled('choices')
        if parameter.get('type').value == 'Date':
            parameter.should_have_filled('date_format')

    @spec('ParameterCliValue')
    def parameter_cli_value_specs(self, parameter_cli_value: SpecModelNode):
        parameter_cli_value.should_have_filled('cli_pattern')

    @spec('StringParamPattern')
    def string_param_pattern_specs(self, string_param_pattern: SpecModelNode):
        string_param_pattern.should_have_filled('prefix')
        string_param_pattern.should_have('white_space')
        string_param_pattern.should_have('vars')
        string_param_pattern.should_have('count')
        string_param_pattern.should_have('count_many')
        string_param_pattern.should_have('separator')
        string_param_pattern.should_have('count_char')

    @spec('BoolWithPositivePattern')
    def bool_with_positive_pattern_specs(self, bool_with_positive_pattern: SpecModelNode):
        bool_with_positive_pattern.should_have_filled('positive')
        bool_with_positive_pattern.should_have('negative')

    @spec('BoolNegativeOnlyPattern')
    def bool_with_negative_only_pattern_specs(self, bool_with_negative_only_pattern: SpecModelNode):
        bool_with_negative_only_pattern.should_have_filled('negative')
        bool_with_negative_only_pattern.should_have_empty('positive')

    @spec('ParameterReference')
    def parameter_reference_specs(self, parameter_reference: SpecModelNode):
        parameter_reference.should_exist()

    @spec('CommandReference')
    def command_reference_specs(self, command_reference: SpecModelNode):
        command_reference.should_exist()

    @spec('CodeBlock')
    def code_block_specs(self, code_block: SpecModelNode):
        code_block.should_have_filled('code')

    # constraints:

    @spec('CommandConstraint')
    def command_constraint_specs(self, constraint: SpecModelNode):
        constraint.should_have_filled('code_block')
        constraint.should_have_filled('message')

    @spec('NumericValueConstraint')
    def numeric_value_constraint_specs(self, constraint: SpecModelNode):
        constraint.should_have_filled('type')
        constraint.should_have_filled('value')
        constraint.should_have_filled('message')

    @spec('DateConstraint')
    def date_constraint_specs(self, constraint: SpecModelNode):
        constraint.should_have_filled('type')
        constraint.should_have_filled('value')
        constraint.should_have_filled('message')

    @spec('LengthConstraint')
    def length_constraint_specs(self, constraint: SpecModelNode):
        constraint.should_have_filled('type')
        constraint.should_have_filled('value')
        constraint.should_have_filled('message')

    @spec('StringFlagConstraint')
    def string_flag_constraint_specs(self, constraint: SpecModelNode):
        constraint.should_have_filled('type')
        constraint.should_have_filled('message')

    @spec('NumberFlagConstraint')
    def number_flag_constraint_specs(self, constraint: SpecModelNode):
        constraint.should_have_filled('type')
        constraint.should_have_filled('message')

    @spec('FileFlagConstraint')
    def file_flag_constraint_specs(self, constraint: SpecModelNode):
        constraint.should_have_filled('type')
        constraint.should_have_filled('message')

    @spec('RegexConstraint')
    def regex_constraint_specs(self, constraint: SpecModelNode):
        constraint.should_have_filled('value')
        constraint.should_have_filled('message')

    @spec('CodeConstraint')
    def regex_constraint_specs(self, constraint: SpecModelNode):
        constraint.should_have_filled('value')
        constraint.should_have_filled('message')

    # cli structure:

    @spec('CliStructureMultiLine')
    def cli_structure_specs(self, cli_structure: SpecModelNode):
        cli_structure.shouldnt_exist()

    @spec('CliStructure')
    def cli_structure_specs(self, cli_structure: SpecModelNode):
        self.common_cli_element_specs(cli_structure)
        cli_structure.should_have('has_options')
        cli_structure.should_have('has_subcommand')

    @spec('CliGroup')
    def cli_group_specs(self, cli_group: SpecModelNode):
        self.common_cli_element_specs(cli_group)

    @spec('CliOptionalGroup')
    def cli_optional_group_specs(self, cli_optional_group: SpecModelNode):
        self.common_cli_element_specs(cli_optional_group)

    @spec('CliOrGroup')
    def cli_or_group_specs(self, cli_or_group: SpecModelNode):
        self.common_cli_element_specs(cli_or_group)
        cli_or_group.shouldnt_have('lhs')
        cli_or_group.shouldnt_have('rhs')

    def common_cli_element_specs(self, cli_element):
        self.common_structure_group_specs(cli_element)
        if any([element.is_of_type('CliSeparator') for element in cli_element.each('elements')]):
            cli_element.should_have_true('has_cli_separator')

    @spec('CliSeparator')
    def cli_separator_spec(self, cli_separator: SpecModelNode):
        cli_separator.should_have_filled('value')
        cli_separator.should_have_filled('usage_repr')
        cli_separator \
            .map(lambda sep: parent_command(sep), 'parent_command') \
            .should_have_filled('cli_separators')

    # gui structure:

    @spec('GuiStructure')
    def gui_structure_spec(self, gui_structure: SpecModelNode):
        self.common_structure_group_specs(gui_structure)

    @spec('GuiTabs')
    def gui_tabs_spec(self, gui_tabs: SpecModelNode):
        self.common_structure_group_specs(gui_tabs)

    @spec('GuiSectionGroup')
    def gui_section_group_spec(self, gui_section_group: SpecModelNode):
        self.common_structure_group_specs(gui_section_group)
        gui_section_group.should_have('exclusive')

    @spec('GuiSection')
    def gui_section_spec(self, gui_section: SpecModelNode):
        gui_section.should_have_filled('body')
        gui_section.should_have('expanded')
        gui_section.should_have('optional')

    @spec('GuiGrid')
    def gui_grid_spec(self, gui_grid: SpecModelNode):
        self.common_structure_group_specs(gui_grid)

    @spec('GuiTab')
    def gui_tab_spec(self, gui_tab: SpecModelNode):
        gui_tab.should_have_filled('body')

    @spec('GuiGridRow')
    def gui_grid_row_spec(self, gui_grid_row: SpecModelNode):
        self.common_structure_group_specs(gui_grid_row)

    @staticmethod
    def common_structure_group_specs(structure_element):
        structure_element.should_have('sub_elements')
        structure_element.should_have('elements')
