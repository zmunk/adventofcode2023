from utils import get_match
from collections import defaultdict
from queue import Queue
import random
from copy import deepcopy

inp = open("day25.txt").read().strip()
sample = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""


def get_connections(inp: str) -> dict[str, set]:
    connections = defaultdict(set)

    for line in inp.split("\n"):
        node, conns = get_match(r"(.*): (.*)", line)
        conns = conns.split(" ")

        for other_node in conns:
            connections[node].add(other_node)
            connections[other_node].add(node)

    return connections


def get_clusters(a, b, connections):
    initial_clusters = [a, b]
    processed = set()
    clusters = [set(), set()]
    q = [Queue(), Queue()]

    for i in [0, 1]:
        for c in sorted(initial_clusters[i]):
            q[i].put(c)

    transfer_candidates = set()
    i = 1
    while True:
        i, j = (i + 1) % 2, i
        if q[i].empty():
            if q[j].empty():
                break
            continue
        node = q[i].get()

        if node in clusters[j]:
            transfer_candidates.add((node, i))
            continue

        clusters[i].add(node)

        if node in processed:
            continue

        for neighbor in sorted(connections[node]):
            q[i].put(neighbor)

        processed.add(node)
    return clusters, sorted(transfer_candidates)


def optimize_clusters(init, transfer_candidates, connections):
    for cand, d in transfer_candidates:
        links = connections[cand]
        if len(init[d] & links) > len(init[(d + 1) % 2] & links):
            yield cand, d


def part1(inp):
    connections: dict[str, set] = get_connections(inp)
    while True:
        a, b = random.sample(list(connections), 2)
        clusters, transfer_candidates = get_clusters({a}, {b}, connections)
        while True:
            transfer_gen = optimize_clusters(clusters, transfer_candidates, connections)
            empty = True
            last_value = None
            init = deepcopy(clusters)
            for cand, d in transfer_gen:
                empty = False
                init[d].add(cand)
                init[(d + 1) % 2].remove(cand)
                clusters, transfer_candidates = get_clusters(
                    init[0], init[1], connections
                )
                if len(transfer_candidates) == 6:
                    return len(clusters[0]) * len(clusters[1])
                if len(transfer_candidates) == last_value:
                    empty = True
                    break
                last_value = len(transfer_candidates)
            if empty:
                break


print(part1(inp))
print("-")
