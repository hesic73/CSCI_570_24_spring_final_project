from typing import Tuple

import numpy as np

ALPHA = np.array([
    [0, 110, 48, 94],
    [110, 0, 118, 48],
    [48, 118, 0, 110],
    [94, 48, 110, 0]
]).astype(np.int32)

DELTA = np.array(30).astype(np.int32)

# Using Numba significantly accelerates computation, such that for small-scale problems, the execution time is nearly constant despite the theoretical quadratic time complexity.
# from numba import njit


# @njit
def _compute_dp(m: int, n: int, dp: np.ndarray, index_s: np.ndarray, index_t: np.ndarray, alpha: np.ndarray,
                delta: np.ndarray) -> np.ndarray:
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost_match = alpha[index_s[i - 1], index_t[j - 1]]
            dp[i][j] = min(dp[i - 1][j - 1] + cost_match, dp[i - 1][j] + delta, dp[i][j - 1] + delta)
    return dp


def basic(s: str, t: str) -> Tuple[int, str, str]:
    m, n = len(s), len(t)
    dp = np.zeros((m + 1, n + 1), dtype=np.int32)

    index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

    index_s = np.array([index[char] for char in s])
    index_t = np.array([index[char] for char in t])

    dp[1:, 0] = np.arange(1, m + 1) * DELTA
    dp[0, 1:] = np.arange(1, n + 1) * DELTA

    dp = _compute_dp(m, n, dp, index_s, index_t, ALPHA, DELTA)

    aligned_s, aligned_t = "", ""
    i, j = m, n
    while i > 0 and j > 0:
        current = dp[i][j]
        if current == dp[i - 1][j - 1] + ALPHA[index_s[i - 1], index_t[j - 1]]:
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

    return int(dp[m][n]), aligned_s, aligned_t


import sys
import time
import psutil
from typing import Tuple, Callable

FunctionType = Callable[[str, str], Tuple[int, str, str]]


def process_memory() -> int:
    process = psutil.Process()
    memory_info = process.memory_info()
    print(memory_info)
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
