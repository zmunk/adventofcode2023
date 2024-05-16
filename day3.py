from collections import defaultdict

sample = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".split("\n")

inp = open("day3.txt").read().splitlines()

def get_adjacencies(row, start_col, end_col):
    res = []
    for r in [row - 1, row + 1]:
        for i in range(max(0, start_col - 1), end_col + 2):
            res.append((r, i))
    for i in [start_col - 1, end_col + 1]:
        res.append((row, i))
    return res

def check_adjacent(row, start_col, end_col, symbols):
    for r in [row - 1, row + 1]:
        for i in range(start_col - 1, end_col + 2):
            if (r, i) in symbols:
                return True
    for i in [start_col - 1, end_col + 1]:
        if (row, i) in symbols:
            return True
    return False

def process(inp):
    row = 0
    line = inp[row]
    nums = []
    symbols = set()
    gears = set()
    for row, line in enumerate(inp):
        num = ""
        start = None
        for i, c in enumerate(list(line) + [None]):
            if c in list("0123456789"):
                if num == "":
                    start = i
                num += c
                continue
            elif num != "":
                nums.append((int(num), row, start, i - 1))

            if c is None:
                break

            if c != ".":
                symbols.add((row, i))
            if c == "*":
                gears.add((row, i))

            num = ""

    return nums, symbols, gears

def part1(inp):
    nums, symbols, _ = process(inp)
    acc = 0
    for num, row, start_col, end_col in nums:
        if check_adjacent(row, start_col, end_col, symbols):
            acc += num
    return acc


def part2(inp):
    nums, _, gears = process(inp)
    gear_nums = defaultdict(list)
    for num, row, start_col, end_col in nums:
        for adj in get_adjacencies(row, start_col, end_col):
            if adj in gears:
                gear_nums[adj].append(num)
                break
    acc = 0
    for val in gear_nums.values():
        if len(val) == 2:
            acc += val[0] * val[1]
    return acc

print(part1(inp))
print(part2(inp))
print('-')
