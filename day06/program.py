from queue import Queue


DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Node(object):
    # A node corresponds to one line of input
    def __init__(self, x, y, max=None, name=None):
        self.name = name
        self.x = x
        self.y = y
        self.iter = None
        self.max_distance = max
        self.is_inf = False


class Surface(object):
    # This acts as a way to keep all Coordinates unique and allows us to
    # work in a pseudo-cartesian plane with numbers rather than in arrays
    def __init__(self):
        self.data = dict()

    def point_at(self, x, y):
        # KeyError-safe logic to find point in 2d dict
        return self.data.get(x, {}).get(y)

    def register(self, x, y, node):
        column = self.data.get(x)
        if column is None:
            column = dict()
            self.data[x] = column
        column[y] = node

    def __iter__(self):
        for column in self.data.values():
            for point in column.values():
                yield point

    def reset(self):
        self.data = dict()


class Coordinate(object):
    # Functions as a coordinate within a surface for the first part of the puzzle
    def __init__(self, surface, max, x, y):
        self.surface = surface
        self.tied = False
        self.closest = None
        self.closest_distance = None
        self.x = x
        self.y = y
        self.max = max
        surface.register(x, y, self)

    def expand(self):
        # Expand is the meat of the solution to this puzzle, by doing any iteration
        # business logic and also sorting out any conflicts near the border of
        # nodes' areas.
        if self.closest_distance > self.max:
            self.closest.is_inf = True
            return

        for x, y in DIRECTIONS:
            new_x, new_y = self.x + x, self.y + y

            point = self.surface.point_at(new_x, new_y)
            if point is None:
                point = Coordinate(self.surface, self.max, new_x, new_y)
                point.closest = self.closest
                point.closest_distance = self.closest_distance + 1
                yield point
            else:
                if point.closest_distance > self.closest_distance + 1:
                    point.closest = self.closest
                    point.closest_distance = self.closest_distance +1
                elif point.closest_distance == self.closest_distance + 1 and \
                        self.closest != point.closest:
                    point.tied = True
                elif point.closest_distance + 1 < self.closest_distance:
                    self.closest = point.closest
                    self.closest_distance = point.closest_distance + 1


class Coordinate2(Coordinate):
    # Functions as a coordinate for the second part of the puzzle
    # Has slightly different expand logic from the first coordinate
    def __init__(self, surface, nodes, max, x, y):
        super().__init__(surface, max, x, y)
        self.nodes = nodes
        self.distance = 0
        self.calculate_distance()

    def calculate_distance(self):
        total = 0
        for node in self.nodes:
            total += abs(self.x - node.x)
            total += abs(self.y - node.y)
        self.distance = total

    def expand(self):
        for x, y in DIRECTIONS:
            new_x, new_y = self.x + x, self.y + y
            if self.surface.point_at(new_x, new_y) is not None:
                continue
            else:
                new_point = Coordinate2(self.surface, self.nodes, self.max,
                                        new_x, new_y)
                yield new_point

    @property
    def in_range(self):
        return self.distance < self.max



def read_input():
    with open("input.txt") as f:
        for i, line in enumerate(f):
            x, y = line.split(", ")
            yield Node(int(x), int(y), name=str(i))


def main1():
    uppest, downest, leftest, rightest = None, 0, None, 0
    for node in read_input():
        if leftest is None or node.x < leftest:
            leftest = node.x
        if node.x > rightest:
            rightest = node.x
        if uppest is None or node.y < uppest:
            uppest = node.y
        if node.y > downest:
            downest = node.y

    # The maximum distance around a Node without being infinite will be
    # at most the radius of a circle that inscribes the working area
    max_distance = int(max((downest - uppest), (rightest - leftest)) / 2) + 1

    surface = Surface()
    q = Queue()

    for node in read_input():
        point = Coordinate(surface, max_distance, node.x, node.y)
        point.closest = node
        point.closest_distance = 0
        q.put(point)

    while not q.empty():
        point = q.get()
        for new_point in point.expand():
            q.put(new_point)

    counts = {}

    for point in surface:
        if not point.closest.is_inf and not point.tied:
            count = counts.get(point.closest.name)
            if count is None:
                counts[point.closest.name] = 1
            else:
                counts[point.closest.name] += 1

    # Get name and area of largest area
    return max(counts.items(), key=lambda x: x[1])


def main2():
    surface = Surface()
    q = Queue()

    nodes = list(read_input())

    # First, find a point that satisfies the requirements. All other points
    # will be contiguous with it
    q.put(Coordinate2(surface, nodes, 10000, nodes[0].x, nodes[0].y))
    root_success = None
    while root_success is None and not q.empty():
        point = q.get()
        if point.in_range:
            root_success = point
        else:
            for new_point in point.expand():
                q.put(new_point)

    # Drain the queue
    while not q.empty():
        q.get()

    # Reset the surface except for the root_success
    surface.reset()
    surface.register(root_success.x, root_success.y, root_success)

    total_in_range = 0
    while not q.empty():
        point = q.get()
        if point.in_range:
            total_in_range += 1
            for new_point in point.expand():
                q.put(new_point)

    return total_in_range


if __name__ == '__main__':
    print("Part 1: {}".format(main1()))
    print("Part 2: {}".format(main2()))
