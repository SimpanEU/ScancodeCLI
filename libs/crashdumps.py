import threading
import os
import time
import datetime
import re
from robot.libraries.BuiltIn import BuiltIn

dmplog = os.environ["SYSTEMDRIVE"] + "\\FDE_robot_dmplog.txt"


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
    global killme
    global dmp
    global dlogCrash

    if not 'CrashDumps' in os.listdir(
            os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\"):
        os.mkdir(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\CrashDumps")
        if not 'archive' in os.listdir(
                os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\CrashDumps\\"):
            os.mkdir(os.environ[
                         "ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\CrashDumps\\archive\\")

    archive = os.environ[
                  "ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\CrashDumps\\archive\\"
    crashdumps = os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\CrashDumps\\"

    killme = False
    dmp = []
    dlogCrash = []
    dmp.clear()

    while True:
        lastLogTime = None
        keyword = "An unexpected problem has occurred"
        dlog = list(
            open(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\dlog1.txt"))

        if 'CrashDumps' in os.listdir(
                os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\"):
            dumps = os.listdir(
                os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\CrashDumps\\")

            for index, item in enumerate(dumps):
                if item not in dmp:
                    currTime = str(datetime.datetime.now())
                    # test_name = BuiltIn().get_variable_value("${TEST_NAME}")
                    # open(dmplog, "a").write(
                    #     str(currTime[:19] + '     Found ' + item + '      During ' + test_name + '\n'))

                    open(dmplog, "a").write(
                        str(currTime[:19] + '     Found ' + item + '      During ' + '\n'))
                    dmp.append(item)
                    print(item, 'before IF')
                    if not 'archive' in item:
                        print("if ON")
                        os.rename(crashdumps + item, archive + item)

        for line in reversed(dlog):
            lastLogTime = re.split(r'\t', line)
            lastLogTime = time.mktime(time.strptime(lastLogTime[0][:15], "%Y%m%d %H%M%S"))
            break

        for index, line in enumerate(dlog):
            if keyword in line:
                crashTime = re.split(r'\t', line)
                crashTime = time.mktime(time.strptime(crashTime[0][:15], "%Y%m%d %H%M%S"))
                if (lastLogTime - crashTime) < 30:
                    for a in range(index, index + 5):
                        if dlog[a] not in dlogCrash:
                            dlogCrash.append(dlog[a])
        if killme:
            break

        time.sleep(1)


def start_background_scan():
    b = threading.Thread(name='background_scanner', target=background_scanner)
    b.start()

    # currTime = str(datetime.datetime.now())
    # open(dmplog, "a").write(str(currTime[:19]+'     Starting background scan...\n'))


def stop_background_scan():
    global killme
    global dlogCrash
    global dmp

    # currTime = str(datetime.datetime.now())
    # open(dmplog, "a").write(str(currTime[:19]+'     Stopping background scan\n'))

    killme = True

    for line in dlogCrash:
        if '.dmp' in line:
            currTime = str(datetime.datetime.now())
            open(dmplog, "a").write(
                str(currTime[:19] + '     Following entries was found in dlog1.txt during testscenario:\n' + line))

    # currTime = str(datetime.datetime.now())
    # open(dmplog, "a").write(str(currTime[:19]+'     Dumps found:\n'))
    # for item in dmp:
    #     if '.dmp' in item:
    #         currTime = str(datetime.datetime.now())
    #         open(dmplog, "a").write(str(currTime[:19]+'     '+item+'\n'))
    # print(item)

    for item in dmp:
        if '.dmp' in item:
            assert False, "CrashDumps found during test suite"


def main():
    create_crashdump()
    start_background_scan()
    time.sleep(10)
    stop_background_scan()


if __name__ == "__main__":
    main()
