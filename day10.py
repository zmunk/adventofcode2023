from pathlib import Path
from copy import copy

sample = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

sample2 = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

sample3 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""


inp = open(Path(__file__).resolve().stem + ".txt").read()

white = lambda s: f"\033[1;37m{s}\033[0m"
cyan = lambda s: f"\033[1;36m{s}\033[0m"
red = lambda s: f"\033[1;31m{s}\033[0m"


def printg(*groups):
    """
    print grid (global)
    groups = [
        ([(0, 0)], cyan, "*"),
        ([(0, 1)], red, "X"),
    ]
    """
    for row, line in enumerate(grid.split()):
        for col, c in enumerate(line):
            for coords, color, char in groups:
                if (row, col) in coords:
                    if char is None:
                        print(color(c), end="")
                    else:
                        print(color(char), end="")
                    break
            else:
                print(c, end="")
        print()


def get_char(coords):
    return grid.split()[coords[0]][coords[1]]


def open_below(coords):
    return get_char(coords) in ["|", "F", "7"]


def open_above(coords):
    return get_char(coords) in ["|", "J", "L"]


def open_left(coords):
    return get_char(coords) in ["-", "J", "7"]


def open_right(coords):
    return get_char(coords) in ["-", "F", "L"]


def below(coords):
    return (coords[0] + 1, coords[1])


def above(coords):
    return (coords[0] - 1, coords[1])


def right(coords):
    return (coords[0], coords[1] + 1)


def left(coords):
    return (coords[0], coords[1] - 1)


def get_runners_v2(start):
    directions = []
    if open_above(below(start)):
        directions.append(DOWN)

    if open_below(above(start)):
        directions.append(UP)

    if open_left(right(start)):
        directions.append(RIGHT)

    if open_right(left(start)):
        directions.append(LEFT)

    assert len(directions) == 2
    return set(directions)


def get_runners(start):
    coords = []
    if open_above(below(start)):
        coords.append(below(start))

    if open_below(above(start)):
        coords.append(above(start))

    if open_left(right(start)):
        coords.append(right(start))

    if open_right(left(start)):
        coords.append(left(start))

    assert len(coords) == 2
    return coords


def get_directions(point):
    if isinstance(point, tuple):
        char = get_char(point)
    elif isinstance(point, str):
        char = point
    else:
        raise TypeError()

    if char == "S":
        directions = [UP, DOWN, LEFT, RIGHT]
    elif char == "L":
        directions = [UP, RIGHT]
    elif char == "F":
        directions = [RIGHT, DOWN]
    elif char == "7":
        directions = [LEFT, DOWN]
    elif char == "J":
        directions = [LEFT, UP]
    elif char == "|":
        directions = [UP, DOWN]
    elif char == "-":
        directions = [LEFT, RIGHT]
    else:
        raise ValueError()

    return directions


def get_next(curr, prev):
    char = get_char(curr)
    directions = get_directions(char)
    next_candidates = [move(curr, d) for d in directions]
    for nxt in next_candidates:
        if nxt != prev:
            return nxt
    raise ValueError()


direction_names = {
    (-1, 0): "up",
    (1, 0): "down",
    (0, -1): "left",
    (0, 1): "right",
}


class Direction:
    def __init__(self, y, x):
        self.name = direction_names[(y, x)]
        self.x = x
        self.y = y

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.y, self.x))

    def __invert__(self):
        return Direction(-self.y, -self.x)


UP = Direction(-1, 0)
DOWN = Direction(1, 0)
LEFT = Direction(0, -1)
RIGHT = Direction(0, 1)


def move(point, step):
    if isinstance(step, Direction):
        step = (step.y, step.x)
    return (point[0] + step[0], point[1] + step[1])


def get_start():
    for row, line in enumerate(grid.split()):
        for col, c in enumerate(line):
            if c == "S":
                return row, col
    raise ValueError()


def part1(inp):
    global grid
    grid = inp
    start = get_start()
    a, b = get_runners(start)
    prev_a = start
    prev_b = start
    a_coords = [a]
    b_coords = [b]

    steps = 1
    while a != b:
        steps += 1
        prev_a, a = a, get_next(a, prev_a)
        prev_b, b = b, get_next(b, prev_b)
        a_coords.append(a)
        b_coords.append(b)
    return steps


