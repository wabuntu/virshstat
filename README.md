# virshstat

## Detail

A single python script which ...
1. Runs virsh domstat
2. Summarizes load data
3. Prints in TUI table format

## Install

1. Download and install
  - Download whl file from : https://github.com/wabuntu/virshstat/tree/main/dist
  - pip3 install  --no-deps ./virshstat-*.whl

2. Or just copy .py file from 
  - https://github.com/wabuntu/virshstat/tree/main/src/virshstat

## Example

vm000000000000001

Example result
```
% python ./virshstat.py comp-node0
                     comp-node0                      
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃            Domain ┃ CPU Time(G) ┃ Network R/W(GB) ┃ Disk R/W(GB) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ vm000000000000001 │        1285 │            4386 │        27517 │
│ vm000000000000002 │       12615 │             659 │          845 │
│ vm000000000000003 │       80223 │             872 │          668 │
│ vm000000000000004 │       41616 │            3128 │         7924 │
│ vm000000000000005 │       11802 │             814 │        51821 │
│ vm000000000000006 │       22176 │            4475 │        10518 │
│ vm000000000000007 │       15374 │             354 │          540 │
│ vm000000000000008 │       66201 │            5804 │        14398 │
│ vm000000000000009 │      171361 │               0 │         5991 │
│ vm000000000000010 │       36385 │            1289 │         3816 │
└───────────────────┴─────────────┴─────────────────┴──────────────┘

```
