from pathlib import Path
from functools import lru_cache

sample = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".split(
    "\n"
)

inp = open(Path(__file__).resolve().stem + ".txt").read().strip().split("\n")


def process(inp):
    data = []
    for line in inp:
        conf, nums = line.split()
        nums = [int(x) for x in nums.split(",")]
        data.append((conf, nums))
    return data


def matches(to_check, pattern):
    assert len(to_check) == len(pattern)
    for c, p in zip(to_check, pattern):
        if c not in [p, "?"]:
            return False
    return True


@lru_cache
def num_arrangements_v2(conf, vals):
    """
    anything, [] -> 1
    "", vals>[] -> 0
    "#", [2] -> 0
    """
    if len(vals) == 0:
        if "#" in conf:
            return 0
        else:
            return 1
    if len(conf) == 0:
        return 0

    conf = "." + conf + "."
    val = vals[0]
    pattern = "." + "#" * val + "."

    # find first location that fits the pattern ".##." where any of the characters
    # can be "?" and the length of "#" corresponds to val (the first value in vals)
    start_index = 0

    count = 0
    while True:
        end_index = start_index + val + 2
        if end_index > len(conf):
            break
        to_check = conf[start_index:end_index]
        if matches(to_check, pattern):
            count += num_arrangements_v2(conf[end_index:-1], vals[1:])
        if to_check[1] == "#":
            break
        start_index += 1

    return count


@lru_cache
def num_arrangements(conf, vals):
    """
    anything, [] -> 1
    "", vals>[] -> 0
    "#", [2] -> 0
    """
    if len(vals) == 0:
        if "#" in conf:
            return []
        else:
            return ["." * len(conf)]
    if len(conf) == 0:
        return []

    conf = "." + conf + "."
    val = vals[0]
    pattern = "." + "#" * val + "."

    # find first location that fits the pattern ".##." where any of the characters
    # can be "?" and the length of "#" corresponds to val (the first value in vals)
    start_index = 0

    arr = []
    while True:
        end_index = start_index + val + 2
        if end_index > len(conf):
            break

        to_check = conf[start_index:end_index]
        if matches(to_check, pattern):
            sub_arr = num_arrangements(conf[end_index:-1], vals[1:])
            display_pattern = pattern
            if start_index == 0:
                display_pattern = display_pattern[1:]
            if end_index == len(conf):
                display_pattern = display_pattern[:-1]
            for s in sub_arr:
                arr.append("." * (start_index - 1) + display_pattern + s)
        if to_check[1] == "#":
            break
        start_index += 1

    return arr


def analyze(conf, vals):
    print(" " * 3, conf, vals)
    arr = num_arrangements(conf, vals)
    assert len(set(arr)) == len(arr)
    for i, s in enumerate(arr, start=1):
        num = f"{i})"
        print(f"{num: <3}", s)
    print()


def part2():
    """4443895258186"""
    # inp = sample
    acc = 0
    for conf, vals in process(inp):
        conf = "?".join([conf] * 5)
        vals = vals * 5
        n = num_arrangements_v2(conf, tuple(vals))
        acc += n
    return acc


def part1():
    # inp = sample
    acc = 0
    for conf, vals in process(inp):
        acc += len(num_arrangements(conf, tuple(vals)))
        # analyze(conf, vals)
    return acc


print(part1())
print(part2())
print("-")
