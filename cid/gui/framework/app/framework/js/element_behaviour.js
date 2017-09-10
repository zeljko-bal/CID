
// ------------------- MATERIALIZE INIT -------------------

$('.datepicker').pickadate(
{
	selectMonths: true, // Creates a dropdown to control month
	selectYears: 15, // Creates a dropdown of 15 years to control year
	closeOnSelect: true, // Close upon selecting a date,
});

$('select').material_select();

$('.modal-trigger').leanModal();

$('ul.tabs').tabs();

// ------------------- INPUT LIST TITLES -------------------

function replace_titles(list_items, param_type)
{
	list_items.each((i, list_item) =>
	{
		list_item = $(list_item);
		if(param_type == 'File')
		{
			var label = list_item.find('.file-field .btn span');
		}
		else
		{
			var label = list_item.find('.input-field label');
		}
		label.text(label.text().replace(/\d+$/, i+1));
	});
}

// ------------------- SECTIONS -------------------

$('.collapsible-header.exclusive-section').click(event =>
{
	let current_section = $(event.currentTarget);
	let section_group = current_section.parents('.collapsible').first();
	
	let sections = section_group.children('li').children('.collapsible-header');
	
	for(other_section of sections.get())
	{
		other_section = $(other_section);
		
		if(!other_section.is(current_section))
		{
			other_section.children('i.section-check-icon').text('radio_button_unchecked');
		}
	};
	
	if(current_section.hasClass('active'))
	{
		event.stopPropagation();
	}
	else
	{
		current_section.children('i.section-check-icon').text('check_circle');
	}
	
	window.setTimeout(digest, 1);
});

$('.collapsible-header.optional-section').click(event =>
{
	let current_section = $(event.currentTarget);
	if(current_section.hasClass('active'))
	{
		current_section.children('i.section-check-icon').text('radio_button_unchecked');
		current_section.children('i.section-expand-icon').text('expand_more');
	}
	else
	{
		current_section.children('i.section-check-icon').text('check_circle');
		current_section.children('i.section-expand-icon').text('expand_less');
	}
	
	window.setTimeout(digest, 1);
});

function is_section_active(section)
{
	return $('[data-gui-id='+section.gui_id+'] > .collapsible-header').hasClass('active');
}

// ------------------- COMMANDS -------------------

function toggle_command_panel(event)
{
	let button = $(event.currentTarget);
	let command_id = button.attr('data-command-id');
	
	let command_panels = $(".command-panel");
	
	for(let i=0; i<command_panels.length; i++)
	{
		command_panel = $(command_panels[i]);
		
		if(command_panel.attr('id') == command_id)
		{
			command_panel.fadeIn(200);
		}
		else
		{
			command_panel.hide();
		}
	}
	
	if(event.data == 'next')
	{
		current_commands.push(command_id);
	}
	else
	{
		while(current_commands[current_commands.length-1] != command_id)
		{
			current_commands.pop();
		}
	}
	
	window.dispatchEvent(new Event('resize'));
	
	digest();
}

function execute_sub_command(event)
{
	const button = $(event.currentTarget);
	const command_id = button.attr('data-command-id');
	const cli_command = command_models[command_id].cli_command;
	
	const cli_string = get_current_cli_string();
	
	execute_cli_string(cli_string + ' ' + cli_command);
}

$('.sub-command-link').click('next', toggle_command_panel);
$('.parent-command-link').click('prev', toggle_command_panel);
$('.sub-command-execute').click(execute_sub_command);

// display sub-command in cli panel
$('.sub-command-wrapper .btn').hover(event =>
{
	const command_id = $(event.currentTarget).attr('data-command-id');
	const cli_command = command_models[command_id].cli_command;
	$('#sub-command-cli-text').text(cli_command);
},() =>
{
	$('#sub-command-cli-text').text('');
});

$('.sub-command-wrapper .btn').click(event => 
{
	$('#sub-command-cli-text').text('');
});

// ------------------- TRISTATE CHECKBOX -------------------

// add tri-state checkbox functionality
// taken from: https://css-tricks.com/indeterminate-checkboxes/
$(".tristate-checkbox").click(function()
{
	if (this.readOnly) this.checked=this.readOnly=false;
	else if (!this.checked) this.readOnly=this.indeterminate=true;
});

function get_checkbox_state(cb) // get checkbox state: true, false or null (intermidiate)
{
	cb = cb[0]; // dereference jquery
	if(cb.indeterminate) return null;
	else return cb.checked;
}

// ------------------- NONE SWITCH -------------------

$('.none-switch input').click(event =>
{
	let none_switch = $(event.currentTarget);
	none_switch.parents('.parameter-wrapper').find('.input-field input').prop('disabled', !none_switch.prop('checked'));
});

// activate on click

function activate_on_click(event)
{
	let none_switch = event.data;
	if(!none_switch.prop('checked'))
	{
		none_switch.click();
	}
}

$('.none-switch input').each((i, none_switch) =>
{
	none_switch = $(none_switch);
	none_switch.parents('.parameter-wrapper').first().find('.input-field').click(none_switch, activate_on_click);
});

// ------------------- DESCRIPTION -------------------

$('.desc-btn').click(event =>
{
	let button = $(event.currentTarget);
	let card_id = button.attr('data-shows');
	let card = $('[id='+card_id+']');
	card.slideToggle(100);
});

$('.close-desc-button').click(event =>
{
	$(event.currentTarget).parent().slideToggle(100);
});

// ------------------- REINITIALIZE INPUTS -------------------

