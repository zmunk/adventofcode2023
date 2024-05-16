from pathlib import Path
from functools import lru_cache
from collections import defaultdict

sample = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
inp = open(Path(__file__).resolve().stem + ".txt").read().strip()


def part1(inp):
    acc = 0
    for line in inp.split(","):
        s = 0
        for c in line:
            s = (s + ord(c)) * 17 % 256
        acc += s
    return acc


class Box:
    def __init__(self):
        self.next = self
        self.last = self

    def __repr__(self):
        node = self.next
        if node == self:
            return "[]"
        r = "["
        while node is not None:
            r += repr(node) + ", "
            node = node.next
        return r[:-2] + "]"

    def append(self, node):
        node.prev = self.last
        self.last = node

    def remove(self, node):
        if node == self.last:
            self.last = node._prev
        node.remove()
        if self.next == None:
            self.next = self

    def score(self):
        if self.next == self:
            return 0
        acc = 0
        slot_num = 1
        node = self.next
        while isinstance(node, Node):
            acc += slot_num * node.val
            node = node.next
            slot_num += 1
        return acc


class Node:
    def __init__(self, name, val):
        self.name = name
        self.val = val
        self._prev = None
        self.next = None

    def __repr__(self):
        return f"({self.name} {self.val})"

    def __setattr__(self, name, value):
        if name == "prev":
            self.set_prev(value)
        else:
            super().__setattr__(name, value)

    def set_prev(self, prev):
        self._prev = prev
        prev.next = self

    def remove(self):
        if self.next is not None:
            self.next.prev = self._prev
        elif self._prev is not None:
            self._prev.next = None


@lru_cache
def hash(name):
    s = 0
    for c in name:
        s = (s + ord(c)) * 17 % 256
    return s


def part2(inp):
    m = {}
    d = defaultdict(Box)

    for line in inp.split(","):
        if line[-1] == "-":
            name = line[:-1]
            if name in m:
                d[hash(name)].remove(m[name])
                del m[name]
        else:
            name, val = line.split("=")
            val = int(val)

            if name in m:
                m[name].val = val
            else:
                node = Node(name, val)
                m[name] = node
                d[hash(name)].append(node)

    acc = 0
    for k, box in d.items():
        score = box.score()
        acc += (k + 1) * score

    return acc


print(part1(inp))
print(part2(inp))
print("-")
