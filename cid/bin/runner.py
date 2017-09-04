from subprocess import Popen
from os.path import realpath, join, dirname
import sys

_bin_path = join(dirname(realpath(__file__)))

def run_cid_generator_cli():
    run_command("cid_generator.bat")
    
def run_cid_generator_gui():
    run_command("cid_generator_gui.bat")
    
def run_command(command):
    Popen([join(_bin_path, command), *sys.argv[1:]], cwd=_bin_path).communicate()
