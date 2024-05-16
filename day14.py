from pathlib import Path

sample = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

inp = open(Path(__file__).resolve().stem + ".txt").read().strip()


def tilt(
    axis_len1, axis_len2, round_rocks, cube_rocks, invert_coords=False, invert=False
):
    if invert_coords:
        round_rocks = {(j, i) for (i, j) in round_rocks}
        cube_rocks = {(j, i) for (i, j) in cube_rocks}
    round_updated = set()
    points = [axis_len1 if invert else -1] * axis_len2
    i_iter = range(axis_len1 - 1, -1, -1) if invert else range(axis_len1)
    for i in i_iter:
        for j in range(axis_len2):
            if (i, j) in round_rocks:
                points[j] += -1 if invert else 1
                round_updated.add((points[j], j))
            elif (i, j) in cube_rocks:
                points[j] = i
    if invert_coords:
        round_updated = {(j, i) for (i, j) in round_updated}
    return round_updated


def tilt_west(num_rows, num_cols, *args):
    return tilt(num_cols, num_rows, *args, invert_coords=True)


def tilt_north(*args):
    return tilt(*args)


def tilt_east(num_rows, num_cols, *args):
    return tilt(num_cols, num_rows, *args, invert_coords=True, invert=True)


def tilt_south(*args):
    return tilt(*args, invert=True)


def display(num_rows, num_cols, round_rocks, cube_rocks):
    for i in range(num_rows):
        for j in range(num_cols):
            if (i, j) in round_rocks:
                print("O", end="")
            elif (i, j) in cube_rocks:
                print("#", end="")
            else:
                print(".", end="")
        print()


def process(inp):
    round_rocks = set()
    cube_rocks = set()
    rows = inp.split("\n")
    num_rows = len(rows)
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            if c == "O":
                round_rocks.add((i, j))
            if c == "#":
                cube_rocks.add((i, j))
    return num_rows, len(rows[0]), round_rocks, cube_rocks


def part1(inp):
    num_rows, num_cols, round_rocks, cube_rocks = process(inp)
    round_rocks = tilt_north(num_rows, num_cols, round_rocks, cube_rocks)
    acc = 0
    for i, _ in round_rocks:
        acc += num_rows - i
    return acc


def iterate(round_rocks):
    round_rocks = tilt_north(num_rows, num_cols, round_rocks, cube_rocks)
    round_rocks = tilt_west(num_rows, num_cols, round_rocks, cube_rocks)
    round_rocks = tilt_south(num_rows, num_cols, round_rocks, cube_rocks)
    round_rocks = tilt_east(num_rows, num_cols, round_rocks, cube_rocks)
    return round_rocks


def part2(inp):
    global num_rows, num_cols, cube_rocks
    num_rows, num_cols, round_rocks, cube_rocks = process(inp)
    n = 1000000000
    seen = {}
    n_cycles = 0
    while True:
        round_rocks = iterate(round_rocks)
        n_cycles += 1
        t = tuple(sorted(round_rocks))
        if t in seen:
            cycle_len = n_cycles - seen[t]
            break
        seen[t] = n_cycles
    for _ in range((n - n_cycles) % cycle_len):
        round_rocks = iterate(round_rocks)
    acc = 0
    for i, _ in round_rocks:
        acc += num_rows - i
    return acc


print(part1(inp))
print(part2(inp))
