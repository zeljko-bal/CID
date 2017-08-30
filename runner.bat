@ECHO OFF
setlocal EnableDelayedExpansion
:: for all output lines from the gui app
FOR /F "usebackq delims==" %%G IN (`D:\docs\FAX\master\electron\electron.exe D:\docs\FAX\master\material_html_template\generated-electron-quick-start\`) DO (
	SET _line=%%G
	:: if the line starts with "__EXECUTE_COMMAND__:"
	IF "!_line:~0,20!"=="__EXECUTE_COMMAND__:" (
		:: echo the command and then call it
		ECHO !_line:~20!
		call !_line:~20!
	)
)