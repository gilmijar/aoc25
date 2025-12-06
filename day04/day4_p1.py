from board import Board, Cell
from os import chdir
from pathlib import Path

me = Path(__file__)
chdir(me.parent)

file_name = "sample.txt"
file_name = 'input.txt'

datafile = open(file_name, "r", encoding="UTF-8").read().strip()

bd = Board.from_filling(datafile)

print(
        sum(bd.each_apply(
            lambda c: 1 if (
                c.neighbor_values.count("@") < 4 
                and
                c.value == '@'
                ) else 0,
        ))
)
