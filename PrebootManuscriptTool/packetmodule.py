def calculatePackets(arg1, arg2=None):
    packets = 0

    # -u -p -t arguments given
    if arg1 is not None and arg2 is not None:
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

        packets += 6
        return packets


    # -s -t arguments given OR if running with no args
    elif arg1 is not None and arg2 is None:
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
        return packets
