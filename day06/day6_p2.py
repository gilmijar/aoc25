from typing import Iterable
from os import chdir
from pathlib import Path

me = Path(__file__)
chdir(me.parent)
file_name = "sample.txt"
file_name = "input.txt"


def prod(factors: Iterable[int]) -> int:
    result = 1
    for factor in factors:
        result *= factor
    return result


proc = {"+": sum, "*": prod}

raw = open(file_name, "r", encoding="UTF-8").read().strip('\n').splitlines()
ops = raw[-1].split()
rows_transposed = list(map("".join, zip(*raw[:-1])))

with open('cmp.txt', 'w') as f:
    for line in rows_transposed:
        f.write(line + '\n')

groups = []
curr_group = []
for line in rows_transposed:
    lean_line = line.strip()
    if lean_line:
        curr_group.append(int(lean_line))
    else:
        groups.append(curr_group)
        curr_group = []

if curr_group:
    groups.append(curr_group)

total = 0
for op, group in zip(ops, groups):
    result = proc[op](group)
    total += result
    print(op, group, result)

print("===>", total)
