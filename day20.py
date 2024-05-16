import time
from queue import Queue
from collections import defaultdict
from utils import get_match

inp = open("day20.txt").read().strip()

sample1 = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

sample2 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


class BaseModule:
    def __init__(self, dest):
        """dest: destination modules"""
        self.dest: list[str] = dest

    def propagate(self, pulse: int, *args):
        next_pulses = []
        for module in self.dest:
            next_pulses.append((module, pulse))
        return next_pulses


class BroadcasterModule(BaseModule):
    pass


class TestModule(BaseModule):
    def __init__(self):
        pass

    def propagate(self, *args):
        return []


class FlipFlopModule(BaseModule):
    def __init__(self, dest):
        self.state = 0
        super().__init__(dest)

    def __str__(self):
        return f"[{self.state}]"

    def propagate(self, pulse: int, *args):
        """pulse: 0 for low and 1 for high"""
        next_pulses = []
        if pulse == 1:
            return next_pulses
        assert pulse == 0
        if self.state == 0:
            self.state = 1
            return super().propagate(1)
        assert self.state == 1
        self.state = 0
        return super().propagate(0)


class ConjuctionModule(BaseModule):
    def __init__(self, dest, inputs):
        """
        history: defaultdict that stores 0 (low) or 1 (high) for last
            pulse received from each module that feeds into this module
        """
        self.history = {k: 0 for k in inputs}
        self.low_pulse_inputs = set(inputs)
        super().__init__(dest)

    def __str__(self):
        return f"{dict(self.history)}"

    def propagate(self, pulse: int, src: str):
        self.history[src] = pulse
        if pulse == 0:
            self.low_pulse_inputs.add(src)
        elif pulse == 1:
            self.low_pulse_inputs.discard(src)
        else:
            raise ValueError

        if len(self.low_pulse_inputs) == 0:
            return super().propagate(0)
        else:
            return super().propagate(1)


def process_input(inp):
    modules = {}

    ## compile backwards map, i.e. output -> list of inputs
    backwards_map = defaultdict(list)
    for line in inp.split("\n"):
        module_name, destination_modules = get_match(r"(.*) -> (.*)", line)
        module_name = module_name[1:]
        destination_modules = destination_modules.split(", ")
        for dest in destination_modules:
            backwards_map[dest].append(module_name)

    for line in inp.split("\n"):
        module_name, destination_modules = get_match(r"(.*) -> (.*)", line)
        destination_modules = destination_modules.split(", ")
        if module_name[:1] == "%":
            modules[module_name[1:]] = FlipFlopModule(destination_modules)
        elif module_name[:1] == "&":
            module_name = module_name[1:]
            modules[module_name] = ConjuctionModule(
                destination_modules, backwards_map[module_name]
            )
        elif module_name == "broadcaster":
            modules["broadcaster"] = BroadcasterModule(destination_modules)
        else:
            raise ValueError(module_name)
    return modules


class GXPulseException(Exception):
    pass


class RXPulseException(Exception):
    pass


def push_button(modules, verbose=0):
    """
    pulses stores tuples e.g. (source name, destination name, pulse value)
    pulse value: 1 for high or 0 for low
    """
    if verbose > 0:
        print("pushing button ...")
    pulses = Queue()
    pulses.put(("button", "broadcaster", 0))

    pulse_counts = [0, 0]  # low, high

    while not pulses.empty():
        src, dest, pulse_value = pulses.get()
        if verbose > 0:
            print(f"{src} -{pulse_value}-> {dest}")
        # if dest == "rx":
        #     print(f"sending pulse {pulse_value} to 'rx'")
        #         if checking_rx and src == "gx" and pulse_value == 0:
        #             raise GXPulseException()
        #
        #         if checking_rx and dest == "rx" and pulse_value == 0:
        #             raise RXPulseException()
        pulse_counts[pulse_value] += 1
        module = modules.get(dest)
        if module is None:
            continue
        for next_module, next_val in module.propagate(pulse_value, src):
            pulses.put((dest, next_module, next_val))

    if verbose > 0:
        print("module states:")
    for module_name, module in modules.items():
        if verbose > 0:
            print(module_name, str(module))

    if verbose > 0:
        print(f"pulse counts: {pulse_counts}")

    return pulse_counts


"""
modules = {
    "broadcaster": BroadcasterModule(["a", "b", "c"]),
    "a": FlipFlopModule(["b"]),
    "b": FlipFlopModule(["c"]),
    "c": FlipFlopModule(["inv"]),
    "inv": ConjuctionModule(["a"], ["c"]),
}

modules = {
    "broadcaster": BroadcasterModule(["a"]),
    "a": FlipFlopModule(["inv", "con"]),
    "inv": ConjuctionModule(["b"], ["a"]),
    "b": FlipFlopModule(["con"]),
    "con": ConjuctionModule(["output"], ["a", "b"]),
    "output": TestModule(),
}
"""


def add(a, b):
    return [a[0] + b[0], a[1] + b[1]]


def part1(inp):
    modules = process_input(inp)
    pulse_counts = [0, 0]
    for _ in range(1000):
        counts = push_button(modules)
        pulse_counts = add(pulse_counts, counts)
    return pulse_counts[0] * pulse_counts[1]


def push_button_v2(modules, to_observe):
    """
    pulses stores tuples e.g. (source name, destination name, pulse value)
    pulse value: 1 for high or 0 for low
    """
    pulses = Queue()
    pulses.put(("button", "broadcaster", 0))

    triggered = False
    while not pulses.empty():
        src, dest, pulse_value = pulses.get()
        if (dest, pulse_value) == to_observe:
            triggered = True
        module = modules.get(dest)
        if module is None:
            continue
        for next_module, next_val in module.propagate(pulse_value, src):
            pulses.put((dest, next_module, next_val))

    return triggered


def get_diff(inp, module):
    modules = process_input(inp)
    count = 0
    last_hit = 0
    diff = 0
    while True:
        triggered = push_button_v2(modules, (module, 0))
        if triggered:
            if count - last_hit == diff:
                return diff
            diff = count - last_hit
            last_hit = count
        count += 1


def part2(inp):
    n = 1
    modules = process_input(inp)
    for module in modules["hp"].history.keys():
        n *= get_diff(inp, module)
    return n


assert part1(inp) == 812609846
assert part2(inp) == 245114020323037


print("-")
