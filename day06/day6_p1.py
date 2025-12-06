from typing import Collection
from os import chdir
from pathlib import Path
me = Path(__file__)
chdir(me.parent)
file_name = "sample.txt"
file_name = "input.txt"


def prod(factors: Collection[int])->int:
    result = 1
    for factor in factors:
        result *= factor
    return result

raw = open(file_name, "r", encoding="UTF-8").read().strip().splitlines()
*rows, ops = (r.split() for r in raw)
cols = [list(map(int, c)) for c in zip(*rows)]
proc = {"+": sum, "*": prod}

final = 0
for op, col in zip(ops, cols):
    x = proc[op](col)
    final += x

print(final)