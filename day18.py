import re
from pathlib import Path
from typing import Iterable

sample = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

inp = open(Path(__file__).resolve().stem + ".txt").read().strip()


def process(inp, version="v1") -> Iterable[tuple[int, int]]:
    for row in inp.split("\n"):
        m = re.match(r"(.) (\d+) \(#(.*)\)", row)
        if m is None:
            raise ValueError()
        groups = list(m.groups())
        if version == "v1":
            yield get_deltas(groups[0], int(groups[1]))
        elif version == "v2":
            yield get_deltas("RDLU"[int(groups[2][5])], int(groups[2][:5], 16))


def calculate_area(gen):
    x = 0
    area = 1
    for dx, dy in gen:
        x += dx
        if dy > 0:
            area += dy * (x + 1)
        elif dy < 0:
            area += dy * x
        elif dx > 0:
            area += dx
    return area


def get_deltas(d, c):
    """get_deltas(direction, count)"""
    dx, dy = 0, 0
    if d == "R":
        dx = c
    elif d == "L":
        dx = -c
    elif d == "D":
        dy = c
    elif d == "U":
        dy = -c
    else:
        raise ValueError("")
    return dx, dy


def part1(inp):
    return calculate_area(process(inp))


def part2(inp):
    return calculate_area(process(inp, version="v2"))


print(part1(inp))
print(part2(inp))
print("-")
