from os import chdir
from pathlib import Path
from board import Board, Cell, UP, DOWN, LEFT, RIGHT

me = Path(__file__)
chdir(me.parent)
file_name = "sample.txt"
file_name = 'input.txt'
datafile = open(file_name, "r", encoding="UTF-8").read().strip()
bd:Board = Board.from_filling(datafile)

splits = 0
S = bd.find('S')[0]
front = {S.neighbor(DOWN)}
for _ in range(1, bd.height):
    new_front = set()
    for cell in front:
        if cell == '^':
            # there won't be ^ in front that were not reached by a beam
            cell.neighbor(LEFT).value = '|'
            cell.neighbor(RIGHT).value = '|'
            new_front.add(cell.neighbor(LEFT).neighbor(DOWN))
            new_front.add(cell.neighbor(RIGHT).neighbor(DOWN))
            splits += 1
        else:
            cell.value = '|'
            new_front.add(cell.neighbor(DOWN))
    front = new_front
    print('=' * 50)
    print(bd)
    input(f'{splits =}, next? ')

