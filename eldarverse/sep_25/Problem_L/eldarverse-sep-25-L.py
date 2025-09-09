"""Eldarverse Puzzles - Problem L
Solution Started: September 6,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-L
Solution by: Abbas Moosajee
Brief: [GEOLYMP]"""

#!/usr/bin/env python3
from pathlib import Path
import math, heapq
# Load input file
input_file = "problem-sep-25-long-L-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()
    test_cases = list(map(int, data[1:]))

def count_subseq(result, target_str):
    """Count subsequences equal to target_str in result."""
    m = len(target_str)
    dp = [0] * (m + 1)
    dp[0] = 1
    for ch in result:
        for j in range(m - 1, -1, -1):
            if ch == target_str[j]:
                dp[j + 1] += dp[j]
    return dp[m]

def construct_string(init_k, target_str, min_base=20, max_base=1000):
    the_best_output = None
    m = len(target_str)

    for BASE in range(min_base, max_base):
        K = init_k
        values = []
        while K > 0:
            values.append(K % BASE)
            K //= BASE

        result = []

        # D0: prefix (all but last char), then last-char repeated n (if present)
        n = values.pop(0) if values else None
        result += list(target_str[:-1])
        if n is not None:
            result += [target_str[-1]] * n

        # D1 .. D(m-2): for idx=1..m-2 append the appropriate left-to-right block
        # (this is the crucial loop: range stops at m-2 inclusive)
        for idx in range(1, m - 1):
            n = values.pop(0) if values else None
            # suffix of length idx before the last char, left-to-right
            suffix = target_str[-(idx + 1):-1]
            for ch in suffix:
                result += [ch] * (BASE - 1)
            if n is not None:
                result += [target_str[-1]] * n

        # verify
        total = count_subseq(result, target_str)
        if total == init_k:
            output = ''.join(result)
            if the_best_output is None or len(output) < len(the_best_output):
                the_best_output = output

    return the_best_output if the_best_output is not None else ""

solutions = []
for case_no, case_k in enumerate(test_cases, start=1):
    best_string = construct_string(case_k, "GEOLYMP")
    solutions.append(f"Case #{case_no}: {best_string}")
    # print(solutions[-1])
    print(case_no, case_k, len(best_string))

output_file = "problem-sep-25-long-L-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions))
