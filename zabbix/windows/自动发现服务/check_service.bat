@echo off
echo {
echo         "data":[
for /F "skip=1 eol=Ãü tokens=*" %%i IN ('net start') DO echo                 {"{#SERVICE_NAME}":"%%i"},
echo                 {"{#SERVICE_NAME}":"Zabbix Agent"}
echo         ]
echo }
pause