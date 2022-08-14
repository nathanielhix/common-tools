from getpass import getuser, getpass
import sys


levels = [
    'info',
    'warn',
    'crit',
    'debug'
]


def print_exit(msg: str, severity: str, exit_status: int):
    if severity not in levels:
        severity = 'debug'

    msg = c_fmt(msg, severity)

    if severity == 'debug':
        print(f'{msg}', file=sys.stderr)
    else:
        print(f'{msg}')
    sys.exit(exit_status)


def c_fmt(msg: str, severity: str) -> str:
    if severity not in levels:
        severity = 'debug'

    c_info = '\033[94m'
    c_warn = '\033[93m'
    c_crit = '\033[91m'
    c_debug = '\033[96m'
    c_reset = '\033[0m'

    msg = f'{msg}{c_reset}'

    if severity == 'info':
        return f'{c_info}{msg}'
    elif severity == 'warn':
        return f'{c_warn}{msg}'
    elif severity == 'crit':
        return f'{c_crit}{msg}'
    elif severity == 'debug':
        return f'{c_debug}{msg}'


def get_user_name(user_name):
    if user_name is None:
        user_name = getuser()

    return user_name


def get_passwd():
    passwd = None

    while passwd is None:
        passwd = getpass()

        if not passwd.strip():
            passwd = None

    return passwd


def file_read_lines(file_name: str) -> list:
    with open(file_name, 'r') as f:
        return f.read().splitlines()
