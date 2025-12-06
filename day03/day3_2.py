from os import chdir
from pathlib import Path

me = Path(__file__)
chdir(me.parent)

file_name = 'sample.txt'
file_name = 'input.txt'

datafile = open(file_name, 'r', encoding='UTF-8').read().strip().splitlines()

def find_max_jolts(line:str)->int:
    digits:list[str] = []
    for x in range(-11, 0, 1):
        max_digit = max(line[:x])
        digits.append(max_digit)
        line = line.partition(max_digit)[2]
    last_digit = max(line)
    digits.append(last_digit)
    result = ''.join(digits)
    # print('=>', result)
    return int(result)
 

total = sum( find_max_jolts(line) for line in datafile)

print(total)