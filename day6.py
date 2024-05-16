import math
import re


def get_strats(t, d):
    det = t * t - 4 * d
    s1 = math.ceil((t + math.sqrt(det)) / 2) - 1
    s2 = math.floor((t - math.sqrt(det)) / 2) + 1
    return s1 - s2 + 1


assert get_strats(7, 9) == 4
assert get_strats(15, 40) == 8
assert get_strats(30, 200) == 9

sample = """\
Time:      7  15   30
Distance:  9  40  200""".split(
    "\n"
)

inp = """\
Time:        40     70     98     79
Distance:   215   1051   2147   1005""".split(
    "\n"
)


def part2():
    time = int(re.match(r"Time: *(.*)", inp[0]).groups()[0].replace(" ", ""))
    distance = int(re.match(r"Distance: *(.*)", inp[1]).groups()[0].replace(" ", ""))
    return get_strats(time, distance)


def part1():
    time = [int(x) for x in re.match(r"Time: *(.*)", inp[0]).groups()[0].split()]
    distance = [
        int(x) for x in re.match(r"Distance: *(.*)", inp[1]).groups()[0].split()
    ]

    res = 1
    for t, d in zip(time, distance):
        res *= get_strats(t, d)
    return res


part2()
print("-")
