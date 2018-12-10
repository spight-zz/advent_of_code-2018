from queue import Queue
import sys

VERBOSE = False


class Node(object):
    def __init__(self, name, values):
        self.name = name
        self.children = []
        self.metadata = []
        self.value = 0

        num_children = values.get()
        num_metadata = values.get()

        if VERBOSE:
            print("{} child(ren) and {} metadata in {}".format(num_children, num_metadata, self.name))

        for i in range(num_children):
            self.children.append(Node("{}-{}".format(self.name, str(i)), values))

        for i in range(num_metadata):
            self.metadata.append(values.get())

        if len(self.children) > 0:
            for datum in self.metadata:
                if datum - 1 < len(self.children):
                    self.value += self.children[datum - 1].value
        else:
            self.value = sum(self.metadata)



def read_input():
    with open("input.txt") as f:
        for line in f:
            for chr in line.split(" "):
                yield int(chr)


def main1():
    total = 0
    values = Queue()

    for value in read_input():
        values.put(value)

    root = Node("root", values)

    nodes = Queue()
    nodes.put(root)

    while not nodes.empty():
        node = nodes.get()
        total += sum(node.metadata)
        for child in node.children:
            nodes.put(child)

    return total


def main2():
    total = 0
    values = Queue()

    for value in read_input():
        values.put(value)

    root = Node("root", values)
    return root.value



if __name__ == '__main__':
    print("Part 1: {}".format(main1()))
    print("Part 2: {}".format(main2()))
