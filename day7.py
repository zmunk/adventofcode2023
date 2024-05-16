from collections import Counter
from pathlib import Path
import functools

sample = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".split(
    "\n"
)

inp = open(Path(__file__).resolve().stem + ".txt").read().splitlines()


def get_value(hand, joker=False):
    c = dict(Counter(hand))
    if joker:
        joker_count = c.get("J", 0)
        if joker_count > 0:
            del c["J"]
            try:
                top_card = max(c.items(), key=lambda x: x[1])[0]
            except ValueError:
                top_card = "J"
                c[top_card] = 0
            c[top_card] += joker_count
    c = sorted(c.values())
    if len(c) == 1:
        return 6
    if len(c) == 2:
        if c == [1, 4]:
            return 5
        return 4
    if len(c) == 3:
        if 3 in c:
            return 3
        return 2
    if 2 in c:
        return 1
    return 0


card_ranks = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}


def get_card_rank(card, joker=False):
    if joker and card == "J":
        return 0
    else:
        return card_ranks[card]


def compare_cards(hand1, hand2, joker=False):
    for card1, card2 in zip(hand1, hand2):
        rank1, rank2 = get_card_rank(card1, joker), get_card_rank(card2, joker)
        if rank1 > rank2:
            return 1
        if rank1 < rank2:
            return -1
    return 0


@functools.cmp_to_key
def compare_hands(hand1, hand2):
    val1 = get_value(hand1)
    val2 = get_value(hand2)
    if val1 > val2:
        return 1
    if val1 < val2:
        return -1
    return compare_cards(hand1, hand2)


@functools.cmp_to_key
def compare_hands_v2(hand1, hand2):
    val1 = get_value(hand1, joker=True)
    val2 = get_value(hand2, joker=True)
    if val1 > val2:
        return 1
    if val1 < val2:
        return -1
    return compare_cards(hand1, hand2, joker=True)


def process(inp):
    hands = []
    bids = {}
    for line in inp:
        hand, bid = line.split()
        hands.append(hand)
        bids[hand] = int(bid)
    return hands, bids


def part1():
    hands, bids = process(inp)

    acc = 0
    for rank, hand in enumerate(sorted(hands, key=compare_hands), start=1):
        acc += rank * bids[hand]
    return acc


def part2():
    hands, bids = process(inp)
    acc = 0
    for rank, hand in enumerate(sorted(hands, key=compare_hands_v2), start=1):
        acc += rank * bids[hand]
    print(f"{acc = }")


assert part1() == 256448566
part2()
print("-")
