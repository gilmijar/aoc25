from os import chdir
from pathlib import Path
from typing import Self
from itertools import chain
from heapq import heappush, heappop

type Jolt = tuple[int]
type Btn = tuple[int]
type Buttons = list[Btn]

me = Path(__file__)
chdir(me.parent)
file_name = "sample.txt"
# file_name = "input.txt"

raw = open(file_name, "r", encoding="UTF-8").read().strip('\n').splitlines()

def parse(line:str) -> tuple[Jolt, Buttons]:
    chunks = line.split()
    _ = chunks.pop(0)
    jolts = tuple(map(int, chunks.pop().strip('}{').split(',')))
    buttons = [tuple(map(int, chunk[1:-1].split(','))) for chunk in chunks]
    return jolts, buttons

machines = [parse(line) for line in raw]

class Node:
    def __init__(self, jolts:Jolt, parent:Self|None):
        self.jolts = jolts
        self.parent = parent
        self.arrival_cost = 0 if parent is None else (parent.arrival_cost + 1)
        self.button = tuple()
        self.comp_f = lambda x: x

    @property
    def history(self):
        if self.parent is None:
            return []
        else:
            return self.parent.history + [tuple(i for i,v in enumerate(self.button) if v )]

    @property
    def lineage(self):
        if self.parent is None:
            return []
        else:
            return self.parent.lineage + [self]

    def __repr__(self):
        return str(self.jolts)

    def __lt__(self, other:Self):
        self.arrival_cost < other.arrival_cost


def joltify(base: Jolt, btn: Btn):
    x = list(base)
    for wire in btn:
        x[wire] += 1
    return tuple(x)


def a_star(target: Jolt, operations:Buttons)->Node:
    iterations = 0
    misses = 0

    node = Node((0,) * len(target), None)
    open, closed = [], []
    heappush(open, node)
    while open:
        iterations += 1
        # find q
        candidate = heappop(open)

        for op in operations:
            successor = Node(
                joltify(candidate.jolts, op),
                parent=candidate
            )
            successor.button = op
            if successor.jolts == target:
                print(f"{iterations=}; {misses=}")
                return successor
            if any((s > t for s, t in zip(successor.jolts, target))):
                continue
            existing = [(n.jolts==successor.jolts and n.arrival_cost<=successor.arrival_cost) for n in chain(open, closed)]
            if not any(existing):
                heappush(open, successor)
            else:
                # misses += len(successor.lineage)
                pass
        closed.append(candidate)

total = 0
for machine in machines:
    x = a_star(*machine)
    # print(x.history, len(x.lineage))
    print(len(x.lineage), flush=True)
    total += len(x.lineage)

print('=' * 20)
print(total)