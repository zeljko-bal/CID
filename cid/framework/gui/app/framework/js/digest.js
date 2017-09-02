
// ------------------- DIGEST -------------------

function digest()
{
	const command_results = get_command_results();
	
	for(command_id in command_results)
	{
		const command_result = command_results[command_id];
		
		// disabled
		$('.parameter-wrapper')
			.children('.data-input-wrapper, .none-switch-wrapper')
			.removeClass('force-disabled');
		
		for(const param_id of command_result.context.disabled)
		{
			$("[data-param-id='" + param_id + "']")
				.children('.data-input-wrapper, .none-switch-wrapper')
				.addClass('force-disabled');
		}
		
		// required
		$('.parameter-wrapper')
			.removeClass('required-param');
		
		for(const param of command_result.context.required)
		{
			$("[data-param-id='" + param.model.id + "']")
				.addClass('required-param');
		}
	}
	
	const cli_string = get_cli_string(command_results);
	$('#cli-text').text(cli_string);
	
	const current_command_id = current_commands[current_commands.length-1];
	const current_command_result = command_results[current_command_id];
	
	const command_is_complete = !current_command_result.context.required.length && !current_command_result.context.possibly_required.length;
	const subcommand_allowed = current_command_result.context.sub_command;
	
	$('#execute-btn').prop('disabled', !command_is_complete);
	$('.sub-command-button').prop('disabled', !command_is_complete || !subcommand_allowed);
}
