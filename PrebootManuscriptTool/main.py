#!/usr/bin/env python3

import argparse
from classmodule import ManuscriptClass


def main():
    cli_object = ManuscriptClass('Pre-boot Manuscript')

    parser = argparse.ArgumentParser(description='Pre-boot Manuscript CLI version ' + str(cli_object.version))
    parser.add_argument('-u', '--username', type=str, action='store', help='Username')
    parser.add_argument('-p', '--password', type=str, action='store', help='Password')
    parser.add_argument('-t', '--timeout', type=int, action='store', help='Timeout in milliseconds')
    parser.add_argument('-s', '--string', type=str, action='store', help='Full string to convert')
    args = parser.parse_args()

    # If no arguments given, normal start.
    if args.username is None and args.password is None and args.string is None:
        print('-----------------------------------------------------')
        print('''  __  __   _   _  _ _   _ ___  ___ ___ ___ ___ _____ 
 |  \/  | /_\ | \| | | | / __|/ __| _ \_ _| _ \_   _|
 | |\/| |/ _ \| .` | |_| \__ \ (__|   /| ||  _/ | |  
 |_|  |_/_/ \_\_|\_|\___/|___/\___|_|_\___|_|   |_|  ''')

        print('-----------------------------------------------------')
        print('*** Pre-boot Manuscript Tool version', str(cli_object.version)+'.0 ***')

        print('\nAll characters will be converted to scan codes.')
        print('Tabular or Enter keystrokes must be placed within <>\nE.g. username<tab>password<enter><sleep=1000><enter>')
        print('\nEnter a full string to create a manuscript:\n')
        s = input()
        print('\nEnter default timeout value in milliseconds for each key simulation:')
        timeout = input()
        print()
        cli_object.create(s, None, timeout)

    # If -u, -p and -t arguments given, auto-complete file.
    elif args.username is not None and args.password is not None and args.timeout is not None:
        print()
        cli_object.create(str(args.username), str(args.password), int(args.timeout))

    # If -s and -t arguments given, auto-complete file.
    elif args.string is not None and args.timeout is not None:
        s = args.string
        timeout = args.timeout
        print()
        cli_object.create(s, None, timeout)


if __name__ == "__main__":
    main()
