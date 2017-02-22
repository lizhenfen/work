@echo off
set REPOS=%1
set TXN=%2

set LOGPATH=C:\Repositories\vats-dubbo-project\hooks\pre.log
set /p MSG=< %LOGPATH%
if not defined MSG goto EXIT
if /i %MSG% == deploy goto VATS_API_USER

goto EXIT

:EXIT
    exit 0
:VATS_API_USER
	start http://192.168.15.36:8080/jenkins/job/vats-api-user/build?token=thisisvats-api-user
	goto EXIT

