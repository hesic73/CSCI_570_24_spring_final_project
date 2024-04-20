import numpy as np
import matplotlib.pyplot as plt

import subprocess
import tempfile
import sys
import os
import re

from collections import defaultdict

from typing import Dict

from prettytable import PrettyTable

def get_problem_size(file_path: str) -> int:
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

    return len(s) + len(t)


def read_expected_output(path: str):
    with open(path, 'r') as file:
        lines = file.read().strip().split('\n')
        assert len(lines) == 5
        return float(lines[3]), float(lines[4])


def extract_index(filename: str) -> int:
    # Regular expression to find numbers in the filename
    match = re.search(r'\d+', filename)
    assert match
    return int(match.group(0))


def plot_data(problem_sizes: np.ndarray, times: Dict[str, np.ndarray], memories: Dict[str, np.ndarray]) -> None:
    # Create the CPU time plot with multiple methods
    plt.figure(figsize=(10, 5))
    for method, time in times.items():
        plt.plot(problem_sizes, time, marker='o', linestyle='-', label=f'{method}')
    plt.xlabel('Problem Size (m+n)')
    plt.ylabel('CPU Time (milliseconds)')
    plt.title('CPU Time vs. Problem Size')
    plt.legend()
    plt.savefig(os.path.join('results', 'cpu_time_vs_problem_size.png'))
    plt.close()

    # Create the Memory usage plot with multiple methods
    plt.figure(figsize=(10, 5))
    for method, memory in memories.items():
        plt.plot(problem_sizes, memory, marker='o', linestyle='-', label=f'{method}')
    plt.xlabel('Problem Size (m+n)')
    plt.ylabel('Memory Usage (KB)')
    plt.title('Memory Usage vs. Problem Size')
    plt.legend()
    plt.savefig(os.path.join('results', 'memory_usage_vs_problem_size.png'))
    plt.close()


METHODS = ("basic", )


def main():
    in_files = os.listdir("datapoints")
    in_files.sort(key=extract_index)

    problem_sizes = []
    times = defaultdict(list)
    memories = defaultdict(list)

    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file_path = temp_file.name
        for in_file in in_files:
            path = os.path.join("datapoints", in_file)
            problem_size = get_problem_size(path)
            problem_sizes.append(problem_size)

            for method in METHODS:
                subprocess.run(["python3", f"{method}_3.py", path, temp_file_path], text=True, capture_output=True)

                time, memory = read_expected_output(temp_file_path)

                times[method].append(time)
                memories[method].append(memory)

    problem_sizes = np.array(problem_sizes)
    times = {k: np.array(v) for k, v in times.items()}
    memories = {k: np.array(v) for k, v in memories.items()}

    for method in METHODS:
        table = PrettyTable()
        table.title = f"Method: {method}"
        table.field_names = ["Problem Size", "Time", "Memory"]
        for i, size in enumerate(problem_sizes):
            table.add_row([size, times[method][i], memories[method][i]])
        print(table)
        print("\n")

    plot_data(problem_sizes, times, memories)


if __name__ == '__main__':
    main()
