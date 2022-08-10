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
            self.ifaces[iface] = 'up'
        elif ping_result is False:
            self.ifaces[iface] = 'down'
        else:
            self.ifaces[iface] = 'unknown'


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
