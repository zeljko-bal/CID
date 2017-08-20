@ECHO OFF
FOR /F "usebackq delims==" %%G IN (`D:\docs\FAX\master\electron\electron.exe D:\docs\FAX\master\material_html_template\generated-electron-quick-start\`) DO ECHO %%G && call %%G