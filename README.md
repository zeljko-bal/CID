# CID - Command Interface Description Language

>CID is a domain specific language that can be used to describe command interfaces such as those commonly found in cli applications. It can be used to generate command line and/or graphical user interfaces.

The metamodel consists of concepts such as a command, a parameter, a constraint and so on.. using which you can describe an interface and based on that description generate a cli and / or gui application interfaces.

The CLI generator generates a cli parser implemented as a couple of python modules which you can call by providing hooks that implement your business logic for each command. When the script is invoked with certain arguments the generated cli parser will parse the arguments and invoke the corresponding hook functions supplying them with the argument values.

The GUI generator will generate an app based on the [Electron](https://electron.atom.io/) framework that represents an input form, which when executed will generate and invoke a cli command based on the user input. The gui app can be used on top of an existing cli application or on top of the newly generated one using the same CID script.

*The generators currently only support windows, but as the underlying frameworks and languages that were used are cross platform, the support for other operating systems can be added with just a bit of shell scripting.

## Quick Start:

You can try generating interfaces based on the provided example scripts. The generator interfaces themselves have been generated using the CID generator.

### Dependencies:
These need to be installed first:
- Python 3.6.2
- Electron v1.3.3 (https://electron.atom.io/) (must be in PATH)

### Install:
Simply install the project using pip.
```cmd
> cd <cid_root_directory>
> pip install .
```

### Test Run:
To run the generator you need to specify a .cid script (for example the provided example1.cid), the name of a command found in the .cid script that will be a root command of the interface (in this case 'command1'), a destination directory where to generate the apps and what you want to generate ('generate_cli', 'generate_gui' or 'generate_both'). 

```cmd
> cid_generator <cid_root_directory>/examples/example1.cid command1 <some_destination_directory> generate_both
# or if you prefer gui
> cid_generator_gui
# and then run the example command
> cd <some_destination_directory>
> command1_gui
```

## Licence:
Licensed under MIT license.