#!/usr/bin/env python3

from multiprocessing import cpu_count
import argparse
import concurrent.futures
import json
import net_tools
import sys
import sys_tools


def main():
    args = create_parser()

    # The number of total cores.
    cores = cpu_count()

    # a list of NetHost objects.
    if args.target:
        server_list = [net_tools.NetHost(x) for x in args.target]
    else:
        msg = 'No hosts specified. Provide a space separated list of hosts.'
        sys_tools.print_exit(msg, 'crit', 1)

    # Run ping.
    servers = run_ping(server_list, cores)

    # Run ssh.
    cmd = ['uptime']
    for server in server_list:
        server.ssh_cmd('svc-admin', cmd)

    # Print the results
    print_results(server_list, args)


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


def create_parser():
    # Create a parser.
    parser = argparse.ArgumentParser(description='Common Tools Example')

    # Required arguments group.
    opts_req = parser.add_argument_group('Required Arguments')
    opts_req.add_argument('-t', '--target', nargs='+', required=True, help='Target network host.')

    opts_opt = parser.add_argument_group('Optional Arguments')
    opts_opt.add_argument('-i', '--input-file', help='The file to read from.')
    opts_opt.add_argument('-o', '--output-file', help='The file to write to.')

    opts_fmt = parser.add_mutually_exclusive_group(required=False)
    opts_fmt.add_argument('-j', '--json', action='store_true', help='Output in JSON format.')
    opts_fmt.add_argument('-c', '--csv', action='store_true', help='Output in CSV format.')

    return parser.parse_args()


def print_results(server_list, args):
    if args.json:
        results = {}
        for server in server_list:
            results[server.hostname] = {k:v for k, v in server.__dict__.items()}
        print(json.dumps(results, indent=2))

    elif args.csv:
        print(','.join(f'"{k}"' for k in server_list[0].__dict__.keys()))
        for server in server_list:
            print(','.join(f'"{v}"' for v in server.__dict__.values()))
    else:
        for server in server_list:
            for k, v in server.__dict__.items():
                print(f'{k}: {v}')


if __name__ == '__main__':
    sys.exit(main())
