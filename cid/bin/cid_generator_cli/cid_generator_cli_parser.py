
'''
Automatically generated code. Do not edit directly.
'''

from datetime import datetime
from generic_cli_parser import CommandParserModel, ParameterModel, BasicNonpositional, MultiArgNonpositional, SeparatedNonpositional, \
    CounterNonpositional,   BooleanNonpositional, ParameterGroup, OrGroup, OptionalElement, NonPositionalParameter, \
    PositionalParameter, ParameterSeparator, SubCommand, \
    NumericValueConstraintValidator, DateConstraintValidator, LengthConstraintValidator, StringFlagConstraintValidator, \
    NumberFlagConstraintValidator, FileFlagConstraintValidator, RegexConstraintValidator, CodeConstraintValidator, CommandCodeConstraintValidator, \
    parse_cli_args as _parse_cli_args, invoke_commands as _invoke_commands, print_builtin_help as _print_builtin_help
    
root_command_name = 'cid_generator'
root_command_id = '/cid_generator'

# -------------------- PARAMETER MODEL DEFINITIONS --------------------

parameters = {
    '/cid_generator/cid_file' : ParameterModel(
        name='cid_file',
        type='File',
        usage_model=PositionalParameter('cid_file'),
        default=None,
        constraints=[
            FileFlagConstraintValidator('exists', '''The provided file doesn't exist.'''),
            FileFlagConstraintValidator('is_file', '''The provided path is not a file.'''),
            RegexConstraintValidator('.+\.cid$', '''must be a cid script file (*.cid)'''),
        ],
    ),
    '/cid_generator/root_command' : ParameterModel(
        name='root_command',
        type='Str',
        usage_model=PositionalParameter('root_command'),
        default=None,
    ),
    '/cid_generator/dest_path' : ParameterModel(
        name='dest_path',
        type='File',
        usage_model=PositionalParameter('dest_path'),
        default=None,
        constraints=[
            FileFlagConstraintValidator('exists', '''The provided file doesn't exist.'''),
            FileFlagConstraintValidator('is_directory', '''The provided path is not a directory.'''),
        ],
    ),
}

# -------------------- COMMAND MODEL DEFINITIONS --------------------

commands = {
    '/cid_generator/generate_cli' : CommandParserModel(
        id='/cid_generator/generate_cli',
        name='generate_cli',
        cli_command='generate_cli',
        usage_model=ParameterGroup([
		]),
        builtin_help_params=['-h', '--help'],
        builtin_long_help_params=['-a', '--all'],
    ),
    '/cid_generator/generate_gui' : CommandParserModel(
        id='/cid_generator/generate_gui',
        name='generate_gui',
        cli_command='generate_gui',
        usage_model=ParameterGroup([
		]),
        builtin_help_params=['-h', '--help'],
        builtin_long_help_params=['-a', '--all'],
    ),
    '/cid_generator/generate_both' : CommandParserModel(
        id='/cid_generator/generate_both',
        name='generate_both',
        cli_command='generate_both',
        usage_model=ParameterGroup([
		]),
        builtin_help_params=['-h', '--help'],
        builtin_long_help_params=['-a', '--all'],
    ),
    '/cid_generator' : CommandParserModel(
        id='/cid_generator',
        name='cid_generator',
        cli_command='cid_generator',
        parameter_models=[
            parameters['/cid_generator/cid_file'],
            parameters['/cid_generator/root_command'],
            parameters['/cid_generator/dest_path'],
        ],
        usage_model=ParameterGroup([
			parameters['/cid_generator/cid_file'].usage_model,
			parameters['/cid_generator/root_command'].usage_model,
			parameters['/cid_generator/dest_path'].usage_model,
		    SubCommand(),
		]),
        builtin_help_params=['-h', '--help'],
        builtin_long_help_params=['-a', '--all'],
    ),
}
# -------------------- SUB COMMANDS --------------------

commands['/cid_generator'].sub_commands = [commands['/cid_generator/generate_cli'], commands['/cid_generator/generate_gui'], commands['/cid_generator/generate_both'], ]

# -------------------- COMMAND USAGE HELP --------------------

# /cid_generator/generate_cli usage_help
commands['/cid_generator/generate_cli'].usage_help = '''Usage:  cid_generator generate_cli 

Parameters:
  -h, --help  Shows this help message. For more detailed help type: cid_generator
              generate_cli -h -a.'''

# /cid_generator/generate_cli long_usage_help
commands['/cid_generator/generate_cli'].long_usage_help = '''Usage:  cid_generator generate_cli 

Parameters:
  -h, --help  Shows a shorter help message. For this help message type:
              cid_generator generate_cli -h -a. All detailed help parameters: -a,
              --all.'''

