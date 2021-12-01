from utils import get_input_data


def part1(data: list[int] = None) -> int:
    if not data:
        data = [int(x) for x in get_input_data(1).split("\n") if x]
    count_diff = 0
    prev_val = data[0]
    for i in range(1, len(data)):
        cur_val = data[i]
        if cur_val > prev_val:
            count_diff += 1
        prev_val = cur_val
    return count_diff


def part2(data: list[int] = None) -> int:
    if not data:
        data = [int(x) for x in get_input_data(1).split("\n") if x]
    count_diff = 0
    prev_val = sum(data[0:3])
    for i in range(1, len(data) - 2):
        cur_val = sum(data[i:i+3])
        if cur_val > prev_val:
            count_diff += 1
        prev_val = cur_val
    return count_diff
