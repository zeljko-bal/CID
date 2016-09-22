
import os
from jinja2 import Environment, FileSystemLoader

from cid_parser import parse
from model_processor import ModelProcessor
from common import *
from model_printer import print_model

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

# ------------------------------- GUI MODEL PROCESSORS -------------------------------

def check_parameter_widget(parameter):
	if parameter.widget:
		supported_widgets = {
		 'Str':['password', 'text_field', 'text_area'],
		 'Choice':['dropdown', 'radio_buttons'],
		 'Num':['counter', 'slider'],
		}[element_type(parameter)]
		if parameter.widget not in supported_widgets:
			raise Exception('parameter.widget unsupported')

# -------------------------------

def usage_group_gui_structure(usage_group): # TODO refactor
	usage_group.gui_structure = GuiStructure(parent=None, elements=[])
	optional_elements = []
	
	for element in usage_group.elements:
		if element_type(element) == 'Parameter':
			usage_group.gui_structure.elements.append(element)
		elif element_type(element) == 'CliOptionalGroup':
			optional_elements += element.gui_structure
		elif element_type(element) == 'CliOrGroup':
			usage_group.gui_structure.elements.append(element.gui_structure)
			element.gui_structure.parent = usage_group.gui_structure

	if optional_elements:
		optionals_section = GuiSection(parent=usage_group.gui_structure, title='Optional Parameters', body=None, expanded=False, optional=True)
		optionals_section.body = GuiStructure(parent=optionals_section, elements=optional_elements)
		for opt in optional_elements:
			opt.parent = optionals_section.body
		usage_group.gui_structure.elements.append(optionals_section)
	
def usage_or_group_gui_structure(or_group):
	or_group.gui_structure = GuiSectionGroup(parent=None, elements=[], exclusive=True)
	
	for idx, or_element in enumerate(or_group.elements):
		section = GuiSection(parent=or_group.gui_structure, title='Section {}'.format(idx), body=None, expanded=idx==0, optional=False)
		if element_type(or_element) == 'Parameter':
			section.body = GuiStructure(parent=section, elements=[or_element])
		else:
			if element_type(or_element) == 'ParameterReference': print('!!!!!!!!!!!!!!!!', or_element.local)
			section.body = or_element.gui_structure
			section.body.parent = section
		or_group.gui_structure.elements.append(section)
	
def usage_optional_group_gui_structure(optional_group):
	optional_group.gui_structure = []
	optional_elements = []
	
	for element in optional_group.elements:
		if element_type(element) == 'Parameter':
			optional_group.gui_structure.append(element)
		elif element_type(element) == 'CliOptionalGroup':
			optional_elements += element.gui_structure
		elif element_type(element) == 'CliOrGroup':
			optional_group.gui_structure.append(element.gui_structure)
	
	if optional_elements:
		optionals_section = GuiSection(parent=None, title='Optional Parameters', body=None, expanded=False, optional=True)
		optionals_section.body = GuiStructure(parent=optionals_section, elements=optional_elements)
		for opt in optional_elements:
			opt.parent = optionals_section.body
		optional_group.gui_structure.append(optionals_section)
	
_add_default_gui_structure_visitor = {'CliStructure':usage_group_gui_structure, 'CliGroup':usage_group_gui_structure, 'CliOrGroup':usage_or_group_gui_structure, 'CliOptionalGroup':usage_optional_group_gui_structure}

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
				section = GuiSection(parent=section_group, title='Section {}'.format(idx), body=None, expanded=idx==0, optional=False)
				section.body = usage.gui_structure
				section.body.parent = section
				section_group.elements.append(section)
				
			command.gui = GuiStructure(parent=command, elements=[section_group])
	
# -------------------------------

def gui_section_group_defaults(section_group):
	if all([not section.expanded for section in section_group.elements]):
		section_group.elements[0].expanded = True
	
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

# ------------------------------- DATA EXTRACTORS -------------------------------

# ------------------------------- JINJA FILTERS -------------------------------

class UniqueId:
	def __init__(self):
		self.count = 0
	
	def make_unique(self, id):
		self.count += 1
		return '{id}_{count}'.format(id=id, count=self.count)

# ------------------------------- GENERATOR FUNCTIONS -------------------------------

def process_model(model):
	ModelProcessor({'GuiSectionGroup':gui_section_group_defaults, 'Command':gui_structure_defaults}).process_cli_group(model)
	ModelProcessor({'Parameter':check_parameter_widget, 'GuiGrid':check_gui_grid, 'GuiSectionGroup':check_gui_section_group}).process_cli_group(model)
	
	print_model(model, print_empty_attrs=False, print_empty_lists=True, omitted_attributes=[ 
		#'usage_help', 'long_usage_help', 
		'all_patterns', 
		'sub_elements',
	])
	
def render_gui_code(model, root_command_name, dest_path):
	# EXTRACT DATA ---------------------
	model_extractor = ElementExtractor()
	ModelProcessor(model_extractor.visitor).process_model(model)
	
	all_commands = model_extractor.all_commands
	all_parameters = model_extractor.all_parameters
	
	# RENDER CLI TEMPLATE ---------------------
	env = Environment(loader=FileSystemLoader('.'))
	
	env.filters['all_parent_commands'] = all_parent_commands
	env.filters['element_type'] = element_type
	env.filters['unique_id'] = UniqueId().make_unique
	'''env.filters['tab_indent'] = tab_indent_filter
	env.filters['stringify'] = stringify_filter
	env.filters['have_sub_commands'] = have_sub_commands_filter
	
	env.globals['raise'] = raise_exception_helper'''
	
	
	template = env.get_template('gui.template.html')
	
	rendered = template.render(root_command_name=root_command_name, root_command_id=element_id(root_command_name), commands=all_commands)

	with open(os.path.join(dest_path, "index.html"), "w") as text_file:
		text_file.write(rendered)

def generate_gui(cid_file, root_command_name, dest_path):
	model = parse(cid_file)
	process_model(model)
	render_gui_code(model, root_command_name, dest_path)
	
# ------------------------------- MAIN -------------------------------
	
if __name__ == '__main__':
	generate_gui('./example1.cid', 'command1', '../../material_html_template/generated-electron-quick-start/') # TODO src path as arg, # TODO root_command_name and dest path as args


# custom css []
# custom js, callbackci, da se moze zvati iz custom code []
# custom button u gui structure sa kodom [?][]