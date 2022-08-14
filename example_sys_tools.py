#!/usr/bin/env python3

import sys_tools
import sys


def main():
    try:
        file_name = sys.argv[1]
    except IndexError:
        msg = 'No file name supplied.'
        sys_tools.print_exit(msg, 'crit', 1)

    for line in sys_tools.file_read_lines(file_name):
        print(line)

    print(f'{chr(10)}{sys_tools.c_fmt("Printing color formatting.", "info")}{chr(10)}')

    for word in ['info', 'warn', 'crit', 'debug']:
        print(sys_tools.c_fmt(word, word))


if __name__ == '__main__':
    sys.exit(main())
