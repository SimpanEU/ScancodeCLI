from __future__ import print_function
from statistics import mean
import datetime
import os
import shutil


def read_disk_size():
    total, used, free = shutil.disk_usage("\\")
    print("Storage Unit: ")
    print("Total: %d GB" % (total // (2 ** 30)))
    print("Used: %d GB" % (used // (2 ** 30)))
    print("Free: %d GB" % (free // (2 ** 30)))


def write_new_file(gigabytes=1, nrLoops=10):
    time = []
    time2 = []
    size = switch_size(gigabytes)

    if isinstance(nrLoops, str):
        nrLoops = int(nrLoops)

    for i in range(0, int(nrLoops)):
        file = os.environ["SYSTEMDRIVE"] + '\\SpeedTest1'

        start = datetime.datetime.now()
        f = open(file, "wb")

        for b in range(0, size):
            f.write(b"\n" * 1024 ** 2)
        f.close()
        end = datetime.datetime.now()
        filesize = (os.path.getsize(file) / 1024) / 1024
        os.remove(file)
        time.append((end - start).seconds + (end - start).microseconds / 1000000)

    for i in range(0, int(nrLoops)):
        file = os.environ["SYSTEMDRIVE"] + '\\SpeedTest2'
        start = datetime.datetime.now()
        f = open(file, "wb")
        seekSize = size * 1024 * 1024
        f.seek(seekSize - 1)
        f.write(b"\n")
        f.seek(0)

        for b in range(0, size):
            f.write(b"\n" * 1024 ** 2)
        f.close()
        end = datetime.datetime.now()
        filesize2 = (os.path.getsize(file) / 1024) / 1024
        os.remove(file)
        time2.append((end - start).seconds + (end - start).microseconds / 1000000)

    filespeed1 = filesize / round(mean(time), 2)
    filespeed2 = filesize2 / round(mean(time2), 2)
    print()
    print("==============================================")
    print("Average time writing", filesize, 'MB same data:')
    print(round(mean(time), 2), "seconds")
    print(int(filespeed1), "MB/S")
    print("==============================================")
    print("(SEEK SET)\nAverage time writing", filesize2, 'MB same data:')
    print(round(mean(time2), 2), "seconds")
    print(int(filespeed2), "MB/S")
    print("==============================================")
    print("Test looped", nrLoops, "times.")


def switch_size(argument):
    return {
        '1GB': 1024,
        '2GB': 1024 * 2,
        '3GB': 1024 * 3,
        '4GB': 1024 * 4,
        '5GB': 1024 * 5,
        1: 1024,
        2: 1024 * 2,
        3: 1024 * 3,
        4: 1024 * 4,
        5: 1024 * 5,
    }.get(argument, 1024)


def main():
    # (1GB) file looping (5) times returning mean.
    write_new_file('1GB', 5)


if __name__ == "__main__":
    main()
