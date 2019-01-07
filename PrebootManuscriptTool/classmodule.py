from scancodemodule import *
from writemodule import *
from packetmodule import *
import os


class ManuscriptClass:
    version = 2
    binfile = 'C:\\manuscript.bin'

    def __init__(self, name):
        self.name = name

    @staticmethod
    def create(arg1=None, arg2=None, sleep=None):
        file = ManuscriptClass.binfile
        ver = ManuscriptClass.version
        open(file, 'wb').close()

        # -u -p -t arguments given.
        if arg1 is not None and arg2 is not None and sleep is not None:
            packets = calculatePackets(arg1, arg2)
            writeHeader(file, packets, ver)

            # -u <Username>
            for c in list(arg1):
                if not c.isalpha() and not c.isdigit():
                    writeSpecialKey(file, getSC(c), sleep)
                elif c.isupper():
                    writeUpper(file, getSC(c), sleep)
                else:
                    writeLower(file, getSC(c), sleep)

            writeSpecial(file, getSC('tab'), sleep)

            # -p <Password>
            for c in list(arg2):
                if not c.isalpha() and not c.isdigit():
                    # TODO: Handling non-alpha/non-digit characters
                    # If user input needs shift usage to reproduce, like !"#¤
                    # writeSpecialKey() function is being used as seen below
                    # If user input does not need shift to reproduce, like ,.'¨
                    # writeSpecial() function SHOULD be used instead

                    writeSpecialKey(file, getSC(c), sleep)
                elif c.isupper():
                    writeUpper(file, getSC(c), sleep)
                else:
                    writeLower(file, getSC(c), sleep)

            writeSpecial(file, getSC('enter'), sleep)
            writeSpecial(file, getSC('enter'), sleep)

            print(file, 'has been created!')
            print('\nTotal packets:', packets)
            print('Total size:', os.path.getsize(file), 'bytes')

        # -s -t arguments given OR if running with no args.
        if arg1 is not None and arg2 is None and sleep is not None:
            packets = calculatePackets(arg1)
            writeHeader(file, packets, ver)

            stringInput = arg1.replace('<', ' <').replace('>', '> ').split()
            for word in stringInput:
                if '<' and '>' and 'sleep' in word:
                    sleeper = word.replace('<', '').replace('>', '').replace('sleep', '').replace('=', '')
                    writeSleep(file, sleeper)
                elif '<' and '>' and 'ctrlaltdelete' in word:
                    writeCtrlAltDelete(file)
                elif '<' and '>' in word:
                    code = word.replace('<', '').replace('>', '')
                    writeSpecial(file, getSC(code), sleep)
                else:
                    for char in list(word):
                        if not char.isalpha() and not char.isdigit():
                            writeSpecialKey(file, getSC(char), sleep)
                        elif char.isupper():
                            writeUpper(file, getSC(char), sleep)
                        else:
                            writeLower(file, getSC(char), sleep)

            print(file, 'has been created!')
            print('Total packets:', packets)
            print('Total size:', os.path.getsize(file), 'bytes')
