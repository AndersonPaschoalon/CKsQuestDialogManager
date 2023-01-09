import subprocess
import traceback
import os


class Console:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def yellow(printStr):
        print(f"{Console.WARNING}{printStr}{Console.ENDC}")

    @staticmethod
    def blue(printStr):
        print(f"{Console.OKBLUE}{printStr}{Console.ENDC}")

    @staticmethod
    def cyan(printStr):
        print(f"{Console.OKCYAN}{printStr}{Console.ENDC}")

    @staticmethod
    def green(printStr):
        print(f"{Console.OKGREEN}{printStr}{Console.ENDC}")

    @staticmethod
    def red(printStr):
        print(f"{Console.FAIL}{printStr}{Console.ENDC}")

    @staticmethod
    def bold(printStr):
        print(f"{Console.BOLD}{printStr}{Console.ENDC}")

    @staticmethod
    def underline(printStr):
        print(f"{Console.UNDERLINE}{printStr}{Console.ENDC}")

    @staticmethod
    def execute(command: str):
        bypass = False
        if bypass:
            print("$ " + command)
            return [0, bytes(command, 'utf-8'), bytes("bypass test", 'utf-8')]
        ret = subprocess.run(command, shell=True, capture_output=True)
        return [ret.returncode, ret.stdout, ret.stderr]

    @staticmethod
    def touch(path):
        try:
            basedir = os.path.dirname(path)
            if basedir != "":
                if not os.path.exists(basedir):
                    os.makedirs(basedir)
            with open(path, 'a'):
                os.utime(path, None)
            return True
        except:
            traceback.print_exc()
            return False

