from os import chdir
from pathlib import Path
from collections import namedtuple
from itertools import combinations, chain
from math import dist, prod
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
