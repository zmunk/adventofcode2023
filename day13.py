from pathlib import Path

sample = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

inp = open(Path(__file__).resolve().stem + ".txt").read().strip()


def process(inp):
    grids = []
    for grid in inp.split("\n\n"):
        grids.append([])
        for row in grid.split("\n"):
            grids[-1].append(row)
    return grids


def get_columns(grid):
    cols = [c for c in grid[0]]
    for row in grid[1:]:
        for i, c in enumerate(row):
            cols[i] += c
    return cols


def diff(a, b):
    acc = 0
    for c1, c2 in zip(a, b):
        if c1 != c2:
            acc += 1
    return acc


from copy import copy


def get_reflection_v2(grid):
    candidates = {}
    seen = []
    for i, row in enumerate(grid):
        for c in copy(list(candidates.keys())):
            j = 2 * c - 1 - i
            if j < 0 and candidates[c] == 1:
                return c
            candidates[c] += diff(row, grid[j])
            if candidates[c] > 1:
                del candidates[c]
        if len(seen) > 0 and (d := diff(row, seen[-1])) <= 1:
            candidates[i] = d
        seen.append(row)
    for c, d in candidates.items():
        if d == 1:
            return c
    return None


def get_reflection(grid):
    candidates = []
    seen = []
    for i, row in enumerate(grid):
        for c in candidates:
            j = 2 * c - 1 - i
            if j < 0:
                return c
            if grid[j] != row:
                candidates.remove(c)
        if len(seen) > 0 and row == seen[-1]:
            candidates.append(i)
        seen.append(row)
    if len(candidates) == 0:
        return None
    elif len(candidates) == 1:
        return candidates[0]
    else:
        for i, row in enumerate(grid):
            print(f"{i}) {row}")
        raise ValueError(f"{candidates = }")


def display(rows, cols):
    for i, row in enumerate(rows):
        print(f"{i}) {row}")
    print()
    for i, col in enumerate(cols):
        print(f"{i}) {col}")


def part2():
    grids = process(inp)
    acc = 0
    for rows in grids:
        row_ref = get_reflection_v2(rows)
        if row_ref is not None:
            acc += 100 * row_ref
        else:
            cols = get_columns(rows)
            col_ref = get_reflection_v2(cols)
            if col_ref is None:
                display(rows, cols)
                raise ValueError()
            acc += col_ref
    return acc


def part1():
    grids = process(inp)
    acc = 0
    for rows in grids:
        row_ref = get_reflection(rows)
        if row_ref is not None:
            acc += 100 * row_ref
        else:
            cols = get_columns(rows)
            col_ref = get_reflection(cols)
            if col_ref is None:
                raise ValueError()
            acc += col_ref
    return acc


print(part2())
print("-")
