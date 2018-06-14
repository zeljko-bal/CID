from cid.common.model_specs import spec, ModelSpecs, SpecModelNode


class GuiModelSpecs(ModelSpecs):
    @spec('Command')
    def command_specs(self, command: SpecModelNode):
        command.should_have_filled('gui')

    @spec('GuiGridRow')
    def gui_grid_row_specs(self, gui_grid_row: SpecModelNode):
        gui_grid_row.should_have_filled('dimensions')
