from collections import defaultdict
from queue import Queue
from copy import copy
from utils import get_match
from string import ascii_uppercase

inp = open("day22.txt").read().strip()
sample = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""


def get_blocks(start, end):
    if start == end:
        i = None
    for i in range(3):
        if start[i] != end[i]:
            break
    else:
        yield start
        return
    for j in range(min(start[i], end[i]), max(start[i], end[i]) + 1):
        cp = list(start)
        if i is not None:
            cp[i] = j
        yield tuple(cp)


def get_blocks_wrapper(line):
    start, end = get_match(r"(.*)~(.*)", line)
    start = tuple(map(int, start.split(",")))
    end = tuple(map(int, end.split(",")))

    yield from get_blocks(start, end)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def lower(c, locations, blocks, xyz):
    """drop block by as much as it can go"""
    lowered_locations = []
    for block in locations:
        lowered_locations.append(add(block, (0, 0, -1)))

    for loc in lowered_locations:
        if loc in xyz and c != xyz[loc] or loc[-1] == 0:
            return None

    lowered_lowered_locations = lower(c, lowered_locations, blocks, xyz)
    if lowered_lowered_locations is not None:
        return lowered_lowered_locations

    return lowered_locations


def print_(xyz):
    max_x = 0
    xz = {}
    for (x, y, z), c in xyz.items():
        max_x = max(max_x, x)
        if (x, z) in xz and c != xz[(x, z)]:
            xz[(x, z)] = "?"
        else:
            xz[(x, z)] = c

    max_y = 0
    max_z = 0
    yz = {}
    for (x, y, z), c in xyz.items():
        max_y = max(max_y, y)
        max_z = max(max_z, z)
        if (y, z) in yz and c != yz[(y, z)]:
            yz[(y, z)] = "?"
        else:
            yz[(y, z)] = c

    for dim, dz, max_d in [
        ("x", xz, max_x),
        ("y", yz, max_y),
    ]:
        print(f" {dim} ")
        print("".join(map(str, range(max_d))))
        for z in range(max_z, 0, -1):
            for d in range(max_d):
                if (d, z) in dz:
                    print(dz[(d, z)], end="")
                else:
                    print(".", end="")
            print(f" {z}", end="")
            if z == (9 + 1) // 2:
                print(" z", end="")
            print()
        print("--- 0")


# inp = sample

blocks = defaultdict(list)
xyz = {}
for c, line in enumerate(inp.split("\n")):
    for block in get_blocks_wrapper(line):
        xyz[block] = c
        blocks[c].append(block)

while True:
    no_blocks_updated = True
    xyz_updated = {}
    blocks_updated = defaultdict(list)
    for c in blocks:
        lowered = lower(c, blocks[c], blocks, xyz)
        if lowered is not None:
            new = lowered
            no_blocks_updated = False
        else:
            new = blocks[c]
        for block in new:
            xyz_updated[block] = c
            blocks_updated[c].append(block)
    xyz = xyz_updated
    blocks = blocks_updated
    if no_blocks_updated:
        break


candidates = set(blocks.keys())

directly_below = {}

to_discard = set()
for c in blocks:
    blocks_below = set()
    lowered_locations = []
    for block in blocks[c]:
        lowered_locations.append(add(block, (0, 0, -1)))
    for loc in lowered_locations:
        if loc in xyz and c != xyz[loc]:
            blocks_below.add(xyz[loc])
    directly_below[c] = blocks_below
    if len(blocks_below) == 1:
        to_discard.add(next(iter(blocks_below)))

print("part 1", len(candidates - to_discard))

directly_above = {c: set() for c in directly_below}
for c, blocks_below in directly_below.items():
    for b in blocks_below:
        directly_above[b].add(c)

to_process = Queue()

for c, above in directly_above.items():
    if len(above) == 0:
        to_process.put(c)

full_support = defaultdict(set)
fragmented_support = defaultdict(set)

process_order = []
processed = set()
while not to_process.empty():
    curr = to_process.get()
    if curr in processed:
        continue
    process_order.append(curr)
    processed.add(curr)

    below = directly_below[curr]
    if len(below) == 1:
        supporter = list(below)[0]
        full_support[supporter].add(curr)
    else:
        for item in below:
            fragmented_support[item].add(curr)

    for item in below:
        to_process.put(item)

for curr in process_order:
    while True:
        full_support_before = copy(full_support[curr])
        fragmented_support_before = copy(fragmented_support[curr])

        for item in full_support_before:
            full_support[curr] |= full_support[item]
            fragmented_support[curr] |= fragmented_support[item]

        for frag in copy(fragmented_support[curr]):
            if not directly_below[frag].issubset(full_support[curr]):
                continue
            fragmented_support[curr].remove(frag)
            full_support[curr].add(frag)

        if (
            full_support_before == full_support[curr]
            and fragmented_support_before == fragmented_support[curr]
        ):
            break


acc = 0
for k, v in full_support.items():
    acc += len(v)

print("part 1", acc)
print("-")
