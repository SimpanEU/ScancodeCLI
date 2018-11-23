import sys
import argparse
from .classmodule import ManuscriptCLI


def main():
    parser = argparse.ArgumentParser(description='Preboot Manuscript CLI version 1.0', )
    parser.add_argument('-u', '--username', type=str, action='store', help='Username')
    parser.add_argument('-p', '--password', type=str, action='store', help='Password')
    parser.add_argument('-t', '--timeout', type=int, action='store', help='Timeout in milliseconds')
    args = parser.parse_args()

    if args.username is not None and args.password is not None and args.timeout is not None:
        cli_object = ManuscriptCLI('Preboot Manuscript')
        cli_object.create(str(args.username), str(args.password), int(args.timeout))

    if args.username is None and args.password is None:
        print('\nPreboot Manuscript CLI version 1.0')
        print('----------------------------------------')
        print('Enter a full string to convert:\nE.g. user<tab>password<enter>')
        test = input()
        print('\nEnter default timeout value:')
        timeout = input()
        print('\nTotal Package count =', len(list(test)))

    # args = sys.argv[1:]
    # print('---------------------------------')
    # print('User given     = {}'.format(args[0]))
    # print('Password given = {}'.format(args[1]))
    # print('Sleep given    = {}'.format(args[2]),'ms\n')
    # print('Total Package count = {}'.format(len(list(args[0]))+len(list(args[1]))),'\n')
    # cli_object = ManuscriptCLI('Preboot Manuscript')
    # cli_object.create(str(args[0]), str(args[1]) , int(args[2]))


if __name__ == "__main__":
    main()
