from os import chdir
from pathlib import Path
from board import Board, Cell, UP, DOWN, LEFT, RIGHT

me = Path(__file__)
chdir(me.parent)
file_name = "sample.txt"
# file_name = 'input.txt'

datafile = open(file_name, "r", encoding="UTF-8").read().strip()

bd:Board = Board.from_filling(datafile)

print(bd)