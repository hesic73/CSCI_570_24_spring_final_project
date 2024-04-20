from typing import Tuple

ALPHA = [
    [0, 110, 48, 94],
    [110, 0, 118, 48],
    [48, 118, 0, 110],
    [94, 48, 110, 0]
]

DELTA = 30


def basic(s: str, t: str) -> Tuple[int, str, str]:
    m, n = len(s), len(t)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

    index_s = [index[char] for char in s]
    index_t = [index[char] for char in t]

    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] + DELTA
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] + DELTA

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost_match = ALPHA[index_s[i - 1]][index_t[j - 1]]
            dp[i][j] = min(dp[i - 1][j - 1] + cost_match, dp[i - 1][j] + DELTA, dp[i][j - 1] + DELTA)

    aligned_s, aligned_t = "", ""
    i, j = m, n
    while i > 0 and j > 0:
        current = dp[i][j]
        if current == dp[i - 1][j - 1] + ALPHA[index_s[i - 1]][index_t[j - 1]]:
            aligned_s = s[i - 1] + aligned_s
            aligned_t = t[j - 1] + aligned_t
            i -= 1
            j -= 1
        elif current == dp[i - 1][j] + DELTA:
            aligned_s = s[i - 1] + aligned_s
            aligned_t = '_' + aligned_t
            i -= 1
        else:
            aligned_s = '_' + aligned_s
            aligned_t = t[j - 1] + aligned_t
            j -= 1

    while i > 0:
        aligned_s = s[i - 1] + aligned_s
        aligned_t = '_' + aligned_t
        i -= 1
    while j > 0:
        aligned_s = '_' + aligned_s
        aligned_t = t[j - 1] + aligned_t
        j -= 1

    # assert dp[m][n] == calculate_cost(aligned_s, aligned_t)

    return dp[m][n], aligned_s, aligned_t


def calculate_cost(aligned_s: str, aligned_t: str) -> int:
    assert len(aligned_s) == len(aligned_t)

    index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

    total_cost = 0

    for i in range(len(aligned_s)):
        char_s = aligned_s[i]
        char_t = aligned_t[i]

        if char_s != '_' and char_t != '_':
            total_cost += ALPHA[index[char_s]][index[char_t]]
        elif char_s == '_' or char_t == '_':
            total_cost += DELTA

    return total_cost


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
    _main(basic)
