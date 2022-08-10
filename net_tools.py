from socket import gethostbyname
import subprocess

class NetHost:
    def __init__(
        self,
        hostname
    ):

        self.hostname = hostname
        self.ip_addr = None
        self.ifaces = {}

    def host_ip(self):
        self.ip_addr = get_host_ip(self.hostname)

    def iface_status(self, iface):
        ping_result = ping_check(iface)

        if ping_result is True:
            result = 'up'
        elif ping_result is False:
            result = 'down'
        else:
            result = 'unknown'

        self.ifaces[iface] = result


def get_host_ip(host_name):
    return gethostbyname(host_name)

def ping_check(host_name):
    cmd_ping = [
        'ping',
        '-c1',
        '-w2',
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
