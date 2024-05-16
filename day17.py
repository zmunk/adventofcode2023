import os
from itertools import chain
import time
from collections import defaultdict
from enum import Enum
from pathlib import Path

inf = float("inf")

cyan_bold = lambda s: f"\033[1;36m{s}\033[0m"
green_bold = lambda s: f"\033[1;32m{s}\033[0m"
red_bold = lambda s: f"\033[1;31m{s}\033[0m"


class Direction(Enum):
    RIGHT = ">"
    DOWN = "v"
    UP = "^"
    LEFT = "<"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


all_directions = {
    Direction.RIGHT,
    Direction.LEFT,
    Direction.UP,
    Direction.DOWN,
}


def opposite(dr):
    if dr == Direction.RIGHT:
        return Direction.LEFT
    elif dr == Direction.DOWN:
        return Direction.UP
    elif dr == Direction.UP:
        return Direction.DOWN
    elif dr == Direction.LEFT:
        return Direction.RIGHT
    else:
        raise NotImplementedError(dr)


def lateral(dr):
    if dr in [Direction.RIGHT, Direction.LEFT]:
        return [Direction.DOWN, Direction.UP]
    elif dr in [Direction.DOWN, Direction.UP]:
        return [Direction.RIGHT, Direction.LEFT]
    else:
        raise NotImplementedError(dr)


def add(block: tuple, dr: Direction):
    if dr == Direction.RIGHT:
        return (block[0], block[1] + 1)
    elif dr == Direction.DOWN:
        return (block[0] + 1, block[1])
    elif dr == Direction.UP:
        return (block[0] - 1, block[1])
    elif dr == Direction.LEFT:
        return (block[0], block[1] - 1)
    else:
        raise NotImplementedError(block, dr)


class Handler:
    def __init__(self, block_heats):
        self.block_heats = block_heats
        self._to_propagate = set()
        self.minimal_heat_inputs = defaultdict(
            lambda: defaultdict(lambda: [inf, inf, inf])
        )

    def update(self, block, dr, count, heat, verbose=0):
        """((1, 1), "v", 1, 4)"""
        if block[0] < 0 or block[1] < 0:
            return
        if heat >= self.minimal_heat_inputs[block][dr][count - 1]:
            if verbose > 0:
                print("  ", block, red_bold(heat))
            return
        self.minimal_heat_inputs[block][dr][count - 1] = heat
        if verbose > 0:
            print("  ", block, green_bold(heat))
        self._to_propagate.add(block)

    def to_propagate(self):
        arr = list(self._to_propagate)
        self._to_propagate = set()
        return arr

    def print(self):
        for block, value in dict(self.minimal_heat_inputs).items():
            print(f"{block}: ", end="")
            print(dict(value))

    def propagate(self, verbose=0):
        for block in self.to_propagate():
            if block not in self.block_heats:
                continue
            curr_heat = self.block_heats[block]
            if verbose > 0:
                print(f"{block} [{curr_heat}]")
            inputs = dict(self.minimal_heat_inputs[block])
            for dr, heats in inputs.items():
                ## same direction
                adj = add(block, dr)  # adjacent block
                if verbose > 0:
                    print(dr, adj)
                for count, heat in enumerate(heats[:2]):
                    if heat == inf:
                        continue
                    self.update(adj, dr, count + 2, heat + curr_heat, verbose)
                    if verbose > 0:
                        print(f"  x{count + 1}", heat + curr_heat)

                ## other two directions
                heat = min(self.minimal_heat_inputs[block][dr]) + curr_heat
                for odr in all_directions - {dr, opposite(dr)}:
                    adj = add(block, odr)
                    self.update(adj, odr, 1, heat, verbose)
        return len(self._to_propagate) > 0

    def display(self, inp):
        os.system("clear")
        for i, row in enumerate(inp.split("\n")[:40]):
            for j, h in enumerate(row):
                if (i, j) in self._to_propagate:
                    print(cyan_bold("#"), end="")
                else:
                    print(h, end="")
            print()
        time.sleep(0.1)


sample = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

inp = open(Path(__file__).resolve().stem + ".txt").read().strip()


def process(inp):
    block_heats = {}
    rows = inp.split("\n")
    n_rows = len(rows)
    n_cols = len(rows[0])
    for i, row in enumerate(rows):
        for j, h in enumerate(row):
            block_heats[(i, j)] = int(h)
    return block_heats, n_rows, n_cols


def part1(inp):
    block_heats, n_rows, n_cols = process(inp)
    handler = Handler(block_heats)

    handler.update((0, 1), Direction(">"), 1, 0)
    handler.update((1, 0), Direction("v"), 1, 0)

    while handler.propagate():
        pass
        # handler.display(inp)

    return block_heats[(n_rows - 1, n_cols - 1)] + min(
        chain.from_iterable(
            handler.minimal_heat_inputs[(n_rows - 1, n_cols - 1)].values()
        )
    )


class Handler2:
    def __init__(self, block_heats):
        self.block_heats = block_heats
        self._to_propagate = set()

        # excluding its own heat
        # (x, y) -> {"^": h, ...}
        self.min_heat = defaultdict(lambda: defaultdict(lambda: inf))

    def to_propagate(self):
        arr = list(self._to_propagate)
        self._to_propagate = set()
        return arr

    def update(self, block, directions, heat):
        for dr in directions:
            if heat < self.min_heat[block][dr]:
                self.min_heat[block][dr] = heat
                self._to_propagate.add(block)

    def propagate(self):
        for block in self.to_propagate():
            for dr, heat in self.min_heat[block].items():
                curr = block
                for i in range(10):
                    curr = add(curr, dr)
                    if curr not in self.block_heats:
                        break
                    heat += self.block_heats[curr]
                    if i < 3:
                        continue
                    self.update(curr, lateral(dr), heat)
        return len(self._to_propagate) > 0

    def display(self, inp):
        os.system("clear")
        for i, row in enumerate(inp.split("\n")[:40]):
            for j, h in enumerate(row):
                if (i, j) in self._to_propagate:
                    print(cyan_bold("#"), end="")
                else:
                    print(h, end="")
            print()
        time.sleep(0.1)


def part2(inp):
    block_heats, n_rows, n_cols = process(inp)
    handler = Handler2(block_heats)

    block = (0, 0)
    handler.update(block, [Direction.RIGHT, Direction.DOWN], 0)
    while handler.propagate():
        # handler.display(inp)
        pass
    return min(handler.min_heat[(n_rows - 1, n_cols - 1)].values())


print(part1(inp))
print(part2(inp))


print("---")
