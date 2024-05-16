from pathlib import Path
from pprint import pprint

sample = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

inp = open(Path(__file__).resolve().stem + ".txt").read()


def get_expansion(vals, max_val, expansion_increment=2):
    expansion_constant = 0
    expansion = {}
    for val in range(max_val):
        if val in vals:
            expansion[val] = val + expansion_constant
        else:
            expansion_constant += expansion_increment - 1
    return expansion


def process(inp):
    galaxies = []
    for row, line in enumerate(inp.split()):
        for col, c in enumerate(line):
            if c == "#":
                galaxies.append((row, col))
    return galaxies


def part2(inp, exp):
    galaxies = process(inp)
    g_rows = set(x[0] for x in galaxies)
    g_cols = set(x[1] for x in galaxies)
    grid_width = len(inp.split()[0])
    grid_height = len(inp.split())

    vertical_expansion = get_expansion(
        g_rows, grid_height, expansion_increment=int(exp)
    )
    horizontal_expansion = get_expansion(
        g_cols, grid_width, expansion_increment=int(exp)
    )
    new_galaxies = []
    for row, col in galaxies:
        new_galaxies.append((vertical_expansion[row], horizontal_expansion[col]))
    galaxies = new_galaxies

    acc = 0
    for i, g in enumerate(galaxies):
        for h in galaxies[i + 1 :]:
            acc += abs(g[0] - h[0]) + abs(g[1] - h[1])
    return acc


def part1(inp):
    galaxies = process(inp)
    g_rows = set(x[0] for x in galaxies)
    g_cols = set(x[1] for x in galaxies)

    grid_width = len(inp.split()[0])
    grid_height = len(inp.split())

    vertical_expansion = get_expansion(g_rows, grid_height)
    horizontal_expansion = get_expansion(g_cols, grid_width)

    new_galaxies = []
    for row, col in galaxies:
        new_galaxies.append((vertical_expansion[row], horizontal_expansion[col]))
    galaxies = new_galaxies

    acc = 0
    for i, g in enumerate(galaxies):
        for h in galaxies[i + 1 :]:
            acc += abs(g[0] - h[0]) + abs(g[1] - h[1])
    return acc


assert part1(inp) == 10490062
print(part2(inp, 1e6))

print("-")
