
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