function reinitialize_input_list(param, input_list)
{
	let param_model = get_param_model(param);
	
	// toggle remove buttons
	toggle_remove_btn_visibility(input_list, '.remove-input-field-btn');

	// refresh titles
	if(param_model.count == '*' || (param_model.count == 1 && param_model.multiplicity == '*'))
	{
		replace_titles(input_list.children(), param_model.type);
	}
}

function reinitialize_input_item(param, new_input_li)
{
	// remove button
	new_input_li.find('.remove-input-field-btn').click(remove_input_field);
	
	// activate switch on click
	let none_switch = param.find('.none-switch input');
	if(none_switch.length)
	{
		new_input_li.find('.input-field').click(none_switch, activate_on_click);
	}
	
	// new id
	let new_id = get_new_id(new_input_li);
	new_input_li.find('.input-field').attr('data-input-id', new_id);
	
	switch(get_param_model(param).type)
	{
		case 'Str':
		case 'Num':
		case 'Date':
		{
			// new id
			new_input_li.find('.input-field input').attr('id', new_id);
			new_input_li.find('.input-field label').attr('for', new_id);
			
			// clear input value
			new_input_li.find('.input-field input').val('');
			
			// reinitialize
			Materialize.updateTextFields();
			break;
		}
		case 'File':
		{
			// new id
			new_input_li.find('input.file-path').attr('id', new_id);
			
			// clear input value
			new_input_li.find('input.file-path').val('');
			
			// reinitialize
			Materialize.updateTextFields();
			break;
		}
		case 'Choice':
		{
			var select = new_input_li.find('.input-field select');
			
			// new id
			select.attr('id', new_id);
			
			// clear old elements
			new_input_li.find('.input-field input.select-dropdown').remove();
			new_input_li.find('.input-field ul.select-dropdown.dropdown-content').remove();
			
			// reinitialize
			select.material_select();
			break;
		}
	}
	
	new_input_li.find('input, select').change(digest);
}

// ------------------- INPUT FIELD -------------------

function add_input_field(event)
{
	let btn = $(event.currentTarget);
	let param = btn.parents('.parameter-wrapper');
	let input_list = btn.parents('.input-list').first();
	let new_li = input_list.children().first().clone();
	
	// insert
	new_li.css('display', 'none');
	new_li.insertBefore(btn.parent());
	new_li.fadeIn(200);
	
	reinitialize_input_item(param, new_li);
	reinitialize_input_list(param, input_list);
	
	digest();
}

$('.add-input-field-btn').click(add_input_field);

function remove_input_field(event)
{
	let btn = $(event.currentTarget);
	let li = btn.parents('.input-field').parent();
	let input_list = li.parent();
	let param = input_list.parents('.parameter-wrapper');
	
	li.remove();
	
	toggle_remove_btn_visibility(input_list, '.remove-input-field-btn');
	
	replace_titles(input_list.children(), get_param_model(param).type);
	
	digest();
}

$('.remove-input-field-btn').click(remove_input_field);

// ------------------- INPUT COLLECTION -------------------

$('.add-input-collection-item-btn').click(event =>
{
	let btn = $(event.currentTarget);
	let param = btn.parents('.parameter-wrapper');
	let input_collection = btn.parents('.input-collection');
	let new_li = $(input_collection.children()[1]).clone();
	
	// insert
	new_li.css('display', 'none');
	new_li.appendTo(input_collection);
	new_li.fadeIn(200);
	
	let input_list = new_li.find('.input-list');
	
	// add input btn
	input_list.find('.add-input-field-btn').click(add_input_field);
	
	// remove collection item btn
	new_li.find('.remove-input-collection-item-btn').click(remove_input_collection_item);
	toggle_remove_btn_visibility(input_collection, '.remove-input-collection-item-btn');
	
	let list_items = input_list.children();
	let count_many = !!list_items.find('.add-input-field-btn').length;
	let original_items_length = list_items.length;
	if(count_many) original_items_length -= 1;
	let new_items_length = original_items_length;
	
	// remove excess input fields
	if(count_many)
	{
		for(let i=1;i<original_items_length;i++)
		{
			$(list_items[i]).remove();
		}
		
		new_items_length = 1;
	}
	
	// reinitialize remaining input fields
	for(let i=0;i<new_items_length;i++)
	{
		reinitialize_input_item(param, $(list_items[i]));
	}
	
	// reinitialize input list
	reinitialize_input_list(param, input_list);
	
	digest();
});

function remove_input_collection_item(event)
{
	let btn = $(event.currentTarget);
	
	let li = btn.parents('.collection-item');
	let input_collection = li.parents('.input-collection');
	
	li.remove();
	
	toggle_remove_btn_visibility(input_collection, '.remove-input-collection-item-btn');
	
	digest();
}

function toggle_remove_btn_visibility(btn_list, btn_class)
{
	let btn = btn_list.find(btn_class);
	
	if(btn_list.children().length > 2)
	{
		btn.css('visibility', 'visible');
	}
	else
	{
		btn.css('visibility', 'hidden'); 
	}
}

$('.remove-input-collection-item-btn').click(remove_input_collection_item);

// -------------------

// digest on all input changes
$('.parameter-wrapper')
	.find('input, select')
	.change(digest);

// ------------------- MAIN BUTTONS -------------------

$('#execute-btn').click(event =>
{
	const cli_string = get_current_cli_string();
	
	execute_cli_string(cli_string);
});

$('#close-btn').click(event =>
{
	ipcRenderer.sendSync('close');
});

function execute_cli_string(cli_string)
{
	ipcRenderer.sendSync('execute_command', {cli_string: cli_string});
}
