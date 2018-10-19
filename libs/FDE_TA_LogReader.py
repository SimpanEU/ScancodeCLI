import os
import re
from robot.api.deco import keyword

class  DLogRow:

    # perhaps we should have some sort of "factory" method, that can validate the input and return None if something is wrong
    # for example tab count not being 5, process not being name:pid etc
    # for that we should move the __init__ logic and have it in the factory, and have that return a DLogRow
    # logLine = DLogRowFactory.parseLine(inp)
    # if logLine != None:
    #   ...

    # Todo: convert timestamp to a numerical representation for easier comparison, or just check what tools python have...
    # Todo: do even want the getters in python ? or do we just want to access the attributes directly ?

    def __init__(self, inp):
        self.timestamp = []
        self.type = []
        self.processName = []
        self.processId = []
        self.moduleName = []
        self.message = []

        split = re.split(r'\t', inp.rstrip().rstrip('\t'))

        if len(split) == 5:
            self.timestamp = split[0]
            self.type = split[1]
            if len(split[3]) == 0:
                self.moduleName = None
            else:
                self.moduleName = split[3]

            self.message = split[4]
            procinfo = re.split(r':+', split[2])
            #print(procinfo)
            if len(procinfo) == 2:
                self.processName = procinfo[0]
                self.processId = procinfo[1]
            else:
                self.processName = split[2]
                self.processId = split[2]

    def getTimestamp(self):
        # return timestamp, perhaps we should convert it to a number (or have another method that does that)
        return self.timestamp


    def getType(self):
        # Log level event type, I/E/W/D etc
        return self.type

    def getProcessName(self):
        # array entry is something like notepad.exe:3311, and we want to split it on : and return notepad.exe
        return self.processName

    def getProcessId(self):
        # other part from notepad.exe:3311, we want to return the process id
        return self.processId

    def getModuleName(self):
        return self.moduleName

    def getMessage(self):
        # last array position, here we might want to do a sanity check, can message be empty in dlog1.txt ??
        # what if the message contains \t ? then we wont get any data since we look strictly at it being len 5
        # possible to have it >= 5, and concatinate eveything bigger to message ?
        # roll our own split that just split the first 5, then set message to whatever is left ?
        return self.message


#@keyword('Read FDE DLog')
def read_fde_dlog():

     for line in reversed(list(open(os.environ["ALLUSERSPROFILE"]+"\\CheckPoint\\Endpoint Security\\Full Disk Encryption\\dlog1.txt"))):
     #for line in reversed(list(open("C:\\work\\robot\\tests\\dlog1.txt"))):
        logLine: DLogRow = DLogRow(line)
        print("timestamp: ", logLine.getTimestamp())
        print("type: ", logLine.getType())
        print("processName: ", logLine.getProcessName())
        print("processId: ", logLine.getProcessId())
        print("module: ", logLine.getModuleName())
        print("message: ", logLine.getMessage())

        print("========================================")

def main():
    print("=== Parse_Log_Test ===")
    print()
    read_fde_dlog()

if __name__ == "__main__":
    main()