def replace_start(start):
    global grid
    directions = get_runners_v2(start)
    if directions == {DOWN, RIGHT}:
        char = "F"
    elif directions == {DOWN, LEFT}:
        char = "7"
    elif directions == {DOWN, UP}:
        char = "|"
    else:
        raise NotImplementedError(directions)
    arr = grid.split()
    line = arr[start[0]]
    arr[start[0]] = line[: start[1]] + char + line[start[1] + 1 :]
    grid = "\n".join(arr)


def get_adjacent(point) -> set[tuple[int, int]]:
    res = set()
    for d in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        adj = move(point, d)
        if 0 <= adj[0] < grid_height and 0 <= adj[1] < grid_width:
            res.add(adj)
    return res


def part2(inp):
    """
    pick point along the border and go inwards until you find one path point
    set that point's 'outside' as the direction from which you hit that path
    --> L means you hit it from the left, and since it's an L the bottom must be the
    same as the left, so the 'outside' of this point is (left, bottom)
    this means the character above it has an 'outside' of (left, ...)
    if it is '|' then (left)
    if 'F" then (left, top)
    if '7' then (left, bottom) OR ()
    then follow this all the way around and compile a list of all directly
    adjacent points to the path on the outside
    then propagate from there until you can't find any more adjacent points
    """
    global grid, grid_width, grid_height
    grid = inp
    grid_width = len(grid.split()[0])
    grid_height = len(grid.split())
    start = get_start()
    replace_start(start)
    curr, _ = get_runners(start)
    prev = start
    coords = [start, curr]
    while curr != start:
        prev, curr = curr, get_next(curr, prev)
        coords.append(curr)

    path = set(coords)

    def get_point_on_border(path):
        outside_candidates = (
            [((0, i), UP) for i in range(grid_width)]
            + [((i, 0), LEFT) for i in range(grid_height)]
            + [((grid_height - 1, i), DOWN) for i in range(grid_width)]
            + [((i, grid_width - 1), RIGHT) for i in range(grid_height)]
        )
        for point, outside_direction in outside_candidates:
            if point in path:
                return point, outside_direction
        raise ValueError("could not find a point in the path that touches the border")

    def get_outside_candidates(point, must_include):
        char = get_char(point)
        if char in ["F", "J"]:
            option_sets = [{UP, LEFT}, {DOWN, RIGHT}]
        elif char == "|":
            option_sets = [{LEFT}, {RIGHT}]
        elif char in ["L", "7"]:
            option_sets = [{DOWN, LEFT}, {UP, RIGHT}]
        elif char == "-":
            option_sets = [{UP}, {DOWN}]
        else:
            raise ValueError(f"invalid character: {char}")
        for oset in option_sets:
            if must_include in oset:
                return oset
        raise ValueError()

    def get_first_layer(curr, mv, outside):
        outside_points = set()
        while curr != end_point:
            curr = move(curr, mv)
            tracking.append(curr)
            outside = next(iter(set(outside) - {~mv, mv}))
            outside = get_outside_candidates(curr, outside)

            mv_options = set(get_directions(curr)) - {~mv}
            mv = next(iter(mv_options))
            for d in outside:
                outside_points.add(move(curr, d))
        return outside_points

    start_point, outside_direction = get_point_on_border(path)
    curr = start_point
    tracking = [start_point]
    outside = set(get_outside_candidates(start_point, outside_direction))
    movement_directions = get_directions(start_point)

    end_point = move(start_point, movement_directions[0])
    mv = movement_directions[1]

    outside_points = get_first_layer(curr, mv, outside)
    last_layer = outside_points - path

    outside = set() | last_layer
    while True:
        next_layer = set()
        for point in last_layer:
            next_layer |= get_adjacent(point) - outside - path
        outside_count = len(outside)
        outside |= next_layer
        if len(outside) == outside_count:
            break
        last_layer = next_layer
    for point in copy(outside):
        if 0 <= point[0] < grid_height and 0 <= point[1] < grid_width:
            pass
        else:
            outside.remove(point)
    return grid_width * grid_height - len(path) - len(outside)


assert part1(inp) == 6923
assert part2(inp) == 529
print("-")
