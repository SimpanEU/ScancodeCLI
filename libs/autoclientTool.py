import subprocess
import os
from subprocess import PIPE


def checkpoint_security_screensaver(arg1):
    tool = os.environ["SYSTEMDRIVE"] + '\\V4_debug\\AutomationClient.exe'
    script = os.environ["SYSTEMDRIVE"] + '\\V4_debug\\SecurityScreensaver.txt'
    login = ' -i 192.168.56.2 -u admin -p Password -s '

    cmd = tool + login + '"' + script + '"'

    print(cmd)

    s = "Login\n" \
        "OnecheckAction[fde_enable_onecheck].enableCheckPointEndpointSecurityScreensaver = " + arg1 + "\n" \
                                                                                                      "Commit\n" \
                                                                                                      "update_policies_timestamps_all\n" \
                                                                                                      "Publish\n" \
                                                                                                      "Disconnect\n" \
                                                                                                      "Exit\n"

    with open(script, 'w') as f:
        f.write(s)

    subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()


def checkpoint_security_screensaver_text(arg1):
    tool = os.environ["SYSTEMDRIVE"] + '\\V4_debug\\AutomationClient.exe'
    script = os.environ["SYSTEMDRIVE"] + '\\V4_debug\\SecurityScreensaverText.txt'
    login = ' -i 192.168.56.2 -u admin -p Password -s '

    cmd = tool + login + '"' + script + '"'

    print(cmd)

    s = "Login\n" \
        'OnecheckAction[fde_enable_onecheck].screenSaverText = "' + arg1 + '"\n' \
                                                                           "commit\n" \
                                                                           "update_policies_timestamps_all\n" \
                                                                           "Publish\n" \
                                                                           "Disconnect\n" \
                                                                           "Exit\n"

    with open(script, 'w') as f:
        f.write(s)

    subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()


def main():
    checkpoint_security_screensaver("true")
    #checkpoint_security_screensaver_text("Simpan")


if __name__ == "__main__":
    main()
