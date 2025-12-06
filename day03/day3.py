from os import chdir
from pathlib import Path

me = Path(__file__)
chdir(me.parent)

file_name = 'sample.txt'
file_name = 'input.txt'

datafile = open(file_name, 'r', encoding='UTF-8').read().strip().splitlines()

def find_max_jolts(line:str)->int:
    max_digit = max(line[:-1])
    max_index = line.index(max_digit)
    rest = line[max_index+1:]

    second_digit = max(rest)

    return int(max_digit + second_digit)


total = sum( find_max_jolts(line) for line in datafile)

print(total)