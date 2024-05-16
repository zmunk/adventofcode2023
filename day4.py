from collections import defaultdict
import re
from pathlib import Path

sample = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11 """.split("\n")

inp = open(Path(__file__).resolve().stem + ".txt").read().splitlines()

def process(inp):
    cards = []
    for line in inp:
        winning_nums, nums = re.match(r'Card +\d+: (.*) \| (.*)', line).groups()
        winning_nums = {int(n) for n in winning_nums.split()}
        nums = [int(n) for n in nums.split()]
        cards.append((winning_nums, nums))
    return cards

def part1(inp):
    acc = 0
    for winning_nums, nums in process(inp):
        count = 0
        for num in nums:
            if num in winning_nums:
                count += 1

        score = 2 ** (count - 1) if count > 0 else 0
        acc += score
    return acc

def get_score(count):
    return 2 ** (count - 1) if count > 0 else 0

def part2(inp):
    cards = {i: card for i, card in enumerate(process(inp), start=1)}
    copies = defaultdict(int)
    card_nums = list(range(1, 1 + len(cards)))
    copies.update({i: 1 for i in card_nums})

    for i in card_nums:
        card = cards[i]
        winning, nums = card
        count = 0
        for num in nums:
            if num in winning:
                count += 1

        for j in range(i + 1, i + 1 + count):
            copies[j] += copies[i]
    return sum(copies.values())

print(part1(inp))
print(part2(inp))
print("-")