# /cid_generator/generate_gui usage_help
commands['/cid_generator/generate_gui'].usage_help = '''Usage:  cid_generator generate_gui 

Parameters:
  -h, --help  Shows this help message. For more detailed help type: cid_generator
              generate_gui -h -a.'''

# /cid_generator/generate_gui long_usage_help
commands['/cid_generator/generate_gui'].long_usage_help = '''Usage:  cid_generator generate_gui 

Parameters:
  -h, --help  Shows a shorter help message. For this help message type:
              cid_generator generate_gui -h -a. All detailed help parameters: -a,
              --all.'''

# /cid_generator/generate_both usage_help
commands['/cid_generator/generate_both'].usage_help = '''Usage:  cid_generator generate_both 

Parameters:
  -h, --help  Shows this help message. For more detailed help type: cid_generator
              generate_both -h -a.'''

# /cid_generator/generate_both long_usage_help
commands['/cid_generator/generate_both'].long_usage_help = '''Usage:  cid_generator generate_both 

Parameters:
  -h, --help  Shows a shorter help message. For this help message type:
              cid_generator generate_both -h -a. All detailed help parameters: -a,
              --all.'''

# /cid_generator usage_help
commands['/cid_generator'].usage_help = '''Usage:  cid_generator <CID_FILE> <ROOT_COMMAND> <DEST_PATH> <sub_command>

Parameters:
  <DEST_PATH>     Data type: File.
  <ROOT_COMMAND>  Data type: String.
  <CID_FILE>      Data type: File.
  -h, --help      Shows this help message. For more detailed help type:
                  cid_generator -h -a.

Sub Commands:
  generate_cli   
  generate_gui   
  generate_both  

For help about a speciffic sub command type: cid_generator <sub_command> -h.'''

# /cid_generator long_usage_help
commands['/cid_generator'].long_usage_help = '''Usage:  cid_generator <CID_FILE> <ROOT_COMMAND> <DEST_PATH> <sub_command>

Parameters:
  <DEST_PATH>     Data type: File.
  <ROOT_COMMAND>  Data type: String.
  <CID_FILE>      Data type: File.
  -h, --help      Shows a shorter help message. For this help message type:
                  cid_generator -h -a. All detailed help parameters: -a, --all.

Sub Commands:
  generate_cli   
  generate_gui   
  generate_both  

For help about a speciffic sub command type: cid_generator <sub_command> -h.'''

# -------------------- ARGUMENT PARSING FUNCTIONS --------------------

def get_cli_args():
    import sys
    return sys.argv[1:]
    
_annotated_callbacks = None

class command:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        
    def __call__(self, func):
        global _annotated_callbacks
    
        self.define_sub_commands(func)
            
        if not self.name:
            self.name = func.__name__
            
        if not self.parent:
            if _annotated_callbacks:
                raise Exception("More than one root command encountered.")
            else:
                _annotated_callbacks = func, func.sub_commands
        else:
            self.define_sub_commands(self.parent)
            self.parent.sub_commands[self.name] = func, func.sub_commands
            
        return func
        
    @staticmethod
    def define_sub_commands(func):
        if not hasattr(func, 'sub_commands'):
            func.sub_commands = {}
            
class CommandInterface:
    def get_callbacks(self):
        callbacks = [callback for callback in [getattr(self, attr_name) for attr_name in dir(self)] if hasattr(callback, 'is_command_method')]
        if not callbacks:
           raise Exception("No callbacks specified.")
        root_commands = [callback for callback in callbacks if not callback.parent]
        if not root_commands:
            raise Exception("No root command specified.")
        if len(root_commands) > 1:
            raise Exception("More than one root command encountered.")
        root_command = root_commands[0]
        
        return root_command, self._get_sub_commands(root_command.name, callbacks)
    
    def _get_sub_commands(self, parent_name, callbacks):
        return {callback.name : (callback, self._get_sub_commands(callback.name, callbacks)) for callback in callbacks if callback.parent and callback.parent.name == parent_name}
    
class command_method:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        
    def __call__(self, func):
        if not self.name:
            self.name = func.__name__
        func.name = self.name
        func.parent = self.parent
        func.is_command_method = True
        return func

def parse_cli_args(args=None):
    if args is None:
        args = get_cli_args()
    
    return _parse_cli_args(root_command_id, commands, args)
    
def invoke_commands(command_callbacks=None, args=None):
    global _annotated_callbacks
    
    if args is None:
        args = get_cli_args()
    
    if not command_callbacks:
        if not _annotated_callbacks:
            raise Exception("No callbacks provided.")
        command_callbacks = _annotated_callbacks
    
    _invoke_commands(command_callbacks, root_command_id, commands, args)

def print_builtin_help(args=None):
    if args is None:
        args = get_cli_args()
    
    _print_builtin_help(root_command_id, commands, args)