import win32api
import struct


def writeUpper(binfile, scancode, timeoutms):
    manuscript = open(binfile, 'ab')

    # Shift Key Down
    manuscript.write(struct.pack('1B', 0))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', 42))

    # Char Key Down
    manuscript.write(struct.pack('1B', 0))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', scancode))

    # Char Key Up
    manuscript.write(struct.pack('1B', 1))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', scancode))

    # Shift Key Up
    manuscript.write(struct.pack('1B', 1))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', 42))

    manuscript.close()


def writeLower(binfile, scancode, timeoutms):
    manuscript = open(binfile, 'ab')

    # Char Key Down
    manuscript.write(struct.pack('1B', 0))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', scancode))

    # Char Key Up
    manuscript.write(struct.pack('1B', 1))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', scancode))
    manuscript.close()


def writeSpecial(binfile, scancode, timeoutms):
    # Special keys that dosnt require shift usage, e.g. alt, tab, shift, ctrl, .,-'¨

    manuscript = open(binfile, 'ab')

    # Special Key Down
    manuscript.write(struct.pack('1B', 0))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', scancode))

    # Special Key Up
    manuscript.write(struct.pack('1B', 1))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', scancode))

    manuscript.close()


def writeSpecialKey(binfile, scancode, timeoutms):
    # Special Keys that requires shift usage, e.g. !"#¤%;:*^

    manuscript = open(binfile, 'ab')

    # Shift Key Down
    manuscript.write(struct.pack('1B', 0))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', 42))

    # Char Key Down
    manuscript.write(struct.pack('1B', 0))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', scancode))

    # Char Key Up
    manuscript.write(struct.pack('1B', 1))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', scancode))

    # Shift Key Up
    manuscript.write(struct.pack('1B', 1))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', 42))

    manuscript.close()


def writeHeader(binfile, version, totalPackets):
    # First 4 bytes in binfile

    manuscript = open(binfile, 'ab')

    manuscript.write(struct.pack('I', version))
    manuscript.write(struct.pack('I', totalPackets))

    manuscript.close()


def writeSleep(binfile, timeoutms):
    manuscript = open(binfile, 'ab')

    manuscript.write(struct.pack('1B', 2))
    manuscript.write(struct.pack('1H', int(timeoutms)))
    manuscript.write(struct.pack('1B', 0))

    manuscript.close()


def writeCtrlAltDelete(binfile):
    manuscript = open(binfile, 'ab')

    # Ctrl Key Down
    manuscript.write(struct.pack('1B', 0))
    manuscript.write(struct.pack('1H', 32))
    manuscript.write(struct.pack('1B', win32api.MapVirtualKey(0x11, 0)))  # ctrl

    # Alt Key Down
    manuscript.write(struct.pack('1B', 0))
    manuscript.write(struct.pack('1H', 32))
    manuscript.write(struct.pack('1B', win32api.MapVirtualKey(0x12, 0)))  # alt

    # Delete Key Down
    manuscript.write(struct.pack('1B', 0))
    manuscript.write(struct.pack('1H', 32))
    manuscript.write(struct.pack('1B', win32api.MapVirtualKey(0x2E, 0)))  # delete

    # Ctrl Key Up
    manuscript.write(struct.pack('1B', 1))
    manuscript.write(struct.pack('1H', 32))
    manuscript.write(struct.pack('1B', win32api.MapVirtualKey(0x11, 0)))

    # Alt Key Up
    manuscript.write(struct.pack('1B', 1))
    manuscript.write(struct.pack('1H', 32))
    manuscript.write(struct.pack('1B', win32api.MapVirtualKey(0x12, 0)))

    # Delete Key Up
    manuscript.write(struct.pack('1B', 1))
    manuscript.write(struct.pack('1H', 32))
    manuscript.write(struct.pack('1B', win32api.MapVirtualKey(0x2E, 0)))

    manuscript.close()
