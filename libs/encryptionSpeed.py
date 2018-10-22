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

def write_new_file(gigabytes, nrLoops = 1):
    time = []
    time2 = []
    size = switch_size(gigabytes)

    if isinstance(nrLoops, str):
        nrLoops = int(nrLoops)

    print()
    for i in range(0, int(nrLoops)):
        start = datetime.datetime.now()
        f = open('test', "wb")

        for b in range(0, 1024):
            f.write(b"\n" * 1024**2)
        f.close()
        end = datetime.datetime.now()
        filesize = (os.path.getsize('test')/1024)/1024
        os.remove('test')
        time.append((end - start).seconds+(end - start).microseconds/1000000)
        print(filesize,'MB      TIME:',(end - start).seconds+(end - start).microseconds/1000000)

    print()
    for i in range(0, int(nrLoops)):
        start = datetime.datetime.now()
        f = open('test2', "wb")

        f.seek(1073741824-1)
        f.write(b"\n")
        f.seek(0)

        for b in range(0, 1024):
            f.write(b"\n" * 1024**2)


        f.close()
        end = datetime.datetime.now()
        filesize2 = (os.path.getsize('test2')/1024)/1024
        os.remove('test2')
        time2.append((end - start).seconds+(end - start).microseconds/1000000)
        print(filesize2,'MB (SEEK) TIME:',(end - start).seconds+(end - start).microseconds/1000000)




    print()
    print("Average TIME:", round(mean(time),2),'S   /   ',filesize,'MB =', filesize/round(mean(time),2),'MB/S')
    print("Average TIME (SEEK):", round(mean(time2),2),'S   /   ',filesize2,'MB =', filesize2/round(mean(time2),2),'MB/S')

def switch_size(argument):
    return {
        '1GB': 1,
        '2GB': 2,
        '3GB': 3,
        1: 1,
        2: 2,
        3: 3,
    }.get(argument, 1)


def main():
    read_disk_size()
    write_new_file('1GB', 20)

if __name__ == "__main__":
    main()