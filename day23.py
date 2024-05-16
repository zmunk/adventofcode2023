from copy import copy
from queue import Queue
from collections import defaultdict

inp = open("day23.txt").read().strip()
sample = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

from enum import Enum


direction_str_mapping = {
    (0, 1): ">",
    (-1, 0): "^",
    (0, -1): "<",
    (1, 0): "v",
}


class Direction(Enum):
    RIGHT = (0, 1)
    UP = (-1, 0)
    LEFT = (0, -1)
    DOWN = (1, 0)

    def __repr__(self):
        return direction_str_mapping[self._value_]

    def move(self, pos: tuple[int, int]):
        return (pos[0] + self.value[0], pos[1] + self.value[1])


DIRECTIONS = [Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN]


def surroundings(i, j):
    for d in DIRECTIONS:
        yield (i + d.value[0], j + d.value[1], d)


class NoOptionsException(Exception):
    def __init__(self, foo):
        self.foo = foo


def walk_back_until_fork(
    path, start, step_dir: Direction, grid, seen: set, ignore_slopes=False
):
    """
    params: (tuple)
     - number of steps (int)
     - start position: tuple (row, col)
     - first step direction (<, v, >, ^)
    return: path, n_steps, fork position, step directions (list)
    """
    last_pos = start
    i, j = start[0] + step_dir.value[0], start[1] + step_dir.value[1]
    path = copy(path)
    seen = copy(seen)
    path.append(step_dir)
    seen.add(start)

    while True:
        options = []
        for ii, jj, d in surroundings(i, j):
            try:
                tile = grid[ii][jj]
            except IndexError:
                continue
            if tile == "#":
                continue
            if (ii, jj) == last_pos:
                continue

            if not ignore_slopes:
                hit_slope = False
                for k, v in direction_str_mapping.items():
                    if d.value == k and tile == v:
                        hit_slope = True
                        break
                if hit_slope:
                    continue

            if (ii, jj) in seen:
                continue

            options.append((ii, jj, d))
        if len(options) > 1 or len(options) == 0:
            return path, seen, (i, j), list(map(lambda o: o[2], options))

        last_pos = (i, j)
        i, j, d = options[0]
        path.append(d)
        seen.add((i, j))


def show_path(start, path, grid):
    footsteps = {start}
    pos = start
    for d in path:
        pos = (pos[0] + d.value[0], pos[1] + d.value[1])
        footsteps.add(pos)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if (i, j) in footsteps:
                print("o", end="")
            else:
                print(c, end="")
        print()


def part1():
    branches = Queue()
    branches.put(([], DESTINATION, Direction.UP, set()))

    mx = 0
    while not branches.empty():
        path, start, step_dir, seen = branches.get()
        path, seen, start, options = walk_back_until_fork(
            path,
            start,
            step_dir,
            grid,
            seen,
        )

        if start == GRID_START:
            mx = max(mx, len(path))
        else:
            for step_dir in options:
                branches.put((path, start, step_dir, seen))

    return mx


def movable_positions(grid, pos, last_pos) -> list[Direction]:
    positions = []
    for d in DIRECTIONS:
        (i, j) = d.move(pos)
        if (i, j) == last_pos:
            continue
        try:
            tile = grid[i][j]
        except IndexError:
            continue
        if tile == "#":
            continue
        positions.append(d)
    return positions


def find_fork(start, step_dir: Direction, grid):
    last_pos = start
    pos = step_dir.move(start)
    n_steps = 1

    while True:
        options = movable_positions(grid, pos, last_pos)
        if len(options) > 1:
            return n_steps, pos, options
        if len(options) == 0:
            if pos == DESTINATION:
                return n_steps, pos, []
            else:
                raise ValueError(f"{pos = }")
        last_pos, pos = pos, options[0].move(pos)
        n_steps += 1


def part2():
    n_steps, pos, options = find_fork(GRID_START, Direction.DOWN, grid)

    links = defaultdict(dict)
    links[GRID_START][pos] = n_steps
    links[pos][GRID_START] = n_steps

    to_process = Queue()
    processed_nodes = set()

    to_process.put((pos, options))
    processed_nodes.add(pos)

    while not to_process.empty():
        node, step_dirs = to_process.get()
        for step_dir in step_dirs:
            n_steps, new_pos, options = find_fork(node, step_dir, grid)
            links[node][new_pos] = n_steps
            links[new_pos][node] = n_steps
            if new_pos not in processed_nodes:
                to_process.put((new_pos, options))
                processed_nodes.add(new_pos)

    paths = Queue()
    paths.put((0, GRID_START, set()))

    max_dist = 0
    while not paths.empty():
        dist, node, seen = paths.get()
        if DESTINATION in links[node]:
            total_dist = dist + links[node][DESTINATION]
            if total_dist > max_dist:
                max_dist = total_dist
            continue
        for other_node, new_dist in links[node].items():
            if other_node in seen:
                continue
            paths.put((dist + new_dist, other_node, seen | {node}))

    return max_dist


# global DESTINATION

inp = sample
GRID_START = (0, 1)
grid = inp.split("\n")
DESTINATION = (len(grid) - 1, grid[-1].index("."))

print("part 1", part1())
print("part 2", part2())
# print("part 2", part2(inp))
print("-")
