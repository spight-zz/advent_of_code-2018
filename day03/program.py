import re
import sys

INPUT_PATTERN = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

def read_input():
    with open("input.txt") as f:
        for line in f:
            match = re.match(INPUT_PATTERN, line)
            yield(int(match.group(1)),
                  int(match.group(2)),
                  int(match.group(3)),
                  int(match.group(4)),
                  int(match.group(5)))


def init_fabric(fabric, size_y, size_x, initial=0):
    for i in range(size_y):
        row = list()
        fabric.append(row)
        for j in range(size_y):
            row.append(initial)


def main1():
    fabric = list()
    init_fabric(fabric, 1000, 1000, 0)

    for id, left, top, width, height in read_input():
        for width_iter in range(width):
            for height_iter in range(height):
                if fabric[left + width_iter][top + height_iter] == 0:
                    fabric[left + width_iter][top + height_iter] = 1
                elif fabric[left + width_iter][top + height_iter] == 1:
                    fabric[left + width_iter][top + height_iter] = 2

    total = 0
    for row in fabric:
        for column in row:
            if column == 2:
                total += 1

    return total


def check_claim(fabric, left, top, width, height):
    for width_iter in range(width):
        for height_iter in range(height):
            if fabric[left + width_iter][top + height_iter] == 2:
                return False
    else:
        return True


def main2():
    fabric = list()
    init_fabric(fabric, 1000, 1000, 0)
    for id, left, top, width, height in read_input():
        for width_iter in range(width):
            for height_iter in range(height):
                if fabric[left + width_iter][top + height_iter] == 0:
                    fabric[left + width_iter][top + height_iter] = 1
                elif fabric[left + width_iter][top + height_iter] == 1:
                    fabric[left + width_iter][top + height_iter] = 2

    for id, left, top, width, height in read_input():
        if check_claim(fabric, left, top, width, height):
            return id


if __name__ == '__main__':
    print("Part 1: {}".format(main1()))
    print("Part 2: {}".format(main2()))
