import re

sample1 = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""".split()

sample2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""".split()

inp = open("day1.txt").read().splitlines()

def part1(inp):
    acc = 0
    for line in inp:
        digits = re.sub(r'\D', '', line)
        acc += int(digits[0] + digits[-1])
    return acc

def part2(inp):

    nums = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }

    acc = 0
    for line in inp:

        # find first digit
        first = None
        for i, c in enumerate(line):
            try:
                first = int(c)
                break
            except ValueError:
                pass

            for l in [3, 4, 5]:
                w = line[i : i + l]
                if w in nums:
                    first = nums[w]
                    break
            if first is not None:
                break

            i += 1

        if first is None:
            raise ValueError("")

        # find last digit
        last = None
        i = len(line) - 1
        for i, c in reversed(list(enumerate(line))):
            try:
                last = int(c)
                break
            except ValueError:
                pass

            for l in [3, 4, 5]:
                w = line[i + 1 - l : i + 1]
                if w in nums:
                    last = nums[w]
                    break
            if last is not None:
                break

            i -= 1

        if last is None:
            raise ValueError("")

        acc += int(str(first) + str(last))
    return acc

print(part1(inp))
print(part2(inp))
