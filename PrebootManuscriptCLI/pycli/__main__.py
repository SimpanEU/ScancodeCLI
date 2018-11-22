import sys
import getopt
from .classmodule import MyClass

def main():

    args = sys.argv[1:]

    print('User given = {}'.format(args[0]))
    print('Password given = {}'.format(args[1]))
    print('Sleep given = {}'.format(args[2]),'ms\n')
    print('Total Package count = {}'.format(len(list(args[0]))+len(list(args[1]))),'\n')


    my_object = MyClass('Preboot Manuscript')
    my_object.create_manuscript(str(args[0]), str(args[1]) , int(args[2]))

    print('C:\\manuscript.bin created')

    with open('C:\\manuscript.bin', 'rb') as f:
        print(f.read())