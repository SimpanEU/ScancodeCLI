from pywinauto import Application
from subprocess import PIPE
import subprocess
import zipfile
import os
import psutil
import time

def start_notepad():
    #subprocess.Popen('notepad.exe')
    notepad = Application().start("Notepad.exe")

    for x in range (1, 11):
        notepad.Notepad.Edit.type_keys("FDE TEST" + str(x) + "{ENTER}")

    time.sleep(0.5)

    proc = []

    for p in psutil.process_iter():
        proc.append(str(p))
    for p in proc:
        if "notepad" in p:
            proc = p
    print(proc)

def verify_notepad_running():
    if "notepad.exe" in (p.name() for p in psutil.process_iter()):
        print('notepad.exe is running.')
    else:
        assert False, 'notepad.exe is not running'

    for proc in psutil.process_iter():
        if proc.name() == "notepad.exe":
            print('Killing notepad.exe')
            proc.kill()

def verify_cpe_agent_running():
    if "cpda.exe" in (p.name() for p in psutil.process_iter()):
        print('cpda.exe is running')
    else:
        assert False, 'cpda.exe is not running'

def change_os_user_password(user, password):
    cmd = 'net user '+user+' '+password
    p = subprocess.Popen(cmd, shell=True, stdin=PIPE)
    p.communicate()

def start_cpinfo():
    detailLevel = 1
    dL = switch_detail_level(detailLevel)

    # Currently runs CPInfo with -q|-quiet parameter, uses general detail level.
    # TODO: Communicate with CPInfo.exe through PIPE to send input sequence once launched.
    # TODO: Sequence 'C', '1', '3', 'ENTER' - where '3' is corresponding to detail level 'Extended'.

    cpInfoPath = os.environ["ProgramFiles(x86)"] + "\\CheckPoint\\Endpoint Security\\Endpoint Common\\cpinfo\\cpinfo.exe"
    p = subprocess.Popen([cpInfoPath, '-q'], shell=True, stdin=PIPE)
    p.communicate()

def switch_detail_level(argument):
    # Dictionary for returning input parameters to determine detail level for CPInfo.

    return {
        'Extended': 3,
         3: 3,
        'General': 2,
        '2': 2,
         2: 2,
        'Basic': 1,
        '1': 1,
         1: 1,
    }.get(argument, 3)

def verify_cpinfo_files():
    bootEnvironment = None

    for line in list(open(os.environ['WINDIR'] + "\\Panther\\setupact.log", encoding="utf8")):
        if 'boot environment: BIOS' in line:
            print(line)
            bootEnvironment = 'BIOS'
        elif 'boot environment: UEFI' in line:
            print(line)
            bootEnvironment = 'UEFI'

    cpinfoPath = os.environ["USERPROFILE"] + "\\CPInfo\\"

    # Sort all folders in date order and save name for the newest one.
    os.chdir(cpinfoPath)
    cpinforZip = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)[-1]

    # Saves all files inside the .zip to a list.
    files = str(zipfile.ZipFile(cpinfoPath+cpinforZip+'\\'+cpinforZip+'.zip').namelist())

    if bootEnvironment == 'UEFI':
        assert 'preboot.cab' in files
        assert 'dlog1.txt' in files
        assert 'FDE_dlog.txt' in files
        assert 'dlogs' in files
        print(bootEnvironment, 'preboot.cab, dlog1.txt, FDE_dlog.txt and dlogs dir found in', cpinforZip + '.zip')

    elif bootEnvironment == 'BIOS':
        assert 'preboot.cab' in files
        assert 'dlog1.txt' in files
        assert 'FDE_dlog.txt' in files
        assert 'dlogs' in files
        print(bootEnvironment, 'preboot.cab, dlog1.txt, FDE_dlog.txt and dlogs dir found in', cpinforZip + '.zip')

    else:
        print(bootEnvironment, 'preboot.cab, dlog1.txt, FDE_dlog.txt and dlogs dir COULD NOT BE FOUND in', cpinforZip + '.zip')
        assert False

def read_release_build():
    name = subprocess.Popen('systeminfo | findstr /B /C:"OS Name', shell=True, stdout=PIPE).communicate()
    ver = subprocess.Popen('systeminfo | findstr /B /C:"OS Version', shell=True, stdout=PIPE).communicate()
    print(name)
    print(ver)

def check_if_win_activated():
    subprocess.Popen('cscript c:\windows\system32\slmgr.vbs /dli > c:\WinStatus.txt', shell=True, stdout=PIPE).communicate()

    with open('C:\\WinStatus.txt', 'r') as myfile:
        print(myfile.read())
        myfile.close()

    for line in open('C:\\WinStatus.txt', 'r'):
        if "Status" in line:
            print(line)

def check_if_win_activated_wmic(arg1):
    if isinstance(arg1, str):
        if "TRUE" in arg1 or "True" in arg1 or "true" in arg1:
            arg1 = True
        elif "FALSE" in arg1 or "False" in arg1 or "false" in arg1:
            arg1 = False
    open('C:\\wa.ps1', 'wb').write(b'Get-CimInstance -ClassName SoftwareLicensingProduct | Where-Object PartialProductKey | Select-Object Name, ApplicationId, LicenseStatus | out-file C:\\isActivated.txt -Encoding UTF8')
    p = subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Unrestricted', 'C:\\wa.ps1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()

    with open('C:\\isActivated.txt', "r") as myfile:
        key = myfile.read()
        key = key[-4:]
    key = switch_license(key)

    if arg1:
        if key is 'Licensed':
            print('Key is activated, current status: '+key)
            assert True
        else:
            assert False
    if not arg1:
        if key is 'Licensed':
            print('Key is activated, current status: '+key)
            assert False
        else:
            print('Key is in '+key+' status.')

def switch_license(arg1):
    if isinstance(arg1, str):
        arg1 = int(arg1)
    return {
        0: 'Unlicensed',
        1: 'Licensed',
        2: 'OOBGrace',
        3: 'OOTGrace',
        4: 'NonGenuineGrace',
        5: 'Notification',
        6: 'ExtentedGrace',
    }.get(arg1, "Undetected")

def schedule_wakeup_task(user, password):
    open('C:\\WakeUp.bat', 'wb').write(b'echo hello')
    cmd = "schtasks.exe /CREATE /TN WakeUpTask /XML c:\WakeUpTask.xml /F /RU "+user+" /RP "+password
    subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE).communicate()

def tpm_status():
    print(os.system("powershell get-tpm"))

def main():
    #check_if_win_activated()
    #start_notepad()
    tpm_status()

if __name__ == "__main__":
    main()


    if "TOKIGISYLT" + "SOTS+8" == "FAIL":
        __self__