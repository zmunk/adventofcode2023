import re
import json
from functools import reduce
from pprint import pprint

sample = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".split("\n")

inp = open("day2.txt").read().splitlines()

def process(inp):
    games = []
    for line in inp:
        try:
            game_num, game = re.match(r'Game (\d+): (.*)', line).groups()
        except AttributeError:
            print(line)
        rounds = []
        for subset in game.split("; "):
            counts = []
            for t in subset.split(", "):
                num, color = re.match(r'(\d+) (.*)', t).groups()
                counts.append((int(num), color))
            rounds.append(counts)
        games.append(rounds)
    return games
# pprint(game)
def check(game):
    for rnd in game:
        for count, color in rnd:
            if color == "red" and count > 12 \
                    or color == "green" and count > 13 \
                    or color == "blue" and count > 14:
                return False
    return True


def part1(inp):
    games = process(inp)

    acc = 0
    for i, game in enumerate(games, start=1):
        if check(game):
            acc += i
    return acc

def part2(inp):
    games = process(inp)

    res = 0
    for game in games:
        counts = {
            "blue": 0,
            "green": 0,
            "red": 0,
        }
        for rnd in game:
            for count, color in rnd:
                print(f"{count, color = }")
                counts[color] = max(counts[color], count)
        res += reduce(lambda x, y: x * y, counts.values(), 1)
    return res
            

# print(part1(inp))
print(part2(inp))
print("-")

