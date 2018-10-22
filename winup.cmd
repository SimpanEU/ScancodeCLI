@echo off
rmdir /S /Q %TEMP%\winupiso
mkdir %TEMP%\winupiso
net use * /delete /YES
net use Y: \\192.168.0.1:8080\
set destination="%TEMP%\winupiso\"
set source="Y:/win10/"
xcopy /s /c /d /e /h /i /r /y %source% %destination%
PS > Rename-Item "%TEMP%\winupiso\17134.1.180410-1804.rs4_release_CLIENTENTERPRISE_OEM_x64FRE_en-us.iso" "%TEMP%\winupiso\win10.iso"

cd %TEMP%\winupiso\
7z.exe x win10.iso

copy "%systemdrive%\Users\Default\AppData\Local\Microsoft\Windows\WSUS\SetupConfig.ini" SetupConfig.ini

echo ShowOobe=None >> SetupConfig.ini
echo Telemetry=Disable >> SetupConfig.ini
echo Auto=Upgrade >> SetupConfig.ini

rem it's important to have done a runas in interactive mode so the password is stored when running it from robotframework
rem we could implement some sort of "interceptor" for whatever pops up in stdout, and send passwords and such via the iostreams in java

runas /user:administrator /savecred "%TEMP%\winupiso\Setup.exe /ConfigFile "%TEMP%\winupiso\SetupConfig.ini"