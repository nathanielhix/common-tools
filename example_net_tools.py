#!/usr/bin/env python3

from multiprocessing import cpu_count
import concurrent.futures
import json
import net_tools
import sys


def main():
    # The number of total cores.
    cores = cpu_count()

    # a list of NetHost objects.
    server_list = [net_tools.NetHost(x) for x in sys.argv[1:]]

    # Run ping.
    servers = run_ping(server_list, cores)

    # Run ssh.
    cmd = ['uptime']
    for x in server_list:
        x.ssh_cmd('svc-admin', cmd)

    # Print the results
    print(json.dumps(servers, indent=2))


def run_ping(server_list, cores):
    # A dictionary of NetHost objects.
    servers = {}

    # Ping NetHost objects concurrently.
    with concurrent.futures.ThreadPoolExecutor(max_workers=cores) as executor:
        future_ping_proc = {executor.submit(ping_server, server): server for server in server_list}
        for future in concurrent.futures.as_completed(future_ping_proc):
            server = future_ping_proc[future]

            try:
                server = future.result()
            except Exception as exc:
                print(f'{server.hostname} generated an exception: {exc}')

            servers[server.hostname] = server.__dict__

    return servers


def ping_server(server):
    server.host_ip()
    server.iface_status(server.hostname)

    return server


if __name__ == '__main__':
    sys.exit(main())
