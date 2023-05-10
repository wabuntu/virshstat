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

    result = subprocess.run(['ssh',
                            args.host,
                            'sudo virsh domstats --cpu-total --interface --block'],
                            capture_output=True,
                            text=True)
    lines = format(result.stdout)
    if len(lines) < 1:
        exit

    with open('dump.txt', mode='w') as f:
        f.writelines(lines)
    with open('dump.txt', mode='r') as f:
        lines = f.readlines()

    table = Table(title=args.host)
    columns = ["Domain", "CPU Time(G)", "Network R/W(GB)", "Disk R/W(GB)"]
    for column in columns:
        table.add_column(column, justify='right')

    row = ["", 0, 0, 0]
    index = -1
    bytes = []
    for line in lines:
        #        pdb.set_trace()
        index = line.find('Domain: ')
        if index >= 0:
            if len(row[0]):
                table.add_row(row[0], str(row[1]), str(row[2]), str(row[3]))
            row = [line[len('Domain: ')+2:-2], 0, 0, 0]
            index = -1
            continue

        index = line.find('cpu.time=')
        if index >= 0:
            row[1] = int(line[len('cpu.time=')+2:]) // UNIT
            index = -1
            continue

        bytes = re.findall(r'net\.[0-9].*\.bytes=([0-9]+)', line)
        if len(bytes) > 0:
            row[2] += int(bytes[0]) // UNIT
            bytes = []
            continue

        bytes = re.findall(r'block\.[0-9].*\.bytes=([0-9]+)', line)
        if len(bytes) > 0:
            row[3] += int(bytes[0]) // UNIT
            bytes = []
            continue

    console = Console()
    console.print(table)


def test_main():
    assert 0 == 0


if __name__ == "__main__":
    main()
