from os import chdir
from pathlib import Path
from collections import namedtuple
from itertools import combinations, chain
from math import dist
from time import monotonic

me = Path(__file__)
chdir(me.parent)
file_name = "sample.txt"
file_name = "input.txt"

raw = open(file_name, "r", encoding="UTF-8").read().strip('\n').splitlines()

Box = namedtuple('box', 'x y z') # type: ignore
boxes = {Box(*map(int, line.split(','))) for line in raw}

t0 = monotonic()
all_pairs = sorted(combinations(boxes, 2), key=lambda pair: dist(*pair))
closest_pairs = all_pairs[:1000]
boxes -= {chain(*zip(*closest_pairs))}

print("Finding closest pairs time:", monotonic() - t0)
t0 = monotonic()

cirquits = [{*pair} for pair in closest_pairs] + [{box} for box in boxes]
cnt = 0
while len(cirquits)>1:
    cirq = cirquits.pop()
    for c2 in cirquits:
        if not cirq.isdisjoint(c2):
            c2.update(cirq)
            break
    else:
        cirquits.append(cirq)
        closest_pair = all_pairs.pop(0)
        try:
            cirquits.remove(closest_pair[0])
        except ValueError:
            pass
        try:
            cirquits.remove(closest_pair[1])
        except ValueError:
            pass
        cirquits.append({*closest_pair})
        cnt += 1

print("Merging cirquits time:", monotonic() - t0)
print('='*20)
print(f"{closest_pair=}, {cnt=}")
print(closest_pair[0].x * closest_pair[1].x)
