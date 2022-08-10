#!/usr/bin/env python3

import sys
import json
import net_tools

def main():
    user_input = sys.argv[1]

    server = net_tools.NetHost(user_input)
    server.host_ip()
    server.iface_status(server.hostname)

    for k, v in server.__dict__.items():
        print(f'DEBUG: {k}: {v}', file=sys.stderr)

    print(json.dumps(server.__dict__))


if __name__ == '__main__':
    sys.exit(main())
