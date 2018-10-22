@echo off
net use * /delete /YES
net use Y: \\Vboxsvr\da
set destination="C:\work\robot"
set source="Y:\robot"
xcopy /s /c /d /e /h /i /r /y %source% %destination%




set PYTHONPATH=%PYTHONPATH%;C:\work\robot\libs
cd C:\work\robot\tests
cmd /k