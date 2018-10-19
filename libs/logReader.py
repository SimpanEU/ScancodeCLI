import os
import re
import time

def read_fde_dlog(keyword, minutes):
    lastLogTime = None
    phraseLog = []

    if isinstance(minutes, str):
        minutes = int(minutes) * 60
    elif isinstance(minutes, int):
        minutes = minutes * 60

    for line in reversed(list(
            open(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\dlog1.txt"))):
        lastLogTime = re.split(r'\t', line)
        lastLogTime = time.mktime(time.strptime(lastLogTime[0][:15], "%Y%m%d %H%M%S"))
        break

    for line in reversed(list(
            open(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\dlog1.txt"))):
        if keyword in line:
            phraseTime = re.split(r'\t', line)
            phraseTime = time.mktime(time.strptime(phraseTime[0][:15], "%Y%m%d %H%M%S"))
            if (lastLogTime - phraseTime) < minutes:
                phraseLog.append(line)

    for log in phraseLog:
        print(log, end="")

def sso_chain_logon(arg1):
    ssoTime = None
    onecheckTime = None
    ssoFound = False
    onecheckFound = False

    if isinstance(arg1, str):
        if "TRUE" in arg1 or "True" in arg1 or "true" in arg1:
            arg1 = True
        elif "FALSE" in arg1 or "False" in arg1 or "false" in arg1:
            arg1 = False

    for line in reversed(list(open(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\dlog1.txt"))):
        ssoLog = 'SSO data initialized SUCCESSFULLY.'
        onecheckLog = 'OneCheck repository unlocked successfully.'

        if ssoLog in line and not ssoFound:
            print(line, end="")
            ssoTime = re.split(r'\t', line)
            ssoFound = True

        if onecheckLog in line and not onecheckFound:
            print(line, end="")
            onecheckTime = re.split(r'\t', line)
            onecheckFound = True

    if ssoFound == True and onecheckFound == True:
        onecheckEpoch = time.mktime(time.strptime(onecheckTime[0][:15], "%Y%m%d %H%M%S"))
        ssoEpoch = time.mktime(time.strptime(ssoTime[0][:15], "%Y%m%d %H%M%S"))

    if arg1 is True:
        if ssoFound == True and onecheckFound == True:
            assert (onecheckEpoch-ssoEpoch) < 2 and (onecheckEpoch-ssoEpoch) >= 0, 'No SSO chain for last login.'
    elif arg1 is False:
        if ssoFound == True and onecheckFound == True:
            assert (onecheckEpoch-ssoEpoch) > 2 or (onecheckEpoch-ssoEpoch) < 0, 'SSO chain for last login.'
    else:
        assert False, 'Invalid input(true/false)'

def preboot_bypass_logon(arg1):

    wilLog = False
    systemLog = None

    systemLogFound = False
    wilLogFound = False

    systemEpoch = None
    wilEpoch = None

    if isinstance(arg1, str):
        if "TRUE" in arg1 or "True" in arg1 or "true" in arg1:
            arg1 = True
        elif "FALSE" in arg1 or "False" in arg1 or "false" in arg1:
            arg1 = False

    for line in reversed(list(open(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Logs\\epslog.43.1.log"))):

        wilLogLine = 'fde_account=(Windows Integrated Logon)'
        systemLogLine = 'System event PC was started.'

        if wilLogLine in line and not wilLogFound:
            wilLog = re.split(r'\t', line)
            wilLogFound = True
            wilEpoch = time.mktime(time.strptime(wilLog[0][1:20], "%Y-%m-%d %H:%M:%S"))

        if systemLogLine in line and not systemLogFound:
            systemLog = re.split(r'\t', line)
            systemLogFound = True
            systemEpoch = time.mktime(time.strptime(systemLog[0][1:20], "%Y-%m-%d %H:%M:%S"))

    if wilLog is False:
        wilLog = 'No entries for WIL found.'

    if arg1 is True:
        if wilLog is 'No entries for WIL found.':
            print(wilLog)
            assert False
        else:
            assert (wilEpoch-systemEpoch) <2, 'No preboot bypass entry found for last login.'
    elif arg1 is False:
        if wilLog is 'No entries for WIL found.':
            print(wilLog)
        else:
            assert (wilEpoch-systemEpoch) >2
    else:
        assert False, 'Invalid input(true/false)'

def main():
    read_fde_dlog('FDE_srv.exe', 10)
if __name__ == "__main__":
    main()