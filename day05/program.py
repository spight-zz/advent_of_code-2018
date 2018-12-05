def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def main1():
    line = list(read_input())
    i = 0
    j = 1
    reacted = 0

    while j < len(line):
        chr = line[i]
        next = line[j]
        if chr.islower() != next.islower() and chr.lower() == next.lower():
            # React
            line[i] = None
            line[j] = None
            reacted += 2

            # Go backwards to the latest unreacted character
            while i > 0 and line[i] is None:
                i -= 1

            if line[i] is None:  # No characters before the reaction
                while i < len(line) and line[i] is None:
                    i += 1
            j += 1
            if i == j:  # In case the next character for is is j's pointer
                j += 1
        else:
            j += 1
            i += 1
            # Move forward to the next unreacted character
            while i < len(line) and line[i] is None:
                i += 1

    return len(line) - reacted


def main2():
    raw = read_input()
    types = set(raw.lower())
    worst_type = (None, 0)

    for test_type in types:
        line = list(raw)
        i = 0
        j = 1
        reacted = 0
        while i < len(line) and line[i].lower() == test_type:
            i += 1

        while j < len(line) and line[j].lower() == test_type:
            j += 1

        if i == j:
            j += 1

        while j < len(line):
            chr = line[i]
            next = line[j]
            if chr.islower() != next.islower() and chr.lower() == next.lower():
                # React
                line[i] = test_type
                line[j] = test_type
                reacted += 2

                # Go backwards to the latest unreacted, non-test character
                while i > 0 and line[i].lower() == test_type:
                    i -= 1

                if line[i].lower() is test_type:  # No characters before the reaction
                    while i < len(line) and line[i] == test_type:
                        i += 1

                while j < len(line) and line[j].lower() == test_type:
                    j += 1

                if i == j:  # In case the next character for is is j's pointer
                    j += 1
            else:
                j += 1
                i += 1
                # Move forward to the next unreacted, nontest character
                while i < len(line) and line[i].lower() == test_type:
                    i += 1

                while j < len(line) and line[j].lower() == test_type:
                    j += 1
        if reacted > worst_type[1]:
            worst_type = (test_type, reacted)

    line = list(raw)
    return len(raw) - worst_type[1] - line.count(worst_type[0]) - \
        line.count(worst_type[0].upper())


if __name__ == '__main__':
    print("Part 1: {}".format(main1()))
    print("Part 2: {}".format(main2()))
