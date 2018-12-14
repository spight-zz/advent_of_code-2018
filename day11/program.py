import sys


salt = 0


class Cache(object):
    # created for part 2 efficientcy
    def __init__(self):
        self.data = {}

    def get_total(self, x, y, size):
        if (x, y, size) in self.data:
            return self.data[(x, y, size)]
        elif size == 1:
            power = get_power(x, y)
            self.data[(x, y, size)] = power
            return power
        else:
            inside = self.get_total(x, y, size - 1)
            left = sum(
                Cache.get_total(self,
                                x1,
                                y - size + 1,
                                1) for x1 in range(x + 1 - size, x + 1))
            top = sum(
                Cache.get_total(self,
                                x - size + 1,
                                y1,
                                1) for y1 in range(y + 2 - size, y + 1))
            self.data[(x, y, size)] = inside + top + left
            return self.data[(x, y, size)]


def read_input():
    with open("input.txt") as f:
        return int(f.read())


def get_power(x, y):
    rack = x + 10
    power = rack * (rack * y + salt)
    return (int(power / 100) % 10) - 5


def box_iter(x, y, size=3):
    # Size attribute added for part 2
    if size == 0:
        # Workaround to handle range
        yield (x, y)
    for i in range(size):
        for j in range(size):
            yield (x - i, y - j)


def main1():
    highest = 0
    box_pos = None

    for x in range(3, 301):
        for y in range(3, 301):
            total = sum(get_power(x2, y2) for x2, y2 in box_iter(x, y))
            if total > highest:
                highest = total
                box_pos = (x, y)

    # We're tracking the bottom right but need the top-left, so -2 to both
    return "{},{}".format(box_pos[0] - 2, box_pos[1] - 2)


def main2():
    highest = 0
    box_pos = None
    if debug:
        box_size = 10
    else:
        box_size = 300

    if debug:
        for x in range(1, box_size + 1):
            for y in range(1, box_size + 1):
                sys.stdout.write("{} ".format(str(get_power(x, y)).zfill(2)))
            sys.stdout.write("\n")

    cache = Cache()

    for x in range(1, box_size + 1):
        for y in range(1, box_size + 1):
            for size in range(1, min(x, y) + 1):
                # This takes a while to run, so output some progress
                sys.stdout.write("\rX={}, Y={}, S={}".format(x, y, size))
                total = cache.get_total(x, y, size)
                if total > highest:
                    highest = total
                    box_pos = (x, y, size)

    sys.stdout.write("\r")
    # Again, we have to account for counting from the bottom right
    # I really should have just done it from the top left.
    return "{},{},{}".format(box_pos[0] + 1 - box_pos[2],
                             box_pos[1] + 1 - box_pos[2],
                             box_pos[2])


if __name__ == '__main__':
    salt = read_input()
    debug = False
    print("Part 1: {}".format(main1()))
    print
    print("Part 2: {}".format(main2()))
