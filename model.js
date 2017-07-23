
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
	constructor({type, id, multiplicity=1, count=1, vars, empty_str_allowed=false, prefix='', separator=' ', bool_values})
	{
		this.type = type;
		this.id = id;
		this.multiplicity = multiplicity;
		this.count = count;
		this.vars = vars;
		this.empty_str_allowed = empty_str_allowed;
		this.prefix = prefix;
		this.separator = separator;
		this.bool_values = bool_values;
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
		return [...this.matched, ...this.required, ...this.possibly_required, ...this.optional, ...this.disabled, ...this.sub_command];
	}
}

function param_ids(params)
{
	return params.map(item => item.id).filter(id => id != undefined);
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
		if(multiplicity != 1)
		{
			return value.map(collection_item => _generate_param_instance_str(collection_item))
				.filter(item => item != null)
				.reduce((a,b) => a+' '+b);
		}
		else
		{
			return _generate_param_instance_str(value);
		}
	}
	
	_generate_param_instance_str(value)
	{
		let str_val;
		if(this.model.count != 1)
		{
			str_val = value.map(input_value => _generate_single_input_str(input_value))
				.reduce((a,b) => a+this.model.separator+b);
		}
		else
		{
			str_val = _generate_single_input_str(value);
		}
		
		if(this.model.type == 'Bool' && str_val == null)
		{
			return '';
		}
		
		return this.model.prefix + str_val;
	}
	
	_generate_single_input_str(value)
	{
		switch(this.model.type)
		{
			case 'File':
			case 'Choice':
			case 'Str':
			{
				return '"'+value.replace(/"/g, '\\"')+'"';
			}
			case 'Num':
			case 'Date':
			{
				return value;
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
		
		let sub_group_results = [];
		for(let element of this.elements)
		{
			sub_group_results.push(element.match(param_values));
		}
		
		let impossible_groups_idxs = [];
		let possible_groups_idxs = [...sub_group_results.keys()];
		
		// - ako postoji u matched neki koji uopste ne postoji u nekoj od drugih ta druga je impossible, 
		sub_group_results.filter((el, idx) => !impossible_groups_idxs.includes(idx)).forEach((sub_group_result, group_idx) => 
		{
			for(let param_id of param_ids(sub_group_result.matched))
			{
				sub_group_results.filter((el, idx) => !impossible_groups_idxs.includes(idx) && idx != group_idx).forEach((other_sub_group_result, other_group_idx) => 
				{
					if(!other_sub_group_result.all.includes(param_id))
					{
						possible_groups_idxs.splice(array.indexOf(other_group_idx), 1); // romove from possible_groups_idxs
						impossible_groups_idxs.push(other_group_idx); // add to impossible_groups_idxs
					}
				});
			}
		});
		
		// svi iz impossible grupa (iskljucujuci matched) koji nisu u possible grupama idu u disabled
		for(let impossible_idx of impossible_groups_idxs)
		{
			let impossible_group = sub_group_results[impossible_idx];
			
			for(let param_id of param_ids(impossible_group.all))
			{
				let found = false;
				for(let possible_idx of possible_groups_idxs)
				{
					let possible_group = sub_group_results[possible_groups_idxs];
					if(possible_group.all.includes(param_id))
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
		
		let group = sub_group_results[possible_groups_idxs[0]];
		
		if(possible_groups_idxs.length == 1)
		{
			group_result.required.push(...group.required);
			//group_result.possibly_required.push(...group.possibly_required);
		}
		else
		{
			for(let possible_idx of possible_groups_idxs)
			{
				let possible_group = sub_group_results[possible_idx];
				group_result.possibly_required.push(...possible_group.required);
			}
			
			// oni koji su svuda required idu u required, 
			// ostali required idu u possibly_required
		}
		
		group_result.possibly_required.push(...group.possibly_required);
		
		// - ostali idu u same sebe
		group_result.optional.push(...group.optional);
		group_result.matched.push(...group.matched);
		group_result.disabled.push(...group.disabled);
		
		 // - ako je ostala samo jedna possible grupa njeni required idu u required, ako ih ima vise oni koji su svuda required idu u required, 
		 // ostali required idu u possibly_required
		
		 
		 // na kraju [...new Set([1,2,3,4,4])] da nema duplikata
		 
		 
		 // Problem: ako je definisan default, inicijalno ce biti popunjeno, inicijalno mogu biti u konfliktu, moguce resenje sa exclusive section, nije ocigledno za korisnika
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
		for(let element of this.elements)
		{
			let result = element.match(param_values);
			
			// optional, required i possibly_required idu u optional
			group_result.optional.push(...result.optional);
			group_result.optional.push(...result.required);
			group_result.optional.push(...result.possibly_required);
			
			// ostali idu u same sebe
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
