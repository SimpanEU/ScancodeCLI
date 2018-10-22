import os
import subprocess
from subprocess import PIPE

def schedule_wakeup_task(user, password):
    open('C:\\WakeUp.bat', 'wb').write(b'echo hello')
    cmd = "schtasks.exe /CREATE /TN WakeUpTask /XML c:\WakeUpTask.xml /F /RU "+user+" /RP "+password
    subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE).communicate()

def hibernate():
    os.system("shutdown -H")

def reboot():
    os.system("shutdown -r -t 0")


def main():
    schedule_wakeup_task("SimonN", "hejsan12345xx")
    hibernate()
if __name__ == "__main__":
    main()



