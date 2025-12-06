from os import chdir
from pathlib import Path
me = Path(__file__)
chdir(me.parent)
file_name = "sample.txt"
file_name = 'input.txt'

datafile = open(file_name, "r", encoding="UTF-8").read().strip().splitlines()

empty_line = datafile.index("")
s_ranges = datafile[:empty_line]
s_items = datafile[empty_line+1:]

def parse_range(rng: str)->tuple[int, int]:
    a, b, *_ = map(int, rng.split('-'))
    return a, b+1

ranges = tuple(range(*parse_range(r)) for r in s_ranges)
items = tuple(int(x) for x in s_items)

# check
fresh: list[int] = []
for item in items:
    for range in ranges:
        '''QUADRATIC!!!!!! YEAH!'''
        if item in range:
            fresh.append(item)
            break

print(fresh)
print(len(fresh))
