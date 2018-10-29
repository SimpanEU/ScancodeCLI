import threading
import os
import time
import datetime
import re

def create_dump_test():
    wd = os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\"
    os.chdir(wd)

    if not 'CrashDumps' in os.listdir(os.getcwd()):

         os.mkdir("CrashDumps")
         os.chdir("CrashDumps")

         os.mkdir('TestCrashDir01')
         os.mkdir('TestCrashDir02')
         os.mkdir('TestCrashDir03')

         open("TestCrash.dmp", "wb").write(b'test')
         open("TestCrash2.dmp", "wb").write(b'test')
         open("TestCrash3.dmp", "wb").write(b'test')

def background_scanner():
    global killme
    global dmp
    global dlogCrash

    killme = False
    dmp = []
    dlogCrash = []

    while True:
        lastLogTime = None
        keyword = "An unexpected problem has occurred"
        dlog = list(open(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\dlog1.txt"))

        if 'CrashDumps' in os.listdir(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\"):
            dumps = os.listdir(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\CrashDumps\\")
            for index, item in enumerate(dumps):
                if item not in dmp:
                    currTime = str(datetime.datetime.now())
                    print(item, 'found', currTime[:19])
                    dmp.append(item)

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
    print('Starting background scan...')
    dmp.clear()

def stop_background_scan():
    global killme
    global dlogCrash
    global dmp

    print('Stopping background scan')
    killme = True

    for line in dlogCrash:
        if '.dmp' in line:
            print('Following entries was found in dlog1.txt during testscenario:\n', line)

    print('Dumps found:\n')
    for item in dmp:
        if '.dmp' in item:
            print(item)

    for item in dmp:
        if '.dmp' in item:
            dmp.clear()
            assert False, "CrashDumps found during test suite"


def main():
    #create_dump_test()
    print(os.listdir(os.environ["ALLUSERSPROFILE"] + "\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\CrashDumps\\"))
    # start_background_scan()
    # time.sleep(10)
    # stop_background_scan()

if __name__ == "__main__":
    main()