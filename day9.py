from pathlib import Path

sample = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".split(
    "\n"
)

inp = open(Path(__file__).resolve().stem + ".txt").read().splitlines()


def process(inp):
    res = []
    for line in inp:
        res.append([int(x) for x in line.split()])
    return res


def compute(line):
    next_val = 0
    last_vals = []
    first_vals = []
    while True:
        first_vals.append(line[0])
        last_vals.append(line[-1])
        next_val += line[-1]
        all_zero = True
        new_line = []
        for a, b in zip(line[:-1], line[1:]):
            diff = b - a
            new_line.append(diff)
            if diff != 0:
                all_zero = False
        if all_zero:
            break
        line = new_line
    return first_vals, last_vals


def part2(inp):
    inp = process(inp)
    acc = 0
    for line in inp:
        first_vals, _ = compute(line)
        sign = 1
        for val in first_vals:
            acc += sign * val
            sign *= -1
    return acc


def part1(inp):
    inp = process(inp)
    acc = 0
    for line in inp:
        _, last_vals = compute(line)
        acc += sum(last_vals)
    return acc


print(part2(inp))
print(part1(inp))
print("-")
