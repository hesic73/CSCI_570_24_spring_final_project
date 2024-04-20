from typing import Tuple, List

# ACGT
ALPHA = [
    [0, 110, 48, 94],
    [110, 0, 118, 48],
    [48, 118, 0, 110],
    [94, 48, 110, 0]
]

DELTA = 30

INF = int(1 << 31)


def efficient(s: str, t: str) -> Tuple[int, str, str]:
    index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    index_s = [index[char] for char in s]
    index_t = [index[char] for char in t]
    cost, aligned_s, aligned_t = _efficient(s, t, index_s, index_t, 0, len(s), 0, len(t))

    return cost, aligned_s, aligned_t


def _efficient(s: str, t: str, index_s: List[int], index_t: List[int], start_s: int, end_s: int, start_t: int,
               end_t: int) -> Tuple[int, str, str]:
    assert start_s <= end_s
    assert start_t <= end_t

    # base cases
    if start_s == end_s:
        return (end_t - start_t) * DELTA, '_' * (end_t - start_t), t[start_t:end_t]
    if start_t == end_t:
        return (end_s - start_s) * DELTA, s[start_s:end_s], '_' * (end_s - start_s)

    # The tricky part is that (A, C) 's optimal alignment is (_A, C_).

    if start_s + 1 == end_s:
        min_cost = INF
        min_idx = -1
        for i in range(start_t, end_t):
            cost = ALPHA[index_s[start_s]][index_t[i]]
            if cost < min_cost:
                min_cost = cost
                min_idx = i

        min_cost += (end_t - start_t - 1) * DELTA

        cost_all_gaps = DELTA * (1 + end_t - start_t)
        if min_cost < cost_all_gaps:
            aligned_s = '_' * (min_idx - start_t) + s[start_s] + '_' * (end_t - min_idx - 1)
            aligned_t = t[start_t:end_t]

            return min_cost, aligned_s, aligned_t

        else:
            return cost_all_gaps, s[start_s] + '_' * (end_t - start_t), '_' + t[start_t:end_t]

    if start_t + 1 == end_t:
        min_cost = INF
        min_idx = -1
        for i in range(start_s, end_s):
            cost = ALPHA[index_s[i]][index_t[start_t]]
            if cost < min_cost:
                min_cost = cost
                min_idx = i
        min_cost += (end_s - start_s - 1) * DELTA

        cost_all_gaps = DELTA * (1 + end_s - start_s)

        if min_cost < cost_all_gaps:
            aligned_s = s[start_s:end_s]
            aligned_t = '_' * (min_idx - start_s) + t[start_t] + '_' * (end_s - min_idx - 1)

            return min_cost, aligned_s, aligned_t

        else:
            return cost_all_gaps, '_' + s[start_s:end_s], t[start_t] + '_' * (end_s - start_s)

    # divide-and-conquer

    mid_s = (start_s + end_s) // 2

    # cost_from_start[i]: cost(s[start_s:mid_s],t[start_t:start_t+i])
    cost_from_start = calculate_cost_from_start(index_s, index_t, start_s, mid_s, start_t, end_t)

    # cost_to_end[i]: cost(s[mid_s:end_s],t[end_t-i:end_t])
    cost_to_end = calculate_cost_to_end(index_s, index_t, mid_s, end_s, start_t, end_t)

    min_cost = INF
    split_t = -1
    for i in range(0, end_t - start_t + 1):
        total_cost = cost_from_start[i] + cost_to_end[end_t - start_t - i]
        if total_cost < min_cost:
            min_cost = total_cost
            split_t = start_t + i

    # s[start_s:mid_s]  t[start_t:split_t]
    # s[mid_s:end_s]  t[split_t:end_t]

    cost_left, aligned_left_s, aligned_left_t = _efficient(s, t, index_s, index_t, start_s, mid_s, start_t,
                                                           split_t)
    cost_right, aligned_right_s, aligned_right_t = _efficient(s, t, index_s, index_t, mid_s, end_s, split_t,
                                                              end_t)

    assert cost_left + cost_right == min_cost

    aligned_s = aligned_left_s + aligned_right_s
    aligned_t = aligned_left_t + aligned_right_t

    return cost_left + cost_right, aligned_s, aligned_t


def calculate_cost_from_start(index_s: List[int], index_t: List[int], start_s: int, end_s: int, start_t: int,
                              end_t: int) -> List[int]:
    dp = [INF] * (end_t - start_t + 1)
    dp[0] = 0

    for j in range(1, end_t - start_t + 1):
        dp[j] = j * DELTA
    for i in range(1, end_s - start_s + 1):
        tmp = dp[:]
        dp[0] = i * DELTA
        for j in range(1, end_t - start_t + 1):
            a = dp[j - 1] + DELTA
            b = tmp[j] + DELTA
            c = tmp[j - 1] + ALPHA[index_s[start_s + i - 1]][index_t[start_t + j - 1]]
            dp[j] = min(a, b, c)

    return dp


def calculate_cost_to_end(index_s: List[int], index_t: List[int], start_s: int, end_s: int, start_t: int, end_t: int) -> \
List[int]:
    dp = [INF] * (end_t - start_t + 1)
    dp[0] = 0

    for j in range(1, end_t - start_t + 1):
        dp[j] = j * DELTA

    for i in range(1, end_s - start_s + 1):
        tmp = dp[:]
        dp[0] = i * DELTA
        for j in range(1, end_t - start_t + 1):
            a = dp[j - 1] + DELTA
            b = tmp[j] + DELTA
            c = tmp[j - 1] + ALPHA[index_s[end_s - i]][index_t[end_t - j]]
            dp[j] = min(a, b, c)

    return dp


import sys
import time
import psutil
from typing import Tuple, Callable

FunctionType = Callable[[str, str], Tuple[int, str, str]]


def process_memory() -> int:
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def generate_input_strings(file_path: str) -> Tuple[str, str]:
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    s = lines[0]
    t = None
    flag = True

    for line in lines[1:]:
        if line.isdigit():
            i = int(line)
            if flag:
                s = s[:i + 1] + s + s[i + 1:]
            else:
                t = t[:i + 1] + t + t[i + 1:]
        else:
            if flag:
                t = line
                flag = False

    return s, t


def _main(func: FunctionType) -> None:
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file_path> <output_file_path>")
        sys.exit(1)
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    s, t = generate_input_strings(input_file_path)

    start_time = time.time()
    cost, first_string_alignment, second_string_alignment = func(s, t)
    end_time = time.time()
    time_elapsed = (end_time - start_time) * 1000

    process_memory_consumed = process_memory()

    with open(output_file_path, 'w') as file:
        file.write(
            f"{cost}\n{first_string_alignment}\n{second_string_alignment}\n{time_elapsed}\n{process_memory_consumed}\n")


if __name__ == '__main__':
    _main(efficient)
