
from cid_generator_cli_parser import command, CommandInterface, command_method, parse_cli_args, invoke_commands, print_builtin_help, get_cli_args, \
    root_command_name, root_command_id, parameters as parameter_models, commands as command_models

from cid.cli import cli_generator
from cid.gui import gui_generator


class Interface(CommandInterface):
    @command_method()
    def cid_generator(self, args):
        self.cid_file = args['cid_file']
        self.root_command = args['root_command']
        self.dest_path = args['dest_path']

    @command_method(parent=cid_generator)
    def generate_cli(self, _):
        cli_generator.generate_cli(self.cid_file, self.root_command, self.dest_path)
        
    @command_method(parent=cid_generator)
    def generate_gui(self, _):
        gui_generator.generate_gui(self.cid_file, self.root_command, self.dest_path)
        
    @command_method(parent=cid_generator)
    def generate_both(self, _):
        cli_generator.generate_cli(self.cid_file, self.root_command, self.dest_path)
        gui_generator.generate_gui(self.cid_file, self.root_command, self.dest_path)
    

if __name__ == '__main__':
    invoke_commands(Interface().get_callbacks())
