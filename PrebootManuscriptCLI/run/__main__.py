import argparse
from .classmodule import ManuscriptCLI


def main():
    parser = argparse.ArgumentParser(description='Preboot Manuscript CLI version 1.0', )
    parser.add_argument('-u', '--username', type=str, action='store', help='Username')
    parser.add_argument('-p', '--password', type=str, action='store', help='Password')
    parser.add_argument('-t', '--timeout', type=int, action='store', help='Timeout in milliseconds')
    parser.add_argument('-s', '--string', type=str, action='store', help='Full string to convert')
    args = parser.parse_args()

    # If no arguments given, normal start.
    if args.username is None and args.password is None and args.string is None:
        cli_object = ManuscriptCLI('Preboot Manuscript')
        print('\nPreboot Manuscript CLI version', cli_object.version)
        print('----------------------------------------')
        print('Enter a full string to convert:\nE.g. user<tab>password<enter>')
        s = input()
        print('\nEnter default timeout value in ms:')
        timeout = input()
        cli_object.create(s, None, timeout)

    # If -u, -p and -t arguments given, auto complete file.
    elif args.username is not None and args.password is not None and args.timeout is not None:
        cli_object = ManuscriptCLI('Preboot Manuscript')
        cli_object.create(str(args.username), str(args.password), int(args.timeout))

    # If -s and -t arguments given, auto complete file.
    elif args.string is not None and args.timeout is not None:
        cli_object = ManuscriptCLI('Preboot Manuscript')
        s = args.string
        timeout = args.timeout
        cli_object.create(s, None, timeout)


if __name__ == "__main__":
    main()
