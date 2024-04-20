import numpy as np
import matplotlib.pyplot as plt

import subprocess
import tempfile
import sys
import os
import re


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


def plot_data(problem_sizes: np.ndarray, times: np.ndarray, memories: np.ndarray, method: str) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(problem_sizes, times, marker='o', linestyle='-', label=f'{method} CPU Time (ms)')
    plt.xlabel('Problem Size (m+n)')
    plt.ylabel('CPU Time (milliseconds)')
    plt.title(f'CPU Time vs. Problem Size for {method} Method')
    plt.legend()
    plt.savefig(os.path.join('results', f'{method}_cpu_time_vs_problem_size.png'))
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(problem_sizes, memories, marker='o', linestyle='-', label=f'{method} Memory Usage (KB)')
    plt.xlabel('Problem Size (m+n)')
    plt.ylabel('Memory Usage (KB)')
    plt.title(f'Memory Usage vs. Problem Size for {method} Method')
    plt.legend()
    plt.savefig(os.path.join('results', f'{method}_memory_usage_vs_problem_size.png'))
    plt.close()


def main():
    assert len(sys.argv) == 2
    method = sys.argv[1]

    assert method in ("basic", "efficient"), ValueError(f"Unknown method: {method}")

    print("Method: {}".format(method))

    in_files = os.listdir("datapoints")
    in_files.sort(key=extract_index)

    problem_sizes = []
    times = []
    memories = []

    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file_path = temp_file.name
        for in_file in in_files:
            path = os.path.join("datapoints", in_file)
            problem_size = get_problem_size(path)
            subprocess.run(["python3", f"{method}_3.py", path, temp_file_path], text=True, capture_output=True)

            time, memory = read_expected_output(temp_file_path)

            problem_sizes.append(problem_size)
            times.append(time)
            memories.append(memory)

    problem_sizes = np.array(problem_sizes)
    times = np.array(times)
    memories = np.array(memories)

    plot_data(problem_sizes, times, memories, method)


if __name__ == '__main__':
    main()
