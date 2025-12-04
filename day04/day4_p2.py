from board import Board, Cell
from os import chdir

chdir(__file__.rpartition("\\")[0])

file_name = "sample.txt"
file_name = 'input.txt'

datafile = open(file_name, "r", encoding="UTF-8").read().strip()

bd:Board = Board.from_filling(datafile)

changes = True
while changes:
    changes = False
    for c in bd.cells:
        if c.value == '@' and c.neighbor_values.count('@') < 4:
            c.value = 'o'
            changes= True

print(bd)
print(bd.count('o'))