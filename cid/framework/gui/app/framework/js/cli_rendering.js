
// ------------------- CLI COMMAND RENDERING -------------------
	
function get_current_cli_string()
{
	const command_results = get_command_results();
	return get_cli_string(command_results);
}
	
function get_cli_string(command_results)
{
	return Object.keys(command_results)
		.reduce((previous, command_id) => 
		{
			const command_result = command_results[command_id];
			const command_cli_string = get_command_cli_string(command_result.context, command_result.param_values);
			if(command_cli_string)
				return previous + ' ' + command_result.model.cli_command + ' ' + command_cli_string;
			else 
				return previous + ' ' + command_result.model.cli_command;
		}, '');
}

function get_command_cli_string(result, param_values)
{
	if(!result.matched.length)
		return '';
	
	return result.matched
		.map(m => 
		{
			if (m.model)
			{
				const value = param_values.get(m.model.id);
				return m.generate_str(value);
			}
			return m.generate_str();
		})
		.reduce((previous, param_str) => param_str ? previous + ' ' + param_str : previous);
}

function get_cli_list(command_results)
{
	return Object.keys(command_results)
		.reduce((previous, command_id) => 
		{
			const command_result = command_results[command_id];
			return [...previous, ...get_command_cli_list(command_result.context, command_result.param_values)];
		}, []);
}

function get_command_cli_list(result, param_values)
{
	return result.matched
		.map(m => 
		{
			if (m.model)
			{
				const value = param_values.get(m.model.id);
				return m.generate_list(value);
			}
			return m.generate_list();
		})
		.reduce((previous, params) => [...previous, ...params], []);
}

// ------------------- VALUE EXTRACTION -------------------

function get_command_results()
{
	return current_commands
		.reduce((results, command_id) => 
		{
			const command_model = command_models[command_id];
			const param_values = get_gui_structure_parameter_values(command_model.gui_structure);
			const result_context = command_model.usage_structure.match(param_values);
			
			results[command_id] = {model: command_model, param_values: param_values, context: result_context};
			return results;
		}, {});
}

function get_gui_structure_parameter_values(gui_structure)
{
	let values = new Map();
	let accumulate_values = new_vals => values = new Map([...values, ...new_vals]);
	
	for(let element of gui_structure)
	{
		clear_error_message(element.gui_id);
		
		switch(element.constructor.name)
		{
			case 'GuiTabs':
			{
				let new_vals = get_gui_structure_parameter_values(element.elements);
				accumulate_values(new_vals);
				break;
			}
			case 'GuiSectionGroup':
			{
				for(let section of element.elements)
				{
					if(is_section_active(section) || !element.exclusive)
					{
						let new_vals = get_gui_structure_parameter_values(section.elements);
						accumulate_values(new_vals);
					}
				}
				break;
			}
			case 'GuiGrid':
			{
				for(let row of element.elements)
				{
					let new_vals = get_gui_structure_parameter_values(row.elements);
					accumulate_values(new_vals);
				}
				break;
			}
			case 'GuiParameter':
			{
				let param_value = get_gui_parameter_value(element);
				
				if(param_value)
				{
					const validation_result = validate_parameter(param_value.value, element.model);
					
					if(validation_result.is_valid)
					{
						values.set(param_value.id, param_value.value);
					}
					else
					{
						const message = validation_result.generate_message(param_value.value, element.model);
						set_error_message(message, element.gui_id);
					}
				}
				break;
			}
		}
	}
	
	return values;
}

function get_gui_parameter_value(parameter)
{
	let value;
	let param_model = parameter.model;
	let param_wrapper = $('[data-gui-id='+parameter.gui_id+'].parameter-wrapper');
	
	let none_switch = param_wrapper.find('.none-switch');
	if(none_switch.length && !none_switch.find('input').prop('checked')) // if none switch exists and its off
	{
		return null;
	}
	
	if(param_model.type == 'Bool')
	{
		let cb = param_wrapper.find('input');
		value = get_checkbox_state(cb);
	}
	else
	{
		let input_collection = param_wrapper.find('.input-collection');
		let input_list = param_wrapper.find('.input-list');
		if(input_collection.length)
		{
			let collection_values = [];
			
			for(input_list of input_collection.find('.collection-item .input-list').get())
			{
				input_list = $(input_list);
				let input_list_values = get_input_list_parameter_values(input_list, param_model);
				if(input_list_values)
				{
					collection_values.push(input_list_values);
				}
			};
			
			if(collection_values.length)
			{
				value = collection_values;
			}
		}
		else if(input_list.length)
		{
			let input_list_values = get_input_list_parameter_values(input_list, param_model);
			if(input_list_values)
			{
				value = input_list_values;
			}
		}
		else
		{
			let input_field = param_wrapper.find('.input-field');
			value = get_input_field_value(input_field, param_model);
		}
	}
	
	if(value != null)
	{
		return {'id': parameter.model.id, 'value': value};
	}
	else
	{
		return null;
	}
}

function get_input_list_parameter_values(input_list, param_model)
{
	let values = [];
	
	for(input_field of input_list.find('.input-field').get())
	{
		input_field = $(input_field);
		let val = get_input_field_value(input_field, param_model);
		if(val != null)
		{
			values.push(val);
		}
	};
	
	let exact_count = param_model.count != '*' && param_model.count > 1;
	
	if(values.length > 0 && !(exact_count && param_model.count != values.length))
	{
		return values;
	}
	else
	{
		return null;
	}
}

function get_input_field_value(input_field, param_model)
{
	let value = null;
	switch(param_model.type)
	{
		case 'Str':
		case 'Num':
		case 'Date':
		case 'Choice':
		{
			let elem_name = param_model.type == 'Choice' ? 'select' : 'input';
			value = input_field.find(elem_name).val();
			
			if(!param_model.empty_str_allowed && value == '')
			{
				value = null;
			}
			
			if(param_model.type == 'Date' && param_model.date_format)
			{
				value = new Date(value).toString(param_model.date_format);
			}
			
			return value;
		}
		case 'File':
		{
			let file = input_field.find('input[type=file]')[0].files[0];
			if(file)
			{
				value = file.path
			}
			
			return value;
		}
	}
}
