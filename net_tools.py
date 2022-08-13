from getpass import getuser
from socket import gethostbyname
import subprocess
import sys


class NetHost:
    def __init__(
        self,
        hostname
    ):

        self.hostname = hostname
        self.ip_addr = None
        self.ifaces = {}
        self.outs = None
        self.errs = None


    def host_ip(self):
        self.ip_addr = get_host_ip(self.hostname)


    def iface_status(self, iface):
        ping_result = ping_check(iface)

        if ping_result is True:
            self.ifaces[iface] = 'up'
        elif ping_result is False:
            self.ifaces[iface] = 'down'
        else:
            self.ifaces[iface] = 'unknown'


    def ssh_cmd(self, user, cmd):
        self.outs, self.errs = ssh_cmd(self.hostname, user, cmd)


def get_host_ip(host_name):
    return gethostbyname(host_name)


def ping_check(host_name):
    cmd_ping = [
        'ping',
        '-c1',
        '-w4',
        host_name
    ]

    result = subprocess.run(
        cmd_ping,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode == 0:
        return True
    else:
        return False


def get_user_name(user_name):
    if user_name is None:
        user_name = getuser()

    return user_name


def ssh_cmd(host_name, user_name, cmd):
    # Verify there's an agent running.
    cmd_agent = [
        'ssh-add',
        '-l'
    ]

    result_agent = subprocess.run(
        cmd_agent,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf8'
    )

    if result_agent.returncode != 0:
        if len(result_agent.stdout) > 0:
            err_msg = result_agent.stdout
        elif len(result_agent.stderr) > 0:
            err_msg = result_agent.stderr
        else:
            err_msg = f'stderr and stdout empty, but returncode was non-zero: {result_agent.returncode}'

        print(f'ssh_cmd(): No key in ssh-agent: {err_msg}', file=sys.stderr)
        sys.exit(1)

    # Run ssh.
    if user_name is None:
        user_name = get_user_name(None)

    cmd_ssh = [
        'ssh',
        '-l',
        user_name,
        '-nA',
        host_name,
    ]

    cmd_ssh.extend(cmd)

    proc = subprocess.Popen(
        cmd_ssh,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf8'
    )

    try:
        outs, errs = proc.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()

    return outs.strip(), errs.strip()
