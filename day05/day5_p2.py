from os import chdir
chdir(__file__.rpartition("\\")[0])

file_name = "sample.txt"
file_name = 'input.txt'

datafile = open(file_name, "r", encoding="UTF-8").read().strip().splitlines()

def merge_ranges(a: tuple[int,int], b:tuple[int,int])->tuple[int,int]:
    start = min(a[0], b[0])
    end = max(a[1], b[1])
    return start, end

def overlaps(a: tuple[int,int], b:tuple[int,int])->bool:
    return (b[1] >= a[0] and b[0] <= a[1])

empty_line = datafile.index("")
s_ranges = datafile[:empty_line]

def parse_range(rng: str)->tuple[int, int]:
    a, b, *_ = map(int, rng.split('-'))
    return a, b

ranges = sorted(parse_range(r) for r in s_ranges)

final:list[tuple[int, int]] = []
current = ranges[0]
for range in ranges[1:]:
    if overlaps(current, range):
        current = merge_ranges(current, range)
    else:
        final.append(current)
        current = range
final.append(current)

tally = [b-a+1 for a, b in final]

print(sum(tally))
