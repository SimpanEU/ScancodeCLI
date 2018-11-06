import threading
import os
import time
import datetime
import re
from robot.libraries.BuiltIn import BuiltIn


def create_crashdump():
    fdedir = os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\"
    currTime = str(datetime.datetime.now())
    currTime = currTime[:19]
    currTime = currTime.replace(' ', '').replace(':', '').replace('-', '')

    if not 'CrashDumps' in os.listdir(fdedir):
        os.mkdir(fdedir + 'CrashDumps')

    if 'CrashDumps' in os.listdir(fdedir):
        file = fdedir + 'CrashDumps\\' + currTime + '.dmp'
        open(file, "wb").write(b'testdump')


def background_scanner():
    global dmplog
    global killme
    global dmp
    global dlogCrash

    dmplog = os.environ["SYSTEMDRIVE"] + "\\FDE_robot_dmplog.txt"
    killme = False
    dlogCrash = []
    dmp = []
    dmp.clear()

    pathFde = os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\"
    pathCrash = os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\CrashDumps\\"
    pathArch = os.environ[
                   "ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\CrashDumps\\archive\\"

    if not 'CrashDumps' in os.listdir(pathFde):
        os.mkdir(pathCrash)
    if not 'archive' in os.listdir(pathCrash):
        os.mkdir(pathArch)

    for item in os.listdir(pathCrash):
        if '.dmp' in item:
            os.rename(pathCrash + item, pathArch + item)

    while True:
        lastLogTime = None
        keyword = "An unexpected problem has occurred"
        dlog = list(open(pathFde + 'dlog1.txt'))

        for item in os.listdir(pathCrash):
            if item not in dmp and 'archive' not in item:
                currTime = str(datetime.datetime.now())
                test_name = BuiltIn().get_variable_value("${TEST_NAME}")
                open(dmplog, "a").write(str(currTime[:19] + '     Found "' + item + '"      During "' + str(test_name) + '"\n'))
                dmp.append(item)
                if '.dmp' in item:
                    os.rename(pathCrash + item, pathArch + item)

        for line in reversed(dlog):
            lastLogTime = re.split(r'\t', line)
            lastLogTime = time.mktime(time.strptime(lastLogTime[0][:15], "%Y%m%d %H%M%S"))
            break

        for index, line in enumerate(dlog):
            if keyword in line:
                crashTime = re.split(r'\t', line)
                crashTime = time.mktime(time.strptime(crashTime[0][:15], "%Y%m%d %H%M%S"))

                # Read last 10 seconds from dlog1.txt, appending any line containing
                # logging about crashdumps for later printout.
                if (lastLogTime - crashTime) < 10:
                    for a in range(index, index + 5):
                        if dlog[a] not in dlogCrash:
                            dlogCrash.append(dlog[a])
        if killme:
            break

        time.sleep(1)


def start_background_scan():
    b = threading.Thread(name='background_scanner', target=background_scanner)
    b.start()

    currTime = str(datetime.datetime.now())
    open(dmplog, "a").write(str(currTime[:19] + '     Starting background scan...\n'))


def stop_background_scan():
    global killme
    global dlogCrash
    global dmp

    currTime = str(datetime.datetime.now())
    open(dmplog, "a").write(str(currTime[:19] + '     Stopping background scan...\n'))

    killme = True

    for line in dlogCrash:
        if '.dmp' in line:
            currTime = str(datetime.datetime.now())
            open(dmplog, "a").write(
                str(currTime[:19] + '     Following entries was found in dlog1.txt\n' + line))

    for item in dmp:
        if '.dmp' in item:
            assert False, "CrashDumps found during test suite"


def main():
    start_background_scan() # test_name variable can only be set running via robotframework.
    create_crashdump()
    time.sleep(10)
    stop_background_scan()


if __name__ == "__main__":
    main()
