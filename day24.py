from utils import get_match

inp = open("day24.txt").read().strip()
sample = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


def check_cross(a, b):
    (px1, py1, _), (vx1, vy1, _) = a
    (px2, py2, _), (vx2, vy2, _) = b

    try:
        x = ((vy1 * vx2 * px1 - vy2 * vx1 * px2) + (py2 - py1) * vx1 * vx2) / (
            vy1 * vx2 - vy2 * vx1
        )
    except ZeroDivisionError:
        return False
    y = (vy1 / vx1) * (x - px1) + py1
    t1 = (x - px1) / vx1
    t2 = (x - px2) / vx2
    if t1 > 0 and t2 > 0 and (MIN <= x <= MAX) and (MIN <= y <= MAX):
        return True
    else:
        return False


if False:
    inp = sample
    MIN = 7
    MAX = 27
else:
    MIN = 200000000000000
    MAX = 400000000000000


hailstones = []
for line in inp.split("\n"):
    pos, velocity = get_match(r"(.*) @ (.*)", line)
    pos = tuple(map(int, pos.split(", ")))
    velocity = tuple(map(int, velocity.split(", ")))
    hailstones.append((pos, velocity))

acc = 0
for i, h1 in enumerate(hailstones):
    for h2 in hailstones[i + 1 :]:
        if check_cross(h1, h2):
            acc += 1
print("part 1", acc)

from sympy import symbols, nonlinsolve

x0, y0, z0, vx, vy, vz, *t_vec = symbols(
    "x0, y0, z0, vx, vy, vz, t1, t2, t3", real=True
)
values = hailstones[:3]
equations = []
for t, (pos, velocity) in zip(t_vec, values):
    for i, (p0, v) in enumerate([(x0, vx), (y0, vy), (z0, vz)]):
        equations.append(pos[i] + velocity[i] * t - p0 - v * t)

x, y, z, *_ = list(nonlinsolve(equations, [x0, y0, z0, vx, vy, vz, *t_vec]))[0]
print("part 2", x + y + z)

print("-")
