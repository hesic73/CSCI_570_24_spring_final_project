import unittest
import os

from typing import Tuple

from basic_3 import basic
from efficient_3 import efficient


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


def read_expected_output(path: str):
    with open(path, 'r') as file:
        lines = file.read().strip().split('\n')
        return int(lines[0]), lines[1], lines[2]


class TestFromFiles(unittest.TestCase):

    def setUp(self):
        # Define the base directory for test files
        self.test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'SampleTestCases')

    def test_basic(self):
        test_files = os.listdir(self.test_data_dir)
        # Filter out input files
        input_files = [f for f in test_files if f.startswith('input')]
        input_files.sort()

        for input_file in input_files:
            # Construct full path for input and expected output files
            input_file_path = os.path.join(self.test_data_dir, input_file)
            output_file_path = os.path.join(self.test_data_dir, f'output{input_file[-5:]}')

            s, t = generate_input_strings(input_file_path)
            cost, first_string_alignment, second_string_alignment = basic(s, t)

            expected_cost, expected_first_string_alignment, expected_second_string_alignment = read_expected_output(
                output_file_path)

            self.assertEqual(cost, expected_cost)
            # self.assertEqual(first_string_alignment, expected_first_string_alignment)
            # self.assertEqual(second_string_alignment, expected_second_string_alignment)

    def test_efficient(self):
        test_files = os.listdir(self.test_data_dir)
        # Filter out input files
        input_files = [f for f in test_files if f.startswith('input')]

        for input_file in input_files:
            # Construct full path for input and expected output files
            input_file_path = os.path.join(self.test_data_dir, input_file)
            output_file_path = os.path.join(self.test_data_dir, f'output{input_file[-5:]}')

            s, t = generate_input_strings(input_file_path)
            cost, first_string_alignment, second_string_alignment = efficient(s, t)

            expected_cost, expected_first_string_alignment, expected_second_string_alignment = read_expected_output(
                output_file_path)

            self.assertEqual(cost, expected_cost)
            # self.assertEqual(first_string_alignment, expected_first_string_alignment)
            # self.assertEqual(second_string_alignment, expected_second_string_alignment)


if __name__ == '__main__':
    unittest.main()
