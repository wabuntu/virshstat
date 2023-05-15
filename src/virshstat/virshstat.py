#! /usr/bin/python

# Copyright 2023
# All Rights Reserved
"""
Run virsh domstats
"""
import argparse
from rich.console import Console
from rich.table import Table
import re
import sys
import subprocess
import pdb
import textwrap

UNIT = 1000000000


def run_command(cmd):
    lines = ""
    result = subprocess.run(cmd,
                            capture_output=True,
                            text=True)
    lines = format(result.stdout)
    with open('dump.txt', mode='w') as f:
        f.writelines(lines)
    with open('dump.txt', mode='r') as f:
        lines = f.readlines()
    return lines


def create_table(host, columns):
    table = Table(title=host)
    for column in columns:
        table.add_column(column, justify='right')
    return table


def main():

    parser = argparse.ArgumentParser(
            prog='virshstat',
            description=textwrap.dedent('''\
                ***
                RUN eval `ssh-agent`; ssh-add ~/.ssh/id_rsa
                ***
                '''),
            add_help=True,
            )
    parser.add_argument('host', help='Target compute node')
    parser.add_argument('-p', help='Port number', type=int, default=22)
    args = parser.parse_args()

    lines = run_command(['ssh', args.host, 'sudo virsh domstats --cpu-total --interface --block'])

    table = create_table(args.host, ["Domain", "CPU(G)", "Net(GB)", "I/O(GB)", "Disk(GB)"])
    node = ""
    cpu, net, block, alloc, capa = 0, 0, 0, 0, 0
    index = -1
    bytes = []
    nodes = []
    cnt = 0

    for line in lines:
        #        pdb.set_trace()
        index = line.find('Domain: ')
        if index >= 0:
            if len(node):
                table.add_row(node, str(cpu), str(net), str(block), str(alloc)+'/'+str(capa))
                nodes.append([node, str(cpu), str(net), str(block), str(alloc)+'/'+str(capa)])
                cnt += 1
            node = line[len('Domain: ')+1:-2]
            cpu, net, block, alloc, capa = 0, 0, 0, 0, 0
            index = -1
            continue

        index = line.find('cpu.time=')
        if index >= 0:
            cpu = int(line[len('cpu.time=')+2:]) // UNIT
            index = -1
            continue

        bytes = re.findall(r'net\.[0-9].*\.bytes=([0-9]+)', line)
        if len(bytes) > 0:
            net += int(bytes[0]) // UNIT
            bytes = []
            continue

        bytes = re.findall(r'block\.[0-9].*\.bytes=([0-9]+)', line)
        if len(bytes) > 0:
            block += int(bytes[0]) // UNIT
            bytes = []
            continue

        bytes = re.findall(r'block\.[0-9]\.allocation=([0-9]+)', line)
        if len(bytes) > 0:
            alloc += int(bytes[0]) // UNIT
            bytes = []
            continue

        bytes = re.findall(r'block\.[0-9]\.capacity=([0-9]+)', line)
        if len(bytes) > 0:
            capa += int(bytes[0]) // UNIT
            bytes = []
            continue

    console = Console()
    console.print(table)

    # pdb.set_trace()

    for node in nodes:
        print('To get VM name: openstack server list -c Name -f value --all-projects --instance-name ' + node[0])


def test_main():
    assert 0 == 0


if __name__ == "__main__":
    main()
