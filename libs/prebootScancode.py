import os
import subprocess
import win32api
import win32con
import time
from struct import unpack
from subprocess import PIPE


def create_scancode_bin(user, passwd, timeout):
    # PrebootManuscriptCLI folder
    path = 'C:\\DA\\robot\\PrebootManuscriptCLI'
    os.chdir(path)

    if os.getcwd() == path:
        cmd = 'python -m run -u ' + user + ' -p ' + passwd + ' -t ' + timeout
        print(cmd)
        subprocess.Popen(cmd, shell=True, stdin=PIPE, stderr=PIPE, stdout=PIPE).communicate()


def run_scancode_bin():
    binfile = 'C:\\manuscript.bin'
    file = open(binfile, 'rb')

    version = unpack("4b", file.read(4))
    packetcount = unpack("4b", file.read(4))

    packets = int(len(file.read()))
    file.seek(8)

    operation = []
    timeout = []
    scancode = []
    virtualkey = []

    for i in range(packetcount[0]):
        op = str(unpack("1B", file.read(1))).replace("(", "").replace(")", "").replace(",", "")
        ti = str(unpack("1H", file.read(2))).replace("(", "").replace(")", "").replace(",", "")
        sc = str(unpack("1B", file.read(1))).replace("(", "").replace(")", "").replace(",", "")
        print('Packet:', i + 1, '=', op, ti, sc, win32api.MapVirtualKey(int(sc), 1))
        operation.append(op)
        timeout.append(ti)
        scancode.append(sc)
        virtualkey.append(win32api.MapVirtualKey(int(sc), 1))

    for i in range(packetcount[0]):
        if operation[i] == '0':
            win32api.keybd_event(virtualkey[i], 0, 0, 0)
            time.sleep(int(timeout[i]) / 1000)

        elif operation[i] == '1':
            win32api.keybd_event(virtualkey[i], 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(int(timeout[i]) / 1000)


def main():
    create_scancode_bin('UsEr_1', 'PaSS123!!', '500')
    run_scancode_bin()


if __name__ == "__main__":
    main()
