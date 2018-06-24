
// ----------------- GUI STRUCTURE MODEL -----------------

class GuiStructure
{
	constructor(elements)
	{
		this.elements = elements;
	}
}

class GuiTabs extends GuiStructure
{}

class GuiTab extends GuiStructure
{}

class GuiSectionGroup extends GuiStructure
{
	constructor(exclusive, elements)
	{
		super(elements);
		this.exclusive = exclusive;
	}
}

class GuiSection extends GuiStructure
{
	constructor(gui_id, elements)
	{
		super(elements);
		this.gui_id = gui_id;
	}
}

class GuiGrid extends GuiStructure
{}

class GuiGridRow extends GuiStructure
{}

class EmptyCell
{}

class CellSpan
{}

class GuiParameter
{
	constructor(gui_id, model)
	{
		this.gui_id = gui_id;
		this.model = model;
	}
}

// ----------------- PARAMETER MODEL -----------------

class ParameterModel
{
	constructor({type, id, multiplicity=1, count=1, vars, constraints=[], empty_str_allowed=false, prefix='', prefix_separated=false, separator=' ', count_char, bool_values, date_format})
	{
		this.type = type;
		this.id = id;
		this.multiplicity = multiplicity;
		this.count = count;
		this.vars = vars;
		this.empty_str_allowed = empty_str_allowed;
		this.prefix = prefix;
		this.prefix_separated = prefix_separated;
		this.separator = separator;
		this.count_char = count_char;
		this.bool_values = bool_values;
		this.date_format = date_format;
		this.constraints = constraints;
	}
}

// ----------------- COMMAND MODEL -----------------

class CommandModel
{
	constructor(cli_command, usage_structure, gui_structure)
	{
		this.cli_command = cli_command;
		this.current_cli_text = cli_command;
		this.usage_structure = usage_structure;
		this.gui_structure = gui_structure;
	}
}

// ----------------- USAGE MODEL -----------------

class ParametersContext
{
	constructor({matched=[], required=[], possibly_required=[], optional=[], disabled=[], sub_command=false}={matched:[], required:[], possibly_required:[], optional:[], disabled:[], sub_command:false})
	{
		this.matched = matched; // already filled by the user
		this.required = required; // are required to match the current usage pattern
		this.possibly_required = possibly_required; // will be required if parameters from the same group are filled
		this.optional = optional; // can be filled, but aren't necessary to match the current usage pattern 
		this.disabled = disabled; // belong to an element of a usage 'OrGroup' that can't be matched with the current arguments
		this.sub_command = sub_command;
	}

	get all()
	{
		return [...this.matched, ...this.required, ...this.possibly_required, ...this.optional, ...this.disabled];
	}
}

class ParameterUsage
{
	constructor(model)
	{
		this.model = model;
	}
	
	match(param_values)
	{
		if([...param_values.keys()].includes(this.model.id))
		{
			return new ParametersContext({matched:[this]});
		}
		else
		{
			return new ParametersContext({required:[this]});
		}
	}
	
	generate_str(value)
	{
		const param_list = this.generate_list(value);
		
		if(param_list.length)
		{
			return param_list
				.map(item => quote_if_neccessary(item))
				.reduce((str_val, item) => str_val + ' ' + item);
		}
		else
		{
			return '';
		}
	}
	
	_generate_single_input_value(value)
	{
		switch(this.model.type)
		{
			case 'File':
			case 'Choice':
			case 'Str':
			{
				return value;
			}
			case 'Date':
			{
				return value;
			}
			case 'Num':
			{
				return this.model.count_char ? Array(Number(value) + 1).join(this.model.count_char) : value;
			}
			case 'Bool':
			{
				if(value && this.model.bool_values.positive)
				{
					return this.model.bool_values.positive;
				}
				else if(!value && this.model.bool_values.negative)
				{
					return this.model.bool_values.negative;
				}
				else
				{
					return null;
				}
			}
		}
	}
	
