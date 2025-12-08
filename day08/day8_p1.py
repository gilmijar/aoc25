from os import chdir
from pathlib import Path
from collections import namedtuple
from itertools import combinations
from math import hypot
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


for i in range(10):
    closest_pair = min(all_pairs, key = lambda p: hypot(*box_diff(*p)))
    closest_pairs.append(closest_pair)
    print('==>', i, hypot(*box_diff(*closest_pair)))
    del all_pairs[all_pairs.index(closest_pair)]


print(monotonic() - t0)