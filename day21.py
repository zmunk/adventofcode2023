inp = open("day21.txt").read().strip()
sample = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


def printg(rocks: set[tuple], positions: set[tuple], width=11, height=11):
    """
    rocks (#): {(1, 5), ...}
    positions (O): {(4, 5), ...}
    """
    for i in range(height):
        row = ""
        for j in range(width):
            if (i, j) in rocks:
                row += "#"
            elif (i, j) in positions:
                row += "O"
            else:
                row += "."
        print(row)


def process_input(inp) -> tuple[set, tuple[int, int] | None, tuple[int, int]]:
    rocks = set()
    start_pos = None
    rows = inp.split("\n")
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            if c == "#":
                rocks.add((i, j))
            elif c == "S":
                start_pos = (i, j)
    return rocks, start_pos, (len(rows), len(rows[0]))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def part1(inp):
    rocks, start_pos, _ = process_input(inp)
    positions = {start_pos}
    for _ in range(64):
        next_positions = set()
        for pos in positions:
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                cand = add(pos, d)
                if cand in rocks:
                    continue
                next_positions.add(cand)
        positions = next_positions
    return len(positions)


assert part1(inp) == 3671


def part2(inp):
    rocks, start_pos, (h, w) = process_input(inp)
    if start_pos is None:
        raise ValueError
    positions: set[tuple] = {start_pos}
    already_processed: list[set[tuple]] = [set(), set()]  # even, odd
    step_num = 0
    last_recorded = 0
    last_diff = 0
    last_diff_diff = 0
    diff, diff_diff = 0, 0
    a, b, c, offset = 0, 0, 0, 0
    x = 26501365
    p = 2 * h
    md = x % p
    while True:
        next_positions = set()
        for pos in positions:
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                cand = add(pos, d)
                if (cand[0] % h, cand[1] % w) in rocks:
                    continue
                if cand in already_processed[(step_num + 1) % 2]:
                    continue
                next_positions.add(cand)
        already_processed[step_num % 2] |= positions
        positions = next_positions
        step_num += 1

        if step_num % p == md:
            cnt = len(positions | already_processed[step_num % 2])
            diff = cnt - last_recorded
            diff_diff = diff - last_diff
            if diff_diff == last_diff_diff:
                offset = step_num // p
                a = cnt
                b = diff
                c = diff_diff
                break
            last_recorded = cnt
            last_diff = diff
            last_diff_diff = diff_diff
    i = x // p - offset
    return a + i * b + i * (i + 1) // 2 * c


print(part2(inp))