	generate_list(value)
	{
		if(this.model.multiplicity != 1)
		{
			return value
				.map(collection_item => this._generate_param_instance_list(collection_item))
				.filter(item => item != [])
				.reduce((previous_items, item) => [...previous_items, ...item]);
		}
		else
		{
			return this._generate_param_instance_list(value);
		}
	}
	
	_generate_param_instance_list(value)
	{
		if(this.model.count != 1)
		{
			var instance_values = value
				.map(input_value => this._generate_single_input_value(input_value));
				
			if (!this._is_separator_whitespace())
			{
				const joined_values = instance_values
					.reduce((previous_items, item) => previous_items + this.model.separator + item);
					
				instance_values = [joined_values];
			}
		}
		else
		{
			var instance_values = [this._generate_single_input_value(value)];
		}
		
		instance_values = instance_values
			.filter(val => val != null);
		
		if(this.model.type == 'Bool')
		{
			return instance_values;
		}
		else
		{
			if(this.model.prefix_separated)
			{
				// prefix and values as separated elements
				return [this.model.prefix, ...instance_values];
			}
			else
			{
				// append prefix to the first value
				instance_values[0] = this.model.prefix + instance_values[0];
				return instance_values;
			}
		}
	}
	
	_is_separator_whitespace()
	{
		return /\s+/g.test(this.model.separator);
	}
	
	_is_prefix_separated()
	{
		return /.*\s$/g.test(this.model.prefix);
	}
}

class ParameterGroup
{
	constructor(elements)
	{
		this.elements = elements;
	}
	
	match(param_values)
	{
		let group_result = new ParametersContext();
		
		for(let element of this.elements)
		{
			let result = element.match(param_values);
			
			// merge
			group_result.optional.push(...result.optional);
			group_result.required.push(...result.required);
			group_result.possibly_required.push(...result.possibly_required);
			group_result.matched.push(...result.matched);
			group_result.disabled.push(...result.disabled);
			if(result.sub_command) group_result.sub_command = true;
		}
		
		return group_result;
	}
}

class OrGroup
{
	constructor(elements)
	{
		this.elements = elements;
	}
	
	match(param_values)
	{
		let group_result = new ParametersContext();
		
		let sub_group_results = this.elements
			.map(element => element.match(param_values));
		
		let impossible_groups_idxs = [];
		let possible_groups_idxs = [...sub_group_results.keys()];

		// if a param exists in matched and doesn't exist at all in another group, that other group is impossible
		sub_group_results
			.forEach((sub_group_result, group_idx) => 
			{
				for(let matched_param_id of param_ids(sub_group_result.matched))
				{
					sub_group_results
						.forEach((other_sub_group_result, other_group_idx) => 
						{
							// if other group is impossible or it is this group
							if (impossible_groups_idxs.includes(other_group_idx) || other_group_idx == group_idx)
								return;
							
							if(!param_ids(other_sub_group_result.all).includes(matched_param_id))
							{
								possible_groups_idxs.splice(possible_groups_idxs.indexOf(other_group_idx), 1); // remove from possible_groups_idxs
								impossible_groups_idxs.push(other_group_idx); // add to impossible_groups_idxs
							}
						});
				}
			});

		// all from the impossible groups (excluding matched) that aren't in possible groups are disabled
		for(let impossible_idx of impossible_groups_idxs)
		{
			let impossible_group = sub_group_results[impossible_idx];
			
			for(let param_id of param_ids(impossible_group.all))
			{
				let found = false;
				
				for(let possible_idx of possible_groups_idxs)
				{
					let possible_group = sub_group_results[possible_idx];
					
					if(param_ids(possible_group.all).includes(param_id))
					{
						found = true;
						break;
					}
				}
				
				if(!found)
				{
					group_result.disabled.push(param_id);
				}
			}
		}

		// if there is only one possible group left, it's required params are required
		if(possible_groups_idxs.length == 1)
		{
			const only_possible_group = sub_group_results[possible_groups_idxs[0]];
			
			group_result.required.push(...only_possible_group.required);
		}
		else // if there are more possible groups, those that are required in all of them are required, the rest are possibly_required
		{
			for(let possible_group_idx of possible_groups_idxs)
			{
				const possible_group = sub_group_results[possible_group_idx];
				
				group_result.possibly_required.push(...possible_group.required);
			}
		}
		
		// other params stay in their categories
		for(let possible_group_idx of possible_groups_idxs)
		{
			const possible_group = sub_group_results[possible_group_idx];
			
			group_result.possibly_required.push(...possible_group.possibly_required);
			group_result.optional.push(...possible_group.optional);
			group_result.matched.push(...possible_group.matched);
			group_result.disabled.push(...possible_group.disabled);
			if(possible_group.sub_command) group_result.sub_command = true;
		}
		
		return group_result;
	}
}

