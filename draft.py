from efficient_3 import efficient
from basic_3 import basic


def calculate_cost(aligned_s: str, aligned_t: str) -> int:
    assert len(aligned_s) == len(aligned_t)
    ALPHA = [
        [0, 110, 48, 94],
        [110, 0, 118, 48],
        [48, 118, 0, 110],
        [94, 48, 110, 0]
    ]

    DELTA = 30

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


if __name__ == '__main__':
    s = "AT"
    t = "GA"

    expected_cost, x, y = basic(s, t)
    assert calculate_cost(x, y) == expected_cost
    print(expected_cost)
    print(x, y)

    cost, aligned_s, aligned_t = efficient(s, t)

    assert cost == expected_cost
