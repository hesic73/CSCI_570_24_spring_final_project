from typing import Tuple

import numpy as np

from common import _main
from consts import DELTA, ALPHA


def basic(s: str, t: str) -> Tuple[int, str, str]:
    m, n = len(s), len(t)
    dp = np.zeros((m + 1, n + 1), dtype=np.int64)

    index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] + DELTA
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] + DELTA

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost_match = ALPHA[index[s[i - 1]], index[t[j - 1]]]
            dp[i][j] = min(dp[i - 1][j - 1] + cost_match, dp[i - 1][j] + DELTA, dp[i][j - 1] + DELTA)

    aligned_s, aligned_t = "", ""
    i, j = m, n
    while i > 0 and j > 0:
        current = dp[i][j]
        if current == dp[i - 1][j - 1] + ALPHA[index[s[i - 1]], index[t[j - 1]]]:
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


if __name__ == '__main__':
    _main(basic)
