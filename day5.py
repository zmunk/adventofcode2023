sample = """\
seeds: 79 14 55 13

seed-to-soil map:
    50 98 2
52 50 48

soil-to-fertilizer map:
    0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
    49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
    88 18 7
18 25 70

light-to-temperature map:
    45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
    0 69 1
1 0 69

humidity-to-location map:
    60 56 37
56 93 4""".split(
    "\n"
)

from copy import copy, deepcopy
from pprint import pprint
import re
from pathlib import Path

inp = open(Path(__file__).resolve().stem + ".txt").read().splitlines()


def process(inp):
    inp = iter(inp)

    seeds = re.match(r"seeds: (.*)", next(inp)).groups()[0].split()
    seeds = [int(n) for n in seeds]

    next(inp)

    mappings = []
    for i in range(7):
        next(inp)
        mappings.append([])
        line = next(inp)
        while line != "":
            mappings[i].append([int(n) for n in line.split()])
            try:
                line = next(inp)
            except StopIteration:
                break
    return seeds, mappings


def cross(prev_segment, diff, curr_field):
    """
    prev_segment: (1, 69)
    diff: 1
    curr_field: {(56, 92): 4, (93, 96): -37}

    output:
      - updated_curr_field {(70, 92): 4, (93, 96): -37}
      - new_field_segments {(0, 54): 1, (55, 68): 5}
    """
    field = deepcopy(curr_field)
    unchecked = [(*prev_segment, diff)]
    new_field_segments = {}
    while len(unchecked) > 0:
        seg_start, seg_end, diff = unchecked.pop()
        for (ref_start, ref_end), ref_diff in field.items():
            intersect_start = max(seg_start, ref_start)
            intersect_end = min(seg_end, ref_end)

            ## no intersection
            if intersect_start > intersect_end:
                continue

            ## intersection
            new_field_segments[(intersect_start - diff, intersect_end - diff)] = (
                diff + ref_diff
            )
            if seg_start < intersect_start:
                unchecked.append((seg_start, intersect_start - 1, diff))
            if seg_end > intersect_end:
                unchecked.append((intersect_end + 1, seg_end, diff))
            del field[(ref_start, ref_end)]
            if ref_start < intersect_start:
                field[(ref_start, intersect_start - 1)] = ref_diff
            if ref_end > intersect_end:
                field[(intersect_end + 1, ref_end)] = ref_diff

            break

        else:
            ## field doesn't contain segment at all
            new_field_segments[(seg_start - diff, seg_end - diff)] = diff

    return field, new_field_segments


def step(pair, delta):
    return (pair[0] + delta, pair[1] + delta)


def get_output_field(input_field):
    output_field = {}
    for key, delta in input_field.items():
        output_field[step(key, delta)] = delta
    return output_field


def get_field(mapping):
    field = {}
    for a, b, c in mapping:
        field[(b, b + c - 1)] = a - b
    return field


def partial_step_back(output_field, field):
    new_field = {}
    for seg, diff in output_field.items():
        field, new_field_segments = cross(seg, diff, field)
        new_field.update(new_field_segments)
    return new_field, field


def step_back(mapping, field):
    new_field, field = partial_step_back(get_output_field(get_field(mapping)), field)
    return dict(sorted((new_field | field).items()))


def part1(inp):
    seeds, mappings = process(inp)

    field = {}
    for mapping in mappings[::-1]:
        field = step_back(mapping, field)

    mn = float("inf")
    for seed in seeds:
        for (start, end), diff in field.items():
            if start <= seed <= end:
                break
        else:
            diff = 0
        mn = min(mn, seed + diff)
    return mn


assert part1(inp) == 178159714


def part2():
    # seeds, mappings = process(sample)
    seeds, mappings = process(inp)

    field = {}
    for mapping in mappings[::-1]:
        field = step_back(mapping, field)

    seeds = iter(seeds)
    first_output = {}
    while True:
        try:
            a, b = next(seeds), next(seeds)
        except StopIteration:
            break
        first_output[(a, a + b - 1)] = 0

    new_field, _ = partial_step_back(first_output, field)

    mn = float("inf")
    for (a, _), diff in new_field.items():
        mn = min(mn, a + diff)
    print(mn)


part2()
# test()
print("-")
