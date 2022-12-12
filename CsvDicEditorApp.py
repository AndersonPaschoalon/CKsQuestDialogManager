import getopt
import sys
from PyUtils.CsvDicEditor import CsvDicEditor

def parse_args(argv):
    filename = ""
    try:
        options, args = getopt.getopt(argv, 'f:', ['filename='])
        for opt, arg in options:
            if opt in ('-f', '--filename'):
                filename = arg
    except getopt.GetoptError:
        print('The wrong option is provided')
    return [filename]


if __name__ == '__main__':
    argv = sys.argv[1:]
    [filename] = parse_args(argv)
    editor = CsvDicEditor()
    editor.run_app(filename)