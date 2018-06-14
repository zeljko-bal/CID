from cid.common.model_specs import ModelSpecs, spec, SpecModelNode


class CliModelSpecs(ModelSpecs):
    @spec('Parameter')
    def parameter_specs(self, parameter: SpecModelNode):
        if parameter.has_true('nonpositional'):
            parameter.should_have_filled('prefixes')
        if parameter.get('type').value == 'Bool':
            parameter.should_have('pos_prefixes')
            parameter.should_have('neg_prefixes')
        parameter.should_have_filled('usage_repr')
        parameter.should_have_filled('description')

    @spec('Command')
    def command_specs(self, command: SpecModelNode):
        command.should_have_filled('help_params')
        command.should_have_filled('long_help_params')
        command.should_have_filled('usage_help')
        command.should_have_filled('long_usage_help')

    @spec('CliStructure')
    def cli_structure_specs(self, cli_structure: SpecModelNode):
        cli_structure.should_have('string_repr')

    @spec('CliGroup')
    def cli_group_specs(self, cli_group: SpecModelNode):
        cli_group.should_have('string_repr')

    @spec('CliOptionalGroup')
    def cli_optional_group_specs(self, cli_optional_group: SpecModelNode):
        cli_optional_group.should_have('string_repr')

    @spec('CliOrGroup')
    def cli_or_group_specs(self, cli_or_group: SpecModelNode):
        cli_or_group.should_have('string_repr')
