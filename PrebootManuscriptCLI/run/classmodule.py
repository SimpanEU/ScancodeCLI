from .scancodemodule import *
import struct
import time


class ManuscriptCLI:
    version = 2
    binfile = 'C:\\manuscript.bin'

    def __init__(self, name):
        self.name = name

    @staticmethod
    def create(arg1=None, arg2=None, sleep=None):
        newfile = open(ManuscriptCLI.binfile, 'wb')

        def writeUpper(keycode, timeoutms):
            # Shift Key Down
            newfile.write(struct.pack('1B', 0))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', 42))
            # Char Key Down
            newfile.write(struct.pack('1B', 0))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', keycode))
            # Char Key Up
            newfile.write(struct.pack('1B', 1))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', keycode))
            # Shift Key Up
            newfile.write(struct.pack('1B', 1))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', 42))

        def writeLower(keycode, timeoutms):
            # Char Key Down
            newfile.write(struct.pack('1B', 0))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', keycode))
            # Char Key Up
            newfile.write(struct.pack('1B', 1))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', keycode))

        def writeSpecial(keycode, timeoutms):
            # Special Key Down
            newfile.write(struct.pack('1B', 0))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', keycode))
            # Special Key Up
            newfile.write(struct.pack('1B', 1))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', keycode))

        def writeSpecialKey(keycode, timeoutms):
            # Shift Key Down
            newfile.write(struct.pack('1B', 0))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', 42))
            # Char Key Down
            newfile.write(struct.pack('1B', 0))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', keycode))
            # Char Key Up
            newfile.write(struct.pack('1B', 1))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', keycode))
            # Shift Key Up
            newfile.write(struct.pack('1B', 1))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', 42))

        def writeHeader(pack):
            newfile.write(struct.pack('I', ManuscriptCLI.version))
            newfile.write(struct.pack('I', pack))

        def writeSleep(timeoutms):
            newfile.write(struct.pack('1B', 2))
            newfile.write(struct.pack('1H', int(timeoutms)))
            newfile.write(struct.pack('1B', 0))
            print('Input = sleep', timeoutms, 'ms ... Packets = 1')

        def writeCtrlAltDelete():
            # Ctrl Key Down
            print(win32api.MapVirtualKey(0x12, 0), 'ctrl scan code, vk = ', 0x12)
            newfile.write(struct.pack('1B', 0))
            newfile.write(struct.pack('1H', 32))
            newfile.write(struct.pack('1B', win32api.MapVirtualKey(0x11, 0)))  # ctrl
            # Alt Key Down
            newfile.write(struct.pack('1B', 0))
            newfile.write(struct.pack('1H', 32))
            newfile.write(struct.pack('1B', win32api.MapVirtualKey(0x12, 0)))  # alt
            # Delete Key Down
            newfile.write(struct.pack('1B', 0))
            newfile.write(struct.pack('1H', 32))
            newfile.write(struct.pack('1B', win32api.MapVirtualKey(0x2E, 0)))  # delete
            # Ctrl Key Up
            newfile.write(struct.pack('1B', 1))
            newfile.write(struct.pack('1H', 32))
            newfile.write(struct.pack('1B', win32api.MapVirtualKey(0x11, 0)))
            # Alt Key Up
            newfile.write(struct.pack('1B', 1))
            newfile.write(struct.pack('1H', 32))
            newfile.write(struct.pack('1B', win32api.MapVirtualKey(0x12, 0)))
            # Delete Key Up
            newfile.write(struct.pack('1B', 1))
            newfile.write(struct.pack('1H', 32))
            newfile.write(struct.pack('1B', win32api.MapVirtualKey(0x2E, 0)))

        # If -u, -p and -t arguments given.
        if arg1 is not None and arg2 is not None and sleep is not None:
            packets = 0

            for char in list(arg1):
                if not char.isalpha() and not char.isdigit():
                    packets += 4
                elif char.isupper():
                    packets += 4
                else:
                    packets += 2

            for char in list(arg2):
                if not char.isalpha() and not char.isdigit():
                    packets += 4
                elif char.isupper():
                    packets += 4
                else:
                    packets += 2

            # tab = 2, enter = 2, enter = 2 == 6
            packets += 6
            writeHeader(packets)

            # Username
            for c in list(arg1):
                if not c.isalpha() and not c.isdigit():
                    writeSpecialKey(getKey(c), sleep)
                elif c.isupper():
                    writeUpper(getKey(c), sleep)
                else:
                    writeLower(getKey(c), sleep)

            # Tab
            writeSpecial(getKey('tab'), sleep)

            # Password
            for c in list(arg2):
                if not c.isalpha() and not c.isdigit():
                    writeSpecialKey(getKey(c), sleep)
                elif c.isupper():
                    writeUpper(getKey(c), sleep)
                else:
                    writeLower(getKey(c), sleep)

            # Enter, Enter
            writeSpecial(getKey('enter'), sleep)
            writeSpecial(getKey('enter'), sleep)

            print('\nTotal packets:', packets)
            print(ManuscriptCLI.binfile, 'has been created!')

        # If -s and -t arguments given, OR if running with no args.
        if arg1 is not None and arg2 is None and sleep is not None:
            packets = 0
            stringInput = arg1.replace('<', ' <').replace('>', '> ').split()

            for word in stringInput:
                if '<' and '>' and 'sleep' in word:
                    packets += 1
                elif '<' and '>' and 'ctrlaltdelete' in word:
                    packets += 6
                elif '<' and '>' in word:
                    packets += 2
                else:
                    for char in list(word):
                        if not char.isalpha() and not char.isdigit():
                            packets += 4
                        elif char.isupper():
                            packets += 4
                        else:
                            packets += 2
            writeHeader(packets)

            for word in stringInput:
                if '<' and '>' and 'sleep' in word:
                    sleeper = word.replace('<', '').replace('>', '').replace('sleep', '').replace('=', '')
                    writeSleep(sleeper)
                elif '<' and '>' and 'ctrlaltdelete' in word:
                    writeCtrlAltDelete()
                elif '<' and '>' in word:
                    code = word.replace('<', '').replace('>', '')
                    writeSpecial(getKey(code), sleep)
                else:
                    for char in list(word):
                        if not char.isalpha() and not char.isdigit():
                            writeSpecialKey(getKey(char), sleep)
                        elif char.isupper():
                            writeUpper(getKey(char), sleep)
                        else:
                            writeLower(getKey(char), sleep)

            print('\nTotal packets:', packets)
            print(ManuscriptCLI.binfile, 'has been created!')
