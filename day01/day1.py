file_name = 'sample.txt'
file_name = 'input.txt'

datafile = open(file_name, 'r', encoding='UTF-8').read().strip().splitlines()

DIAL = 100

def parse(lines:list[str]) -> list[int]:
    return [ (-1 if line.startswith('L') else 1 ) * int(line[1:]) for line in lines ]

def land_on_zero(commands:list[int]) -> list[int]:
    pos = 50
    all_pos = [pos]
    for cmd in commands:
        pos = (pos + cmd) % DIAL
        all_pos.append(pos)
    return all_pos

print(land_on_zero(parse(datafile)).count(0))

# PART 2

def zero_cosses(commands:list[int]) -> int:
    pos = 50
    zeros = 0
    for cmd in commands:
        x = pos + cmd
        y, pos = divmod(x, DIAL)
        passes = abs(y)
        if cmd < 0:
            if x == cmd:
                passes -= 1
            if pos == 0:
                passes += 1
        # print(cmd, pos, passes)
        zeros += passes
    return zeros

print(
    zero_cosses(parse(datafile))
)
