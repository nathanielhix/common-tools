from getpass import getuser, getpass


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
