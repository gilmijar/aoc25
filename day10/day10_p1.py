from os import chdir
from pathlib import Path
from bitarray import bitarray, frozenbitarray as frba
from typing import Self
from itertools import chain

me = Path(__file__)
chdir(me.parent)
file_name = "sample.txt"
# file_name = "input.txt"

raw = open(file_name, "r", encoding="UTF-8").read().strip('\n').splitlines()

def parse(line:str) -> tuple[bitarray, list[bitarray], tuple[int]]:
    chunks = line.split()
    lights = frba(
        chunks.pop(0).strip('][').
        replace('.', '0').replace('#', '1')
    )
    jolts = tuple(map(int, chunks.pop().strip('}{').split(',')))
    buttons = []
    for chunk in chunks:
        button = bitarray(lights)
        button.setall(0)
        for wire in chunk[1:-1].split(','):
            button[int(wire)] = 1
        buttons.append(frba(button))
    return lights, buttons, jolts

machines = [parse(line)[:-1] for line in raw]

def render(x:bitarray)->str:
    return x.to01().replace('0', '.').replace('1', '#')

class Node:
    def __init__(self, lights:bitarray, parent:Self|None):
        self.lights = lights
        self.parent = parent
        self.arrival_cost = 0 if parent is None else (parent.arrival_cost + 1)
        self.button = None

    def history(self):
        if self.parent is None:
            return []
        else:
            return self.parent.history() + [tuple(i for i,v in enumerate(self.button) if v )]

    @property
    def lineage(self):
        if self.parent is None:
            return []
        else:
            return self.parent.lineage + [self]

    def __repr__(self):
        return render(self.lights)


def a_star(target: bitarray, operations:list[bitarray])->list[bitarray]:
    def comp(x:Node)->int:
        return x.arrival_cost + (x.lights ^ target).count()

    node = Node(frba(len(target)), None)
    open, closed = [node], []
    while open:
        # find q
        candidate = min(open, key=comp)
        open.remove(candidate)
        for op in operations:
            successor = Node(
                candidate.lights ^ op,
                parent=candidate
            )
            successor.button = op
            if successor.lights == target:
                return successor
            existing = [(n.lights==successor.lights and n.arrival_cost<=successor.arrival_cost) for n in chain(open, closed)]
            if not any(existing):
                open.append(successor)
        closed.append(candidate)

total = 0
for machine in machines:
    x = a_star(*machine)
    print(x.history(), len(x.lineage))
    total += len(x.lineage)

print('=' * 20)
print(total)