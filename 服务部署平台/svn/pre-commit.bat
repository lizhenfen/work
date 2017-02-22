@echo on

set REPOS=%1
set TXN=%2
set LOGPATH=C:\Repositories\vats-dubbo-project\hooks\pre.log
set SVNLOOK="C:\Program Files (x86)\VisualSVN Server\bin\svnlook.exe"

%SVNLOOK% log -t %TXN% %REPOS% > %LOGPATH%

exit 0
