
// ------------------- CONSTRAINT VALIDATORS -------------------

function validate_parameter(value, model)
{
	if(Array.isArray(value))
	{
		const invalid_result = value
			.map(val => validate_parameter(val, model))
			.find(res => !res.is_valid);
		
		if(invalid_result)
			return invalid_result;
		else
			return {is_valid: true};
	}
	else
	{
		const unmet_constraint = model.constraints
			.find(constraint => !constraint.validate(value));
		
		if(unmet_constraint)
		{
			return {is_valid: false, generate_message: (value, model) => unmet_constraint.get_message(value, model)};
		}
		else
		{
			return {is_valid: true};
		}
	}
}

class NumericValueConstraintValidator
{
	constructor(type, value)
	{
		this.type = type;
		this.value = value;
	}
	
	validate(input_value)
	{
		if(this.type == 'max')
            return Number(input_value) <= this.value;
        else // this.type == 'min'
            return Number(input_value) >= this.value;
	}
}

class DateConstraintValidator
{
	constructor(type, value, date_format)
	{
		this.type = type;
		this.value = value;
		this.date_format = date_format;
	}
	
	validate(input_value)
	{
		const raw_value = _to_object_value(this.value);
		const raw_input_value = _to_object_value(input_value);
		
		if(this.type == 'max')
            return raw_input_value <= raw_value;
        else // this.type == 'min'
            return raw_input_value >= raw_value;
	}
	
	_to_object_value(value)
	{
		return Date.parseExact(value, this.date_format);
	}
}

class LengthConstraintValidator
{
	constructor(type, value)
	{
		this.type = type;
		this.value = value;
	}
	
	validate(input_value)
	{
        if(this.type == 'max_length')
            return input_value.length <= this.value;
        else // this.type == 'min_length'
            return input_value.length >= this.value;
	}
}

class StringFlagConstraintValidator
{
	constructor(type)
	{
		this.type = type;
	}
	
	validate(input_value)
	{
		return (/^[a-z0-9]+$/i).test(input_value);
	}
}

class NumberFlagConstraintValidator
{
	constructor(type)
	{
		this.type = type;
	}
	
	validate(input_value)
	{
		return Number.isInteger(Number(input_value));
		}
}

class FileFlagConstraintValidator
{
	constructor(type)
	{
		this.type = type;
	}
	
	validate(input_value)
	{
		switch(this.type)
		{
			case 'exists':
				return ipcRenderer.sendSync('file_exists', input_value);
			case 'doesnt_exist':
				return !ipcRenderer.sendSync('file_exists', input_value);
			case 'is_file':
				return ipcRenderer.sendSync('is_file', input_value);
			case 'is_directory':
				return ipcRenderer.sendSync('is_directory', input_value);
		}
	}
}

class RegexConstraintValidator
{
	constructor(pattern)
	{
		this.pattern = pattern;
	}
	
	validate(input_value)
	{
		return new RegExp(this.pattern).test(input_value);
	}
}

class CodeConstraintValidator
{
	constructor(code)
	{
		this.code = code;
	}
	
	validate(input_value)
	{
		return eval('(function(value){ ' + this.code + ' })(input_value)');
	}
}

class CommandCodeConstraintValidator
{
	constructor(code)
	{
		this.code = code;
	}
	
	validate(input_args, input_sub_command)
	{
		return eval('(function(args, sub_command){ ' + this.code + ' })(input_args, input_sub_command)');
	}
}

// ------------------- VALIDATION ERROR MESSAGES -------------------

function set_error_message(message, parameter_gui_id)
{
	const parameter_wrapper = $('[data-gui-id='+parameter_gui_id+'].parameter-wrapper');
	
	parameter_wrapper
		.find('input, select')
		.addClass('invalid');
		
	parameter_wrapper
		.find('label')
		.last()
		.attr('data-error', message);
}

function clear_error_message(parameter_gui_id)
{
	const parameter_wrapper = $('[data-gui-id='+parameter_gui_id+'].parameter-wrapper');
	
	parameter_wrapper
		.find('input, select')
		.removeClass('invalid');
	
	parameter_wrapper
		.find('label')
		.removeAttr('data-error');
}
