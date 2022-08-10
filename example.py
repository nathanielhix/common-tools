#!/usr/bin/env python3

import sys
import json
import net_tools

def main():
    servers = {}

    for x in sys.argv[1:]:
        server = net_tools.NetHost(x)
        server.host_ip()
        server.iface_status(server.hostname)
        servers[server.hostname] = server.__dict__

    print(json.dumps(servers, indent=2))


if __name__ == '__main__':
    sys.exit(main())
