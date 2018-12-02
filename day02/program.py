def read_input():
    with open("input.txt") as f:
        for line in f:
            yield line


def main1():
    twos = 0
    threes = 0
    for line in read_input():
        twod = False
        threed = False
        for letter in set(list(line)):
            if line.count(letter) == 2 and not twod:
                twos += 1
                twod = True
            if line.count(letter) == 3 and not threed:
                threes += 1
                threed = True
    return twos * threes


def other_endian_sorter(key):
    return "".join(list(reversed(key)))


def check_inputs(inputs):
    # Compares successive elements from the inputs list for a single character
    #   difference, and returns the non-unique characters in the pair as a str,
    #   or None if it fails to find a pair
    i = 0
    while i + 1 < len(inputs):
        first = inputs[i]
        second = inputs[i + 1]
        j = 0

        while j < len(first) and j < len(second):
            if second.startswith(first[:j]) and \
                    second.endswith(first[j+1:]) and \
                    len(first) == len(second):
                return first[:j] + first[j+1:]
            j += 1
        i += 1

    return None


def main2():
    inputs = sorted(read_input())  # Front-to-back sort
    output = check_inputs(inputs)
    if output is not None:
        return output

    inputs = sorted(read_input(), key=other_endian_sorter)  # Back-to-front sort
    output = check_inputs(inputs)
    if output is not None:
        return output

    return None


if __name__ == '__main__':
    print("Part 1: {}".format(main1()))
    print("Part 2: {}".format(main2()))
