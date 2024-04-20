import unittest

import random

from efficient_3 import efficient
from basic_3 import basic

index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}


def generate_dna_sequence(n: int) -> str:
    # Define the DNA characters
    dna_bases = 'ACGT'
    # Generate a random sequence of DNA bases
    sequence = ''.join(random.choices(dna_bases, k=n))
    return sequence


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


class TestEfficient(unittest.TestCase):
    def test_base_cases_1_100(self):
        for i in range(100):
            s = generate_dna_sequence(100)
            t = generate_dna_sequence(1)

            cost, aligned_s, aligned_t = efficient(s, t)
            self.assertEqual(cost, calculate_cost(aligned_s, aligned_t))
            expected_cost, *_ = basic(s, t)
            self.assertEqual(cost, expected_cost)

        for i in range(100):
            s = generate_dna_sequence(1)
            t = generate_dna_sequence(100)

            cost, aligned_s, aligned_t = efficient(s, t)
            self.assertEqual(cost, calculate_cost(aligned_s, aligned_t))
            expected_cost, *_ = basic(s, t)
            self.assertEqual(cost, expected_cost)

    def test_base_cases_1_1(self):
        for i in range(100):
            s = generate_dna_sequence(1)
            t = generate_dna_sequence(1)

            cost, aligned_s, aligned_t = efficient(s, t)
            self.assertEqual(cost, calculate_cost(aligned_s, aligned_t))
            expected_cost, *_ = basic(s, t)
            self.assertEqual(cost, expected_cost)

    def test_base_cases_1_2(self):
        for i in range(100):
            s = generate_dna_sequence(1)
            t = generate_dna_sequence(2)

            cost, aligned_s, aligned_t = efficient(s, t)
            self.assertEqual(cost, calculate_cost(aligned_s, aligned_t))
            expected_cost, *_ = basic(s, t)
            self.assertEqual(cost, expected_cost)

        for i in range(100):
            s = generate_dna_sequence(2)
            t = generate_dna_sequence(1)

            cost, aligned_s, aligned_t = efficient(s, t)
            self.assertEqual(cost, calculate_cost(aligned_s, aligned_t))
            expected_cost, *_ = basic(s, t)
            self.assertEqual(cost, expected_cost)

    def test_2_2(self):
        for i in range(1000):
            s = generate_dna_sequence(2)
            t = generate_dna_sequence(2)

            cost, aligned_s, aligned_t = efficient(s, t)
            self.assertEqual(cost, calculate_cost(aligned_s, aligned_t))
            expected_cost, *_ = basic(s, t)
            self.assertEqual(cost, expected_cost)

    def test_same_sequence(self):
        for i in range(100):
            s = generate_dna_sequence(100)
            t = s
            cost, s_aligned, t_aligned = efficient(s, t)
            self.assertEqual(cost, calculate_cost(s_aligned, t_aligned))
            self.assertEqual(cost, 0)

    def test_commutative_sequence(self):
        for i in range(100):
            s = generate_dna_sequence(random.randint(1, 100))
            t = generate_dna_sequence(random.randint(1, 100))

            cost_st, *_ = efficient(s, t)
            cost_ts, *_ = efficient(t, s)

            self.assertEqual(cost_st, cost_ts)

    def test_small(self):
        for i in range(100):
            s = generate_dna_sequence(random.randint(1, 10))
            t = generate_dna_sequence(random.randint(1, 10))

            cost, aligned_s, aligned_t = efficient(s, t)
            self.assertEqual(cost, calculate_cost(aligned_s, aligned_t))

            expected_cost, *_ = basic(s, t)
            self.assertEqual(cost, expected_cost)


    def test_largel(self):
        for i in range(10):
            s = generate_dna_sequence(random.randint(100, 1000))
            t = generate_dna_sequence(random.randint(100, 1000))

            cost, aligned_s, aligned_t = efficient(s, t)
            self.assertEqual(cost, calculate_cost(aligned_s, aligned_t))

            expected_cost, *_ = basic(s, t)
            self.assertEqual(cost, expected_cost)


if __name__ == '__main__':
    unittest.main()
