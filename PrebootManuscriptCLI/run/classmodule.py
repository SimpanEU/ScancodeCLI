from .scancodemodule import *
import struct


class ManuscriptCLI:

    version = 1
    binfile = 'C:\\manuscript.bin'

    def __init__(self, name):
        self.name = name

    @staticmethod
    def create(arg1=None, arg2=None, sleep=None):
        newfile = open(ManuscriptCLI.binfile, 'wb')

        # If -u, -p and -t arguments given.
        if arg1 is not None and arg2 is not None and sleep is not None:
            newfile.write(struct.pack('I', ManuscriptCLI.version))
            packets = int(len(list(arg1)) + int(len(list(arg2))))
            newfile.write(struct.pack('I', packets))

            for c in list(arg1):
                code = getKey(c)
                newfile.write(struct.pack('1B', code))
                newfile.write(struct.pack('1h', sleep))

            for c in list(arg2):
                code = getKey(c)
                newfile.write(struct.pack('1B', code))
                newfile.write(struct.pack('1h', sleep))

            print('Total packets:', packets)
            print(ManuscriptCLI.binfile, 'has been created!')

        # If -s and -t arguments given, OR if running with no args.
        if arg1 is not None and arg2 is None and sleep is not None:
            packets = 0
            stringInput = arg1.replace('<', ' <').replace('>', '> ').split()

            for word in stringInput:
                if '<' and '>' in word:
                    packets += 1
                else:
                    for char in list(word):
                        packets += 1

            newfile.write(struct.pack('I', ManuscriptCLI.version))
            newfile.write(struct.pack('I', packets))

            for word in stringInput:
                if '<' and '>' in word:
                    code = word.replace('<', '').replace('>', '')
                    code = getKey(code)
                    newfile.write(struct.pack('1B', code))
                    newfile.write(struct.pack('1h', int(sleep)))
                else:
                    for char in list(word):
                        code = getKey(char)
                        newfile.write(struct.pack('1B', code))
                        newfile.write(struct.pack('1h', int(sleep)))

            print('\nTotal packets:', packets)
            print(ManuscriptCLI.binfile, 'has been created!')
