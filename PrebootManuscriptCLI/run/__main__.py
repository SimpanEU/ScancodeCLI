import sys
from .classmodule import ManuscriptCLI

def main():

    args = sys.argv[1:]

    print('---------------------------------')
    print('User given     = {}'.format(args[0]))
    print('Password given = {}'.format(args[1]))
    print('Sleep given    = {}'.format(args[2]),'ms\n')
    print('Total Package count = {}'.format(len(list(args[0]))+len(list(args[1]))),'\n')


    cli_object = ManuscriptCLI('Preboot Manuscript')
    cli_object.create(str(args[0]), str(args[1]) , int(args[2]))


if __name__ == "__main__":
    main()