class OptionalElement
{
	constructor(elements)
	{
		this.elements = elements;
	}
	
	match(param_values)
	{
		let group_result = new ParametersContext();
		
		const sub_group_results = this.elements
			.map(element => element.match(param_values));
		const has_matched = sub_group_results
			.find(sub_group_result => sub_group_result.matched.length);
		
		for(let result of sub_group_results)
		{
			if(has_matched)
			{
				group_result.required.push(...result.required);
				group_result.possibly_required.push(...result.possibly_required);
			}
			else
			{
				group_result.optional.push(...result.required);
				group_result.optional.push(...result.possibly_required);
			}
			
			group_result.optional.push(...result.optional);
			group_result.matched.push(...result.matched);
			group_result.disabled.push(...result.disabled);
			if(result.sub_command) group_result.sub_command = true;
		}
		
		return group_result;
	}
}

class ParameterSeparator
{
	constructor(value)
	{
		this.value = value;
	}
	
	match()
	{
		return new ParametersContext({matched:[this]});
	}
	
	generate_str()
	{
		return this.value;
	}
	
	generate_list()
	{
		return [this.value];
	}
}

class SubCommand
{
	match()
	{
		return new ParametersContext({sub_command:true});
	}
}

class CodeBlock
{
	constructor(invoke)
	{
		this.invoke = invoke;
	}
}

// ----------------- HELPERS -----------------

function param_ids(params)
{
	return params
		.filter(param => param.model != undefined)
		.map(item => item.model.id)
		.filter(id => id != undefined);
}

function quote_if_neccessary(value)
{
	return should_be_quoted(value) ? surround_with_quotes(value) : value;
}

function surround_with_quotes(value)
{
	return '"'+value.replace(/"/g, '\\"')+'"';
}

function should_be_quoted(value)
{
	// should_not_be_quoted if it has no white space or if it is already quoted
	const should_not_be_quoted = /^([^\s]+|".*")$/g.test(value);
	
	return !should_not_be_quoted;
}

// ----------------- CONSTRAINT MODEL -----------------

class Constraint
{
	constructor(validator, message)
	{
		this._validator = validator;
		this._message = message;
	}
	
	validate(value)
	{
		return this._validator.validate(value);
	}
	
	get_message(value, model)
	{
		// assign names to values if defined
		if(model.vars)
		{
			if(model.multiplicity != 1)
			{
				value = value
					.map(val => this._convert_to_vars(val, model.vars));
			}
			else
			{
				value = this._convert_to_vars(value, model.vars);
			}
		}
		
		return this._message.replace(/{value(?:\.\w+|\[\w+\])*}/g, expression => eval(expression));
	}
	
	_convert_to_vars(values, variable_names)
	{
		return values
			.reduce((previous, val, idx) => 
			{
				previous[variable_names[idx]] = val;
				return previous;
			}, {});
	}
}
