from os import chdir
from pathlib import Path
from board import Board, DOWN, LEFT, RIGHT
from time import monotonic

me = Path(__file__)
chdir(me.parent)
file_name = "sample.txt"
file_name = 'input.txt'
datafile = open(file_name, "r", encoding="UTF-8").read().strip()
bd:Board = Board.from_filling(datafile)
for c in bd.cells:
    c.extra = 0

S = bd.find('S')[0]
S.neighbor(DOWN).extra = 1
front = {S.neighbor(DOWN)}
for lvl in range(1, bd.height-1):
    t0 = monotonic()
    new_front = set()
    for cell in front:
        if cell == '^':
            # there won't be ^ in front that were not reached by a beam
            cell.neighbor(LEFT).value = '|'
            cell.neighbor(RIGHT).value = '|'
            next_left = cell.neighbor(LEFT).neighbor(DOWN)
            next_right = cell.neighbor(RIGHT).neighbor(DOWN)
            next_left.extra += cell.extra 
            next_right.extra += cell.extra
            new_front.add(next_left)
            new_front.add(next_right)
        else:
            cell.value = '|'
            cell.neighbor(DOWN).extra += cell.extra
            new_front.add(cell.neighbor(DOWN))
    front = new_front
    print(lvl, round(monotonic()-t0, 3), 'sec')

print(sum(c.extra for c in front))
