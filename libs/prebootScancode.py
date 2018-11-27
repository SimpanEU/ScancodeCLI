import os
import subprocess
from subprocess import PIPE


def create_scancode_bin(user, passwd, timeout):
    # PrebootManuscriptCLI folder
    path = 'C:\\DA\\robot\\PrebootManuscriptCLI'
    os.chdir(path)

    if os.getcwd() == path:
        cmd = 'python -m run -u ' + user + ' -p ' + passwd + ' -t ' + timeout
        print(cmd)
        subprocess.Popen(cmd, shell=True, stdin=PIPE, stderr=PIPE, stdout=PIPE).communicate()


def main():
    create_scancode_bin('simpan', 'password', '32')


if __name__ == "__main__":
    main()
