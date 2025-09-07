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
    subsequences = list(map(int, data[1:]))

solutions = []
TARGET_STR = "GEOLYMP"
MAX_STR_LEN = 1000

def construct_string(K: int) -> str:
    letters = list("GEOLYMP")
    str_len = len(letters)
    counts = [1] * str_len  # factors for G,E,O,L,Y,M,P

    # Greedily distribute factors to keep counts balanced
    while math.prod(counts) < K:
        # choose index with minimal count
        i = min(range(str_len), key=lambda idx: counts[idx])
        counts[i] += 1

    # Build string
    result = "".join(letter * cnt for letter, cnt in zip(letters, counts))

    # Verify the solution
    assert math.prod(counts) == K, f"Product {math.prod(counts)} != {K}"
    assert len(result) <= 1000, f"String too long: {len(result)}"

    return result

def construct_string(K):
    # Use the base conversion method which guarantees the length constraint
    # Convert K to base-N where N is chosen to keep the sum of digits ≤ 994
    
    # We need 7 digits, so choose base such that 7 * (base-1) ≤ 994
    # This means base ≤ 994/7 + 1 ≈ 143
    base = 142  # Safe choice
    
    digits = []
    n = K
    for i in range(7):
        digits.append(n % base)
        n //= base
    
    # If there's any remainder, add it to the last digit
    if n > 0:
        digits[-1] += n * base
    
    # Reverse to get the correct order
    digits = digits[::-1]
    
    # Ensure no digit is 0 (we need at least 1 of each character)
    for i in range(7):
        if digits[i] == 0:
            digits[i] = 1
    
    # Build the string
    target = "GEOLYMP"
    parts = []
    for i, char in enumerate(target):
        parts.append(char * digits[i])
        if i < len(target) - 1:
            parts.append('X')
    return ''.join(parts)

for case_no, sub_val in enumerate(subsequences, 1):
    full_string = construct_string(sub_val)
    solutions.append(f"Case #{case_no}: {full_string}")
    # print(solutions[-1], len(full_string))
    print(case_no, len(full_string))

output_file = "problem-sep-25-long-L-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions))

