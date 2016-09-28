
import os
from collections import defaultdict, namedtuple
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
		
GuiRowDimensions = namedtuple('GuiRowDimensions', ['colspan', 'width'])

def html_id(id):
	return id.replace('/', '_')

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
	
	for element in usage_group.elements:
		if element_type(element) == 'Parameter':
			usage_group.gui_structure.elements.append(element)
		elif element_type(element) in ['CliOptionalGroup', 'CliOrGroup']:
			usage_group.gui_structure.elements.append(element.gui_structure)
			element.gui_structure.parent = usage_group.gui_structure

def usage_or_group_gui_structure(or_group):
	or_group.gui_structure = GuiSectionGroup(parent=None, elements=[], exclusive=True)
	
	for idx, or_element in enumerate(or_group.elements):
		section = GuiSection(parent=or_group.gui_structure, title='Variant: {}'.format(idx+1), body=None, expanded=idx==0, optional=False)
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
				section = GuiSection(parent=section_group, title='Variant: {}'.format(idx+1), body=None, expanded=idx==0, optional=False)
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
			width = round((100/len(grid_row.elements))*colspan)
			grid_row.dimensions.append(GuiRowDimensions(colspan, width))
		else:
			grid_row.dimensions.append(None)

# -------------------------------

def gui_section_group_defaults(section_group):
	if all([not section.expanded for section in section_group.elements]):
		section_group.elements[0].expanded = True
	
# -------------------------------

def convert_id(element):
	element.id = html_id(element.id)
	
_convert_id_visitor = {'Command':convert_id, 'Parameter':convert_id}

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

class UniqueIdGenerator:
	def __init__(self):
		self.id_counts = defaultdict(int)
	
	def make_new(self, id, id_format='{id}:{count}'):
		self.id_counts[id] += 1
		return self.get_current(id, id_format)
		
	def get_current(self, id, id_format='{id}:{count}'):
		return id_format.format(id=id, count=self.id_counts[id])

# ------------------------------- GENERATOR FUNCTIONS -------------------------------

def process_model(model):
	ModelProcessor([{'GuiSectionGroup':gui_section_group_defaults, 'Command':gui_structure_defaults, 'GuiGridRow':add_gui_grid_row_dimensions}, _convert_id_visitor]).process_model(model)
	ModelProcessor({'Parameter':check_parameter_widget, 'GuiGrid':check_gui_grid, 'GuiSectionGroup':check_gui_section_group}).process_model(model)
	
	'''print_model(model, print_empty_attrs=False, print_empty_lists=True, omitted_attributes=[ 
		#'usage_help', 'long_usage_help', 
		'all_patterns', 
		'sub_elements',
	])'''
	
def render_gui_code(model, root_command_name, dest_path):
	# EXTRACT DATA ---------------------
	model_extractor = ElementExtractor()
	ModelProcessor(model_extractor.visitor).process_model(model)
	
	all_commands = model_extractor.all_commands
	all_parameters = model_extractor.all_parameters
	
	# RENDER CLI TEMPLATE ---------------------
	unique_id_generator = UniqueIdGenerator()
	env = Environment(loader=FileSystemLoader('.'))
	
	env.filters['all_parent_commands'] = all_parent_commands
	env.filters['element_type'] = element_type
	env.filters['new_unique_id'] = unique_id_generator.make_new
	env.filters['current_unique_id'] = unique_id_generator.get_current
	env.filters['tab_indent'] = tab_indent_filter
	'''env.filters['stringify'] = stringify_filter
	env.filters['have_sub_commands'] = have_sub_commands_filter'''
	
	#env.globals['raise'] = raise_exception_helper
	
	
	template = env.get_template('gui.template.html')
	
	rendered = template.render(root_command_name=root_command_name, root_command_id=html_id(element_id(root_command_name)), commands=all_commands)

	with open(os.path.join(dest_path, "index.html"), "w") as text_file:
		text_file.write(rendered)

def generate_gui(cid_file, root_command_name, dest_path):
	model = parse(cid_file)
	process_model(model)
	render_gui_code(model, root_command_name, dest_path)
	import winsound; winsound.PlaySound('turret_collide_2.wav', winsound.SND_FILENAME)
	
# ------------------------------- MAIN -------------------------------
	
if __name__ == '__main__':
	generate_gui('./example1.cid', 'command1', '../../material_html_template/generated-electron-quick-start/') # TODO src path as arg, # TODO root_command_name and dest path as args

	
	
!!!!!!!!!!!!! 
- nema vise none_allowed
- ima empty_str = allowed/disalowed samo za string, po defaultu je True ako je default=''
- defaults:
	"Str":None,
	"Num":None,
	"Bool":'False',
	"Date":None,
	"File":None,
	"Choice":None
(tehnicki 
if not parameter.default:
	if parameter.type == 'Bool': 
		parameter.default = 'False' sem ako postoji pos i neg pattern, onda je none
)
- switch ima samo za string ako je empty_str_allowed (i za multiple i count many str), kad je iskljucen i klikne se na polje automatski se ukljuci, ostali imaju fazon za none
- u many ako su sva polja prazna onda je ceo param none



# sub commands [v]
# default = none [v]
# param count [] # za File: You can also use the multiple attribute to allow multiple file uploads. 
# multi param []
# param description prikaz []
# param help prikaz []
# command help prikaz []
# default data json i ucitavanje []
# detektovanje koji je popunjen, update vrednosti u model, ignorisuci collapsed sections []
# na detekciju promene modela:
	# ako je neki popunjen i u subelements je od optional ili or, ostali koji nisu popunjeni su obavezni []
	# ako je neki popunjen u nekom od or grupa, za ostale koje ga nemaju svi koji nisu popunjeni su disabled []
	# ako je neki popunjen u nekom od usagea ako usage nema sub_command onda su dugmad disabled []
# generisanje cli string na osnovu modela []
# widgeti da se generisu []
# date_format da se generise kako treba []
# custom css [v]
# custom js, callbackci, da se moze zvati iz custom code []
# custom button u gui structure sa kodom [?][]

# sve sa constraints []
# sve sa code block []