# Before running this, pass the input through a basic sort, such as with
# the Linux `sort` command
# $ sort input.txt > input.txt.bk && mv input.txt.bk input.txt
from collections import namedtuple
import re
import sys

INPUT_PATTERN = re.compile('\[\d+-\d+-\d+ (\d+):(\d+)\] (.*)')
GUARD_PATTERN = re.compile('\D*(\d+)')
Input = namedtuple("Input", ("minute", "action"))


class Guard(object):
    def __init__(self, id_):
        self._id = id_
        self.minutes = dict()
        for i in range(60):
            self.minutes[i] = 0

    @property
    def minutes_slept(self):
        return sum(self.minutes.values())

    @property
    def most_slept(self):
        return max(self.minutes.items(), key=lambda x: x[1])[0]


def read_input():
    with open("input.txt") as f:
        for line in f:
            match = re.match(INPUT_PATTERN, line)
            if match.group(1) != '00':
                minute = 0
            else:
                minute = int(match.group(2))
            action = match.group(3)
            yield Input(minute, action)


def main1():
    guards = dict()
    onduty = None  # Current on-duty guard
    last_minute = None

    for input in read_input():
        if input.action.lower() =='wakes up':
            for i in range(last_minute, input.minute):
                onduty.minutes[i] += 1
        elif input.action.lower() == 'falls asleep':
            last_minute = input.minute
        else:
            try:
                guard_id = int(re.match(GUARD_PATTERN, input.action).group(1))
            except AttributeError as e:
                print(input)
                return False
            if guards.get(guard_id) is None:
                guards[guard_id] = Guard(guard_id)
            onduty = guards.get(guard_id)

    max_guard = None
    max_slept = 0
    for guard in guards.values():
        if guard.minutes_slept > max_slept:
            max_guard = guard
            max_slept = guard.minutes_slept

    return max_guard.most_slept * max_guard._id


def main2():
    guards = dict()
    onduty = None  # Current on-duty guard
    last_minute = None

    for input in read_input():
        if input.action.lower() =='wakes up':
            for i in range(last_minute, input.minute):
                onduty.minutes[i] += 1
        elif input.action.lower() == 'falls asleep':
            last_minute = input.minute
        else:
            try:
                guard_id = int(re.match(GUARD_PATTERN, input.action).group(1))
            except AttributeError as e:
                print(input)
                return False
            if guards.get(guard_id) is None:
                guards[guard_id] = Guard(guard_id)
            onduty = guards.get(guard_id)

    max_guard = None
    max_slept = 0
    minute_slept = None

    for guard in guards.values():
        if guard.minutes[guard.most_slept] > max_slept:
            max_guard = guard
            max_slept = guard.minutes[guard.most_slept]
            minute_slept = guard.most_slept

    return max_guard._id * minute_slept

if __name__ == '__main__':
    print("Part 1: {}".format(main1()))
    print("Part 2: {}".format(main2()))
