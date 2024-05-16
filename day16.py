from collections import defaultdict
from pathlib import Path

sample = """\
.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""

inp = open(Path(__file__).resolve().stem + ".txt").read().strip()

RIGHT = (0, 1)
UP = (-1, 0)
LEFT = (0, -1)
DOWN = (1, 0)


class Beam:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction: tuple = direction

    def __repr__(self):
        r = f"{self.pos} "
        if self.direction == RIGHT:
            r += ">"
        elif self.direction == DOWN:
            r += "v"
        elif self.direction == LEFT:
            r += "<"
        elif self.direction == UP:
            r += "^"
        else:
            raise ValueError(self.direction)
        return r

    def step(self):
        self.pos = (
            self.pos[0] + self.direction[0],
            self.pos[1] + self.direction[1],
        )

    def out_of_bounds(self):
        if (
            self.pos[0] < 0
            or self.pos[1] < 0
            or self.pos[0] >= num_rows
            or self.pos[1] >= num_cols
        ):
            return True
        else:
            return False


def print_grid(mirrors):
    for i in range(num_rows):
        for j in range(num_cols):
            if (i, j) in energized:
                print("#", end="")
            elif (i, j) in mirrors:
                print(mirrors[(i, j)], end="")
            else:
                print(".", end="")
        print()


def process(inp):
    global num_rows, num_cols
    rows = inp.split("\n")
    num_cols = len(rows[0])
    num_rows = len(rows)
    mirrors = {}
    for i, line in enumerate(rows):
        for j, c in enumerate(line):
            if c in ["|", "-", "/", "\\"]:
                mirrors[(i, j)] = c
    return mirrors


def part1(inp, start=(0, 0), start_direction=RIGHT):
    global energized
    mirror_seen = defaultdict(set)
    mirrors = process(inp)

    energized = set()

    beams = [Beam(start, start_direction)]
    while len(beams) > 0:
        to_remove = []
        new_beams = defaultdict(list)
        for beam in beams:
            if beam.out_of_bounds():
                to_remove.append(beam)
                continue

            energized.add(beam.pos)

            if beam.pos in mirrors:
                pos = beam.pos
                mirror = mirrors[pos]
                if mirror == "|":
                    if beam.direction in [RIGHT, LEFT]:
                        new_beams[pos].extend([UP, DOWN])
                        to_remove.append(beam)
                    else:
                        pass
                elif mirror == "-":
                    if beam.direction in [DOWN, UP]:
                        new_beams[pos].extend([LEFT, RIGHT])
                        to_remove.append(beam)
                    else:
                        pass
                elif mirror == "/":
                    if beam.direction == RIGHT:
                        new_beams[pos].append(UP)
                    elif beam.direction == UP:
                        new_beams[pos].append(RIGHT)
                    elif beam.direction == DOWN:
                        new_beams[pos].append(LEFT)
                    elif beam.direction == LEFT:
                        new_beams[pos].append(DOWN)
                    else:
                        raise NotImplementedError(f"{mirror} {beam.direction}")
                    to_remove.append(beam)
                elif mirror == "\\":
                    if beam.direction == RIGHT:
                        new_beams[pos].append(DOWN)
                    elif beam.direction == UP:
                        new_beams[pos].append(LEFT)
                    elif beam.direction == LEFT:
                        new_beams[pos].append(UP)
                    elif beam.direction == DOWN:
                        new_beams[pos].append(RIGHT)
                    else:
                        raise NotImplementedError(f"{mirror} {beam.direction}")
                    to_remove.append(beam)
                else:
                    raise ValueError(
                        f"invalid mirror: {mirror}, {beam.direction}, {beam.pos}"
                    )

        for beam in to_remove:
            beams.remove(beam)

        for pos, directions in new_beams.items():
            for d in directions:
                if d in mirror_seen[pos]:
                    continue
                beams.append(Beam(pos, d))
                mirror_seen[pos].add(d)

        for beam in beams:
            beam.step()

    num_energized = len(energized)
    del energized
    return num_energized


def part2(inp):
    process(inp)
    max_ = 0
    for pos, direction in (
        [((i, 0), RIGHT) for i in range(num_rows)]
        + [((i, num_cols - 1), LEFT) for i in range(num_rows)]
        + [((0, j), DOWN) for j in range(num_cols)]
        + [((num_rows - 1, j), UP) for j in range(num_cols)]
    ):
        m = part1(inp, start=pos, start_direction=direction)
        max_ = max(max_, m)
    return max_


print(part1(inp))
print(part2(inp))
print("-")
