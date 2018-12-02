def read_input():
    with open("input.txt") as f:
        for line in f:
            yield line


def main1():
    total = 0

    for line in read_input():
        num = int(line)
        total += num

    return total


def main2():
    total = 0
    freqs = set([0])

    while True:
        for line in read_input():
            num = int(line)
            total += num

            if total in freqs:
                return total
            else:
                freqs.add(total)


if __name__ == '__main__':
    print("Part 1: {}".format(main1()))
    print("Part 2: {}".format(main2()))
