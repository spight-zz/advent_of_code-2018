# Before running this, pass the input through a basic sort, such as with
# the Linux `sort` command
# $ sort input.txt > input.txt.bk && mv input.txt.bk input.txt
from collections import namedtuple
import re
import sys

INPUT_PATTERN = re.compile('Step (\w) must be finished before step (\w) can begin.')
Input = namedtuple("Input", ("precursor", "successor"))


def read_input():
    with open("input.txt") as f:
        for line in f:
            match = re.match(INPUT_PATTERN, line)
            yield Input(match.group(1), match.group(2))


class Node(object):
    def __init__(self, name):
        self.name = name
        self.precursors = []
        self.successors = []


class Worker(object):
    def __init__(self, name):
        self.name = name
        self.current = None  # Current task
        self.remaining = 0  # Remaining time to complete current task

    def tick(self):
        self.remaining -= 1

    @property
    def ready(self):
        if self.remaining <= 0:
            return True



def main1():
    instructions = {}
    for first, second in read_input():
        node_a = instructions.get(first)
        node_b = instructions.get(second)
        if node_a is None:
            node_a = Node(first)
            instructions[first] = node_a
        if node_b is None:
            node_b = Node(second)
            instructions[second] = node_b

        node_a.successors.append(node_b)
        node_b.precursors.append(node_a)

    order = []

    while True:
        ready = sorted(
            filter(lambda x: len(x[1].precursors) == 0, instructions.items()),
            key=lambda x: x[1].name)

        if len(ready) == 0:
            break

        name, node = ready[0]
        order.append(name)
        for successor in node.successors:
                successor.precursors.remove(node)
        del instructions[name]

    return "".join(order)


def main2():
    instructions = {}
    for first, second in read_input():
        node_a = instructions.get(first)
        node_b = instructions.get(second)
        if node_a is None:
            node_a = Node(first)
            instructions[first] = node_a
        if node_b is None:
            node_b = Node(second)
            instructions[second] = node_b

        node_a.successors.append(node_b)
        node_b.precursors.append(node_a)

    duration = 0
    workers = []

    for i in range(5):
        workers.append(Worker(str(i)))

    while True:
        ready = sorted(
            filter(lambda x: len(x[1].precursors) == 0, instructions.items()),
            key=lambda x: x[1].name)

        remaining = max(map(lambda x: x.remaining, workers))
        if remaining <= 0 and len(instructions) == 0:
            break

        for name, node in ready:
            idle_worker = None
            for worker in workers:
                if worker.ready:
                    idle_worker = worker
                    break
            if idle_worker:
                idle_worker.current = node
                del instructions[name]
                # Ordinal of A is 65, but duration is 61, and all durations
                # increase linearly, so subtract 4 to get actual duration
                idle_worker.remaining = ord(node.name) - 4

        for worker in workers:
            worker.tick()
            if worker.ready and worker.current is not None:
                for successor in worker.current.successors:
                    successor.precursors.remove(worker.current)
                worker.current = None

        duration += 1

    return duration


if __name__ == '__main__':
    print("Part 1: {}".format(main1()))
    print("Part 2: {}".format(main2()))
