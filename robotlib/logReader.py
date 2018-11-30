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


def read_fde_dlog_crashes(minutes=False):
    if isinstance(minutes, str):
        minutes = int(minutes) * 60
    elif isinstance(minutes, int) and minutes > 0:
        minutes = minutes * 60
    else:
        minutes = None

    lastLogTime = None
    keyword = "An unexpected problem has occurred"

    for line in reversed(list(
            open(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\dlog1.txt"))):
        lastLogTime = re.split(r'\t', line)
        lastLogTime = time.mktime(time.strptime(lastLogTime[0][:15], "%Y%m%d %H%M%S"))
        break

    dlog = list(
        open(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\dlog1.txt"))

    for index, line in enumerate(dlog):
        if keyword in line:
            crashTime = re.split(r'\t', line)
            crashTime = time.mktime(time.strptime(crashTime[0][:15], "%Y%m%d %H%M%S"))

            if minutes is not None:
                if (lastLogTime - crashTime) < minutes:
                    for a in range(index, index + 5):
                        print(dlog[a], end="")
            else:
                for a in range(index, index + 5):
                    print(dlog[a], end="")


def sso_chain_logon(arg1):
    ssoTime = None
    onecheckTime = None
    autologonTime = None
    ssoFound = False
    onecheckFound = False
    autologonFound = False

    if isinstance(arg1, str):
        if "TRUE" in arg1 or "True" in arg1 or "true" in arg1:
            arg1 = True
        elif "FALSE" in arg1 or "False" in arg1 or "false" in arg1:
            arg1 = False

    for line in reversed(list(
            open(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\dlog1.txt"))):
        ssoLog = 'SSO data initialized SUCCESSFULLY.'
        onecheckLog = 'OneCheck repository unlocked successfully.'
        autologonLog = 'Credential type: autologon'

        if ssoLog in line and not ssoFound:
            print(line, end="")
            ssoTime = re.split(r'\t', line)
            ssoFound = True

        if onecheckLog in line and not onecheckFound:
            print(line, end="")
            onecheckTime = re.split(r'\t', line)
            onecheckFound = True

        if autologonLog in line and not autologonFound:
            print(line, end="")
            autologonTime = re.split(r'\t', line)
            autologonFound = True

    if ssoFound == True and onecheckFound == True:
        onecheckEpoch = time.mktime(time.strptime(onecheckTime[0][:15], "%Y%m%d %H%M%S"))
        ssoEpoch = time.mktime(time.strptime(ssoTime[0][:15], "%Y%m%d %H%M%S"))

    if autologonFound:
        autologonEpoch = time.mktime(time.strptime(autologonTime[0][:15], "%Y%m%d %H%M%S"))

    if arg1 is True:
        if ssoFound == True and onecheckFound == True and autologonFound == True:
            assert (onecheckEpoch - ssoEpoch) < 2 and (onecheckEpoch - ssoEpoch) >= 0 and (
                    autologonEpoch - ssoEpoch) < 2 and (
                           autologonEpoch - ssoEpoch) >= 0, 'No SSO chain found for last login.'
        else:
            assert False, 'Missing "Credential type: autologon" log in dlog1'

    elif arg1 is False and autologonFound is True:
        assert (autologonEpoch - ssoEpoch) > 2 or (autologonEpoch - ssoEpoch) < 0, 'SSO chain found last login.'

    elif arg1 is False and autologonFound is False:
        autologonEpoch = 0
        if ssoFound == True and onecheckFound == True:
            assert (autologonEpoch - ssoEpoch) < 0, 'SSO chain found last login.'

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

    for line in reversed(
            list(open(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Logs\\epslog.43.1.log"))):

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
            assert (wilEpoch - systemEpoch) < 2, 'No preboot bypass entry found for last login.'
    elif arg1 is False:
        if wilLog is 'No entries for WIL found.':
            print(wilLog)
        else:
            assert (wilEpoch - systemEpoch) > 2
    else:
        assert False, 'Invalid input(true/false)'


def main():
    # read_fde_dlog_crashes()
    sso_chain_logon(True)


if __name__ == "__main__":
    main()
