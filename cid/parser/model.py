
# ------------------------------- ADDITIONAL MODELS -------------------------------


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
