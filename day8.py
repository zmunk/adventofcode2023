from math import lcm
import re
from pathlib import Path
from itertools import repeat, cycle
from pprint import pprint

sample = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""".split(
    "\n"
)
sample2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""".split(
    "\n"
)

sample3 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".split(
    "\n"
)

inp = open(Path(__file__).resolve().stem + ".txt").read().splitlines()


def get_count(links, start_node, directions):
    count = 0
    node = start_node
    for d in cycle(directions):
        if node.endswith("Z"):
            break
        count += 1

        j = 0 if d == "L" else 1
        node = links[node][j]
    return count


def part2(inp):
    directions, links = process(inp)
    curr_nodes = list(filter(lambda x: x.endswith("A"), links.keys()))

    counts = []
    for node in curr_nodes:
        counts.append(get_count(links, node, directions))
    return lcm(*counts)


def process(inp):
    directions = inp[0]
    links_raw = inp[2:]
    links = {}
    for line in links_raw:
        start, left, right = re.match(r"(.*) = \((.*), (.*)\)", line).groups()
        links[start] = (left, right)
    return directions, links


def part1(inp):
    directions, links = process(inp)

    node = "AAA"
    directions = cycle(directions)
    count = 0
    while node != "ZZZ":
        count += 1
        if next(directions) == "L":
            node = links[node][0]
        else:
            node = links[node][1]
    return count


assert part1(inp) == 15989
print(part2(inp))
print("-")
