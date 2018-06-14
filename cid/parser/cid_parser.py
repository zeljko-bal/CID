from os.path import realpath, join, dirname

from textx.metamodel import metamodel_from_file

from cid.parser import pre_processing, post_processing
from cid.parser.cid_model_specs import CidModelSpecs
from cid.parser.reference_resolver import ReferenceResolver, ImportedReferenceDefinition
from cid.common.cid_model_processor import CidModelProcessor
from cid.common.utils import *


def parse(script_path):
    grammar_path = join(dirname(realpath(__file__)), 'grammar', 'cid_grammar.tx')
    metamodel = metamodel_from_file(grammar_path, autokwd=True)
    
    # FIRST PASS ---------------------

    metamodel.register_obj_processors(pre_processing.object_processors)

    model = metamodel.model_from_file(script_path)

    # EXTRACT DATA ---------------------

    model_extractor = ElementExtractor()
    CidModelProcessor(model_extractor.visitor).process_model(model)

    all_defined_commands = model_extractor.all_commands
    all_defined_parameters = model_extractor.all_parameters

    # DEREFERENCE ---------------------

    parameter_instances = {instance.name: instance for instance in all_defined_parameters}
    command_instances = {instance.name: instance for instance in all_defined_commands}

    script_directory = dirname(script_path)
    external_models = {file_path: parse(join(script_directory, file_path)) for file_path in set([_import.file_path for _import in model.imports])}
    import_definitions = {_import.alias: ImportedReferenceDefinition(_import.alias, _import.element_name, external_models[_import.file_path], _import.file_path) for _import in model.imports}

    reference_resolver = ReferenceResolver(parameter_instances, command_instances, import_definitions)
    reference_resolver_visitor = {'ParameterReference': reference_resolver.resolve_parameter_reference, 'CommandReference': reference_resolver.resolve_command_reference}

    CidModelProcessor(reference_resolver_visitor).process_model(model)

    # SECOND PASS ---------------------

    for visitor in post_processing.model_visitors:
        CidModelProcessor(visitor).process_model(model)

    # CHECK SPECS ---------------------

    CidModelProcessor(CidModelSpecs().visitor).process_model(model)

    # ---------------------

    return model
