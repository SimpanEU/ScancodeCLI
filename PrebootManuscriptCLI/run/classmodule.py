from .scancodemodule import *
import struct

class ManuscriptCLI:

    def __init__(self, name):
        self.name = name
        self.version = 1

    @staticmethod
    def create(arg1, arg2, sleep):
        newfile = open('C:\\manuscript.bin', 'wb')

        version = 1
        newfile.write(struct.pack('I', version))

        packets = int(len(list(arg1)) + int(len(list(arg2))))
        newfile.write(struct.pack('I', packets))

        # versiontest = [b'V01']
        # newfile.write(struct.pack('3s', *versiontest))
        #
        # packetstest = 'P' + str(len(list(arg1)) + len(list(arg2)))
        # packetstest = bytes(packetstest, 'utf-8')
        # newfile.write(struct.pack('3b', *packetstest))

        for c in list(arg1):
            code = key(c)
            newfile.write(struct.pack('1B', code))
            newfile.write(struct.pack('1h', sleep))

        for c in list(arg2):
            code = key(c)
            newfile.write(struct.pack('1B', code))
            newfile.write(struct.pack('1h', sleep))

        print('C:\\manuscript.bin created')