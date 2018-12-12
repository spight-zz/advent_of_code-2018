import re
import sys

INPUT_PATTERN = re.compile('(\d+) players?; last marble is worth (\d+) points?')


def read_input():
    with open("input.txt") as f:
        match = re.match(INPUT_PATTERN, f.read())
        return (int(match.group(1)), int(match.group(2)))


class Node(object):
    def __init__(self, value, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev

        self.set_prev(prev)
        self.set_next(next)

    def set_next(self, next):
        self.next = next
        if next:
            next.prev = self

    def set_prev(self, prev):
        self.prev = prev
        if prev:
            prev.next = self

    def remove(self):
        self.next.prev = self.prev
        self.prev.next = self.next
        return self.value


class Player(object):
    def __init__(self, name):
        self.next = None
        self.name = str(name)
        self.score = 0


class Circle(object):
    def __init__(self):
        self.current = Node(0)
        self.root = self.current
        self.current.next = self.current
        self.current.prev = self.current
        self.iter_current = None
        self.iter_stop = False

    def __iter__(self):
        self.iter_stop = False
        self.iter_current = self.root
        return self

    def __next__(self):
        ret = self.iter_current
        self.iter_current = self.iter_current.next
        if ret is self.root:
            if self.iter_stop:
                raise StopIteration()
            else:
                self.iter_stop = True
        return ret

    def add(self, value):
        if value % 23 == 0:
            # Do scoring
            old_node = self.current.prev.prev.prev.prev.prev.prev.prev
            self.current = old_node.next
            extra = old_node.remove()
            return value + extra
        else:
            # new_node = Node(value, self.current.next.next, self.current.next)
            new_node = Node(value)
            new_prev = self.current.next
            new_next = self.current.next.next
            new_node.set_next(new_next)
            new_node.set_prev(new_prev)
            self.current = new_node
            return 0  # No score added for this turn


def main1():
    circle = Circle()
    first_player = None
    current_player = None

    num_players, max_marble = read_input()

    # Set up players
    for i in range(1, num_players + 1):
        new_player = Player(i)
        if first_player is None:
            first_player = new_player

        if current_player is None:
            current_player = new_player
        current_player.next = new_player
        current_player = new_player

    current_player.next = first_player
    current_player = first_player

    # Play the game
    for i in range(1, max_marble + 1):
        current_player.score += circle.add(i)
        current_player = current_player.next

    highest = first_player
    current_player = first_player.next

    while current_player is not first_player:
        if current_player.score > highest.score:
            highest = current_player
        current_player = current_player.next

    return highest.score


def main2():
    circle = Circle()
    first_player = None
    current_player = None

    num_players, max_marble = read_input()
    max_marble *= 100

    # Set up players
    for i in range(1, num_players + 1):
        new_player = Player(i)
        if first_player is None:
            first_player = new_player

        if current_player is None:
            current_player = new_player
        current_player.next = new_player
        current_player = new_player

    current_player.next = first_player
    current_player = first_player

    # Play the game
    for i in range(1, max_marble + 1):
        score = circle.add(i)
        if score > 0:
            current_player.score += score
        current_player = current_player.next

    highest = first_player.score
    current_player = first_player.next

    while current_player is not first_player:
        if current_player.score > highest:
            highest = current_player.score
        current_player = current_player.next

    return highest


if __name__ == '__main__':
    print("Part 1: {}".format(main1()))
    print("Part 2: {}".format(main2()))
