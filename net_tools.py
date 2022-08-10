from socket import gethostbyname

class NetHost:
    def __init__(
        self,
        hostname
    ):

        self.hostname = hostname
        self.ip_addr = None

    def host_ip(self):
        self.ip_addr = get_host_ip(self.hostname)


def get_host_ip(host_name):
    return gethostbyname(host_name)
