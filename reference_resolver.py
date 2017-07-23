from common import *


class ImportedReferenceDefinition:
    def __init__(self, reference_id: str, element_name: str, script_model, file_path: str):
        self.element_name = element_name
        self.script_model = script_model
        self.file_path = file_path
        self.reference_id = reference_id

    def get_instance(self, el_type: str):
        for instance in self.script_model.elements:
            if element_type(instance) == el_type and instance.name == self.element_name:
                return instance
        else:
            raise Exception("Unresolved imported reference: {ref_id}, cannot find instance of: '{el_name}' in imported model: {model_path}.".format(
                ref_id=self.reference_id, el_name=self.element_name, model_path=self.file_path))


class ReferenceResolver:
    def __init__(self, parameter_instances, command_instances, imports_definitions):
        self._parameter_instances = parameter_instances
        self._command_instances = command_instances
        self._imports_definitions = imports_definitions

    def resolve_parameter_reference(self, parameter_reference):
        if parameter_reference.local:
            self.resolve_local_reference(parameter_reference, self._parameter_instances, self.replace_parameter_reference)
        else:
            self.resolve_imported_parameter_reference(parameter_reference)

    def resolve_imported_parameter_reference(self, parameter_reference):
        if parameter_reference.imported not in self._imports_definitions:
            raise Exception("Unresolved imported reference: {}, cannot find import statement.".format(parameter_reference.imported))

        import_definition = self._imports_definitions[parameter_reference.imported]

        instance = import_definition.get_instance('Parameter')

        # check for name collision
        for resolved in [p for p in parent_command(parameter_reference).parameters if element_type(p) == 'Parameter']:
            if resolved.name == import_definition.element_name and resolved is not instance:
                raise Exception('Parameter name collision between {cmd}.{param} and an imported parameter from {path}.'.format(
                    cmd=parent_command(parameter_reference).name, param=import_definition.element_name, path=import_definition.file_path))

        # replace the reference with the actual instance
        self.replace_parameter_reference(parameter_reference, instance)

    def resolve_command_reference(self, command_reference):
        if command_reference.local:
            self.resolve_local_reference(command_reference, self._command_instances, self.replace_command_reference)
        else:
            self.resolve_imported_command_reference(command_reference)

    def resolve_imported_command_reference(self, command_reference):
        if command_reference.imported not in self._imports_definitions:
            raise Exception("Unresolved imported reference: {}, cannot find import statement.".format(command_reference.imported))

        import_definition = self._imports_definitions[command_reference.imported]

        instance = import_definition.get_instance('Command')

        # check for name collision
        if import_definition.element_name in [c.name for c in command_reference.parent.sub_commands]:
            raise Exception('Command name collision between {cmd}.{subcmd} and an imported command from {path}.'.format(
                cmd=command_reference.parent.name, subcmd=import_definition.element_name, path=import_definition.file_path))

        # replace the reference with the actual instance
        self.replace_command_reference(command_reference, instance)

    @staticmethod
    def resolve_local_reference(reference, instances, reference_replacer):
        if reference.local not in instances:
            raise Exception("Unresolved local reference: {}".format(reference.local))

        instance = instances[reference.local]

        # if the instance is defined as a free element or in the enclosing command
        if element_type(instance.parent) == 'Script' or instance.parent is parent_command(reference):
            # replace the reference with the actual instance
            reference_replacer(reference, instance)

    @staticmethod
    def replace_parameter_reference(parameter_reference, instance):
        if hasattr(parameter_reference.parent, 'parameters'):
            idx = parameter_reference.parent.parameters.index(parameter_reference)
            parameter_reference.parent.parameters[idx] = instance
        elif hasattr(parameter_reference.parent, 'elements'):
            idx = parameter_reference.parent.elements.index(parameter_reference)
            parameter_reference.parent.elements[idx] = instance
        else:
            raise Exception("Internal error: ReferenceResolver.replace_parameter_reference: wrong parent type.")

    @staticmethod
    def replace_command_reference(command_reference, instance):
        idx = command_reference.parent.sub_commands.index(command_reference)
        command_reference.parent.sub_commands[idx] = instance
