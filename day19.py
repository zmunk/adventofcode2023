from pathlib import Path
from collections import defaultdict
from copy import deepcopy
import re


def get_match(regex, s):
    res = re.match(regex, s)
    if res is None:
        raise ValueError()
    return res.groups()


sample = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}\
"""

inp = open(Path(__file__).resolve().stem + ".txt").read().strip()


def apply(func_name, ratings, functions):
    for step in functions[func_name]:
        if isinstance(step, str):
            return step
        res = step(ratings)
        if res is not None:
            return res


def run_workflow(ratings, functions):
    res = "in"
    while res not in ["R", "A"]:
        res = apply(res, ratings, functions)
    return res


def create_step(var_name, comparison, limit, on_pass):
    def step(ratings):
        if (comparison == "<" and ratings[var_name] < limit) or (
            comparison == ">" and ratings[var_name] > limit
        ):
            return on_pass
        else:
            return None

    return step


def part1(inp):
    workflows, ratings_raw = inp.split("\n\n")
    functions = {}
    for line in workflows.split("\n"):
        func_name, rules = get_match(r"(.*){(.*)}", line)
        functions[func_name] = []
        for rule in rules.split(","):
            if ":" in rule:
                rating_name, comparison, lim, on_pass = get_match(
                    r"(.*)([<>])(\d+):(.*)", rule
                )
                functions[func_name].append(
                    create_step(rating_name, comparison, int(lim), on_pass)
                )
            else:
                functions[func_name].append(rule)
    acc = 0
    for line in ratings_raw.split("\n"):
        x, m, a, s = get_match(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", line)
        ratings = {"x": int(x), "m": int(m), "a": int(a), "s": int(s)}
        res = run_workflow(ratings, functions)
        if res == "A":
            acc += sum(ratings.values())
    return acc


###
class Condition:
    def __init__(self, rating_name, comparison, lim):
        self.rating_name = rating_name
        self.comparison = comparison
        self.lim = lim

    def __str__(self):
        return f"{self.rating_name} {self.comparison} {self.lim}"

    def __repr__(self):
        return f"{self.rating_name} {self.comparison} {self.lim}"

    def __invert__(self):
        if self.comparison == "<":
            return Condition(self.rating_name, ">=", self.lim)
        elif self.comparison == ">=":
            return Condition(self.rating_name, "<", self.lim)
        else:
            raise ValueError


UPPER_LIMIT = 4001  # exclusive
LOWER_LIMIT = 1  # inclusive


def transform_branch(branch):
    """
    input: [s >= 536, x < 2441]
    output: {
        "x": {">=": 1, "<": 2441},
        "m": {">=": 1, "<": 4001},
        "a": {">=": 1, "<": 4001},
        "s": {">=": 536, "<": 4001},
    }
    """
    output = {
        "x": {">=": LOWER_LIMIT, "<": UPPER_LIMIT},
        "m": {">=": LOWER_LIMIT, "<": UPPER_LIMIT},
        "a": {">=": LOWER_LIMIT, "<": UPPER_LIMIT},
        "s": {">=": LOWER_LIMIT, "<": UPPER_LIMIT},
    }

    for condition in branch:
        if condition.comparison == "<":
            func = min
        elif condition.comparison == ">=":
            func = max
        else:
            raise ValueError
        output[condition.rating_name][condition.comparison] = func(
            output[condition.rating_name][condition.comparison], condition.lim
        )
    return output


def combine_branches(branch_a, branch_b):
    output = {}
    for c in "xmas":
        output[c] = {}
        output[c][">="] = max(branch_a[c][">="], branch_b[c][">="])
        output[c]["<"] = min(branch_a[c]["<"], branch_b[c]["<"])
    return output


def prune(branches, evaluated):
    """Remove all branches that lead to 'R'"""
    pruned_branches = []
    for b, res in branches:
        if res == "R":
            continue

        if res == "A":
            pruned_branches.append(transform_branch(b))
        elif res in evaluated:
            for other_branch in evaluated[res]:
                pruned_branches.append(
                    combine_branches(transform_branch(b), other_branch)
                )
        else:
            raise AssertionError(f"{res = }")

    return pruned_branches


def get_blocks(functions):
    evaluated = {}
    while "in" not in evaluated:
        to_remove = []
        for f, branches in functions.items():
            for _, res in branches:
                if res in ["A", "R"] or res in evaluated:
                    pass
                else:
                    break
            else:
                evaluated[f] = prune(branches, evaluated)
                to_remove.append(f)
        for f in to_remove:
            del functions[f]
    blocks = []
    for rule in evaluated["in"]:
        arr = []
        for c in "xmas":
            arr.append((rule[c][">="], rule[c]["<"]))
        blocks.append(arr)
    return blocks


def get_intersection(block_a, block_b):
    lengths = []
    for dim in range(4):
        lower = max(block_a[dim][0], block_b[dim][0])
        upper = min(block_a[dim][1], block_b[dim][1])
        if lower >= upper:
            return
        lengths.append((lower, upper))
    return lengths


def get_layers(inp):
    functions = get_functions(inp)
    blocks = get_blocks(functions)
    layers = defaultdict(list)
    for block in blocks:
        for i, layer in deepcopy(dict(layers)).items():
            for other_block in layer:
                intx = get_intersection(other_block, block)
                if intx:
                    layers[i + 1].append(intx)
        layers[0].append(block)
    return layers


def get_functions(inp):
    workflows, _ = inp.split("\n\n")
    functions = {}
    for line in workflows.split("\n"):
        func_name, rules = get_match(r"(.*){(.*)}", line)
        arr = []
        prev_conditions = []
        for rule in rules.split(","):
            conditions = []
            new_condition = None
            if ":" in rule:
                rating_name, comparison, lim, on_pass = get_match(
                    r"(.*)([<>])(\d+):(.*)",
                    rule,
                )
                lim = int(lim)
                if comparison == ">":
                    comparison = ">="
                    lim += 1
                new_condition = Condition(rating_name, comparison, lim)
            else:
                on_pass = rule

            for cond in prev_conditions:
                conditions.append(~cond)

            if new_condition:
                conditions.append(new_condition)
                prev_conditions.append(new_condition)

            arr.append((conditions, on_pass))
        functions[func_name] = arr

    return functions


def part2(inp):
    layers = get_layers(inp)
    total_area = 0
    for i, layer in layers.items():
        layer_area = 0
        for line in layer:
            area = 1
            for low, high in line:
                area *= high - low
            layer_area += area
        if i % 2 == 0:
            total_area += layer_area
        else:
            total_area -= layer_area
    return total_area


assert part1(inp) == 575412
assert part2(sample) == 167409079868000
print(f"{part2(inp) = }")
print("-")
