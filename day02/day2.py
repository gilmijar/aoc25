file_name = 'sample.txt'
file_name = 'input.txt'

datafile = open(file_name, 'r', encoding='UTF-8').read().strip().split(',')

def parse(lines:list[str]) -> list[tuple[int, int]]:
    ranges = []
    for l in lines:
        x = map(int, l.split('-')[:2])
        ranges.append(tuple(x))
    return ranges

def detect_repeat(num:int) -> bool:
    s_num = str(num)
    half = len(s_num) // 2
    if half * 2 > len(s_num):
        return False
    return s_num[:half] == s_num[half:]

def sum_repeats(rng:tuple[int, int]) -> int:
    tally = 0
    for x in range(rng[0], rng[1]+1):
        if detect_repeat(x):
            tally += x
    return tally

data = parse(datafile)
print(sum(map(sum_repeats, data)))

