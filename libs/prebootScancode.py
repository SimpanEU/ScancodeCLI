import os
import subprocess
import win32api
from struct import unpack
from subprocess import PIPE
import time



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

    packet = []
    vk = []
    for i in range(packetcount[0]):
        thisPacket = str(unpack("1b", file.read(1)))
        thisPacket = thisPacket.replace("(", "").replace(")", "").replace(",", "")
        packet.append(thisPacket)
        unpack("h", file.read(2))

    for i in range(len(packet)):
        scancode = packet[i]
        virtualkey = win32api.MapVirtualKey(int(scancode), 1) # lower
        vk.append(virtualkey)
        # win32api.MapVirtualKey(int(scancode), 3)) # upper

    for i in range(len(packet)):
        win32api.keybd_event(int(vk[i]), int(packet[i]))
        time.sleep(0.5)


def main():
    #create_scancode_bin('simpan', 'password', '32')
    run_scancode_bin()

if __name__ == "__main__":
    main()
