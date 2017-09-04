@ECHO OFF
setlocal EnableDelayedExpansion
:: for all output lines from the gui app
FOR /F "usebackq delims==" %%G IN (`electron cid_generator_gui`) DO (
	SET _line=%%G
	:: if the line starts with "__EXECUTE_COMMAND__:"
	IF "!_line:~0,20!"=="__EXECUTE_COMMAND__:" (
		:: echo the command and then call it
		ECHO !_line:~20!
		call !_line:~20!
		
		:: pause if double clicked
		IF %0 == "%~0"  pause
	)
)