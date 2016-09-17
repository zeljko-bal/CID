{%- if command.description -%}
{{ command.description }}

{% endif -%}
Usage:{{ command.usages|usage_lines_repr(command_str) }}
{%- if command.parameters or command.help_params %}

Parameters:
{{command|parameters_usage_help(long, command_str)}}
{%- endif %}
{%- if command.sub_commands %}

Sub Commands:
{{command|subcommands_usage_help(common_subcommand_help, parents)}}
{%- endif %}
{%- if common_subcommand_help %}

For help about a speciffic sub command type: {{command_str}} <sub_command> {{common_subcommand_help}}.
{%- endif %}
{%- if long and command.help %}

{{command.help}}
{%- endif %}