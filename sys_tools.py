from getpass import getuser, getpass
import sys


# Severity levels used in text formatting.
levels = [
    'info',
    'warn',
    'crit',
    'debug'
]


def print_exit(msg: str, severity: str, exit_status: int):
    std_err_levels = [
        'warn',
        'crit',
        'debug'
    ]

    if severity not in levels:
        severity = 'debug'

    msg = c_fmt(msg, severity)

    if severity in std_err_levels:
        print(f'{msg}', file=sys.stderr)
    else:
        print(f'{msg}')
    sys.exit(exit_status)


def c_fmt(msg: str, severity: str) -> str:
    if severity not in levels:
        severity = 'debug'

    c_reset = '\033[0m'

    colors = {
        'info': '\033[94m',
        'warn': '\033[93m',
        'crit': '\033[91m',
        'debug': '\033[96m'
    }

    return f'{colors[severity]}{msg}{c_reset}'


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
