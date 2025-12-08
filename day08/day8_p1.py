from os import chdir
from pathlib import Path
from collections import namedtuple
from itertools import combinations
from math import hypot, prod
from time import monotonic

me = Path(__file__)
chdir(me.parent)
file_name = "sample.txt"
file_name = "input.txt"

raw = open(file_name, "r", encoding="UTF-8").read().strip('\n').splitlines()

def box_diff(a: "Box", b: "Box")->tuple[int, int, int]:
    x1, y1, z1 = a
    x2, y2, z2 = b
    return abs(x1 - x2), abs(y1 - y2), abs(z1 - z2)

Box = namedtuple('box', 'x y z') # type: ignore
boxes = [Box(*map(int, line.split(','))) for line in raw]
all_pairs = list(combinations(boxes, 2))

t0 = monotonic()
closest_pairs:list[tuple[Box, Box]] = []

for i in range(1000):
    closest_pair = min(all_pairs, key = lambda p: hypot(*box_diff(*p)))
    closest_pairs.append(closest_pair)
    p,k = closest_pair
    try:
        boxes.remove(p)
    except ValueError:
        pass
    try:
        boxes.remove(k)
    except ValueError:
        pass
    all_pairs.remove(closest_pair)

print("Finding closest pairs time:", monotonic() - t0)
t0 = monotonic()
cirquits = [{*pair} for pair in closest_pairs]+[set([b]) for b in boxes]
final_cirquits:list[set[Box]] = []

while cirquits:
    cirq = cirquits.pop()
    for c2 in cirquits:
        if not cirq.isdisjoint(c2):
            c2.update(cirq)
            break
    else:
        final_cirquits.append(cirq)


print("Merging cirquits time:", monotonic() - t0)
print('='*20)
print(prod(sorted((len(c) for c in final_cirquits), reverse=True)[:3]))
