import re
import sys

INPUT_PATTERN = re.compile(r'position=<([- ]\d+), ([- ]\d+)> velocity=<([- ]\d+), ([- ]\d+)>')


class Pair(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Input(object):
    def __init__(self, pos_x, pos_y, vel_x, vel_y):
        self.pos = Pair(pos_x, pos_y)
        self.vel = Pair(vel_x, vel_y)

    def pos_at(self, time):
        return Pair(self.pos.x + time * self.vel.x,
                    self.pos.y + time * self.vel.y)


class Surface(object):
    # Partially ripped from my day 6 solution
    def __init__(self):
        self.points = list()

    def add(self, pos):
        self.points.append(pos)

    def fit_to_zero(self):
        # Shifts all of the positions such that the bottom left edge is 0,0
        offset_y = min(pos.y for pos in self.points)
        offset_x = min(pos.x for pos in self.points)
        for point in self.points:
            point.x -= offset_x
            point.y -= offset_y

    def __str__(self):
        width = max(pos.x for pos in self.points) + 1
        height = max(pos.y for pos in self.points) + 1
        points_list = list()
        for y in range(height):
            row = list()
            points_list.append(row)
            for x in range(width):
                row.append(' ')

        # print("W: {} H: {} len_out: {} len_in: {}".format(width, height, len(points_list), len(points_list[0])))
        for point in self.points:
            points_list[point.y][point.x] = '#'

        return "\n".join(map(lambda x: "".join(x), points_list))


def read_input():
    with open("input.txt") as f:
        for line in f:
            match = re.match(INPUT_PATTERN, line)
            yield(Input(*map(int, match.groups())))


def main1():
    area = float("inf")
    t = 0
    inputs = list(read_input())

    while True:  # Find when the stars get to their closest point
        left_bound, down_bound = float("inf"), float("inf")
        right_bound, up_bound = float("-inf"), float("-inf")

        for input in inputs:
            pos = input.pos_at(t)
            if pos.x < left_bound:
                left_bound = pos.x
            if pos.x > right_bound:
                right_bound = pos.x
            if pos.y < down_bound:
                down_bound = pos.y
            if pos.y > up_bound:
                up_bound = pos.y


        new_area = (right_bound - left_bound) * (up_bound - down_bound)
        if new_area > area:  # The stars started expanding
            break
        area = new_area
        t += 1

    # The loop stops at the first time the area expands, so t - 1 is the
    # smallest
    t -= 1

    surface = Surface()

    for input in inputs:
        surface.add(input.pos_at(t))
    surface.fit_to_zero()
    return "\n" + str(surface)


def main2():
    area = float("inf")
    t = 0
    inputs = list(read_input())

    while True:  # Find when the stars get to their closest point
        left_bound, down_bound = float("inf"), float("inf")
        right_bound, up_bound = float("-inf"), float("-inf")

        for input in inputs:
            pos = input.pos_at(t)
            if pos.x < left_bound:
                left_bound = pos.x
            if pos.x > right_bound:
                right_bound = pos.x
            if pos.y < down_bound:
                down_bound = pos.y
            if pos.y > up_bound:
                up_bound = pos.y


        new_area = (right_bound - left_bound) * (up_bound - down_bound)
        if new_area > area:  # The stars started expanding
            break
        area = new_area
        t += 1

    return t - 1


if __name__ == '__main__':
    print("Part 1: {}".format(main1()))
    print("Part 2: {}".format(main2()))
