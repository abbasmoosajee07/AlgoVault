"""Eldarverse Puzzles - Problem 1C
Solution Started: October 27,
Puzzle Link: https://www.eldarverse.com/problem/halloween25-1C
Solution by: Abbas Moosajee
Brief: [Werewolf Scribes (part 2)]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
from itertools import chain
import heapq
# Load input file
input_file = "problem-halloween25-1C-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def calculate_strength_v0(total_nights, pattern, A, B, M):
    def strength_eq(xi_1 = 0):
        return ((xi_1 * A) + B) % (2 ** 20)

    median_history = 0
    clan_dict = defaultdict(list)
    prev_strength = 0
    for night_i in range(1,  total_nights + 1):
        wolf_i = (night_i - 1) % len(pattern)
        wolf = int(pattern[wolf_i])
        wolf_strength = strength_eq(prev_strength)
        clan_dict[wolf].append(wolf_strength)
        prev_strength = wolf_strength
        if night_i % 1000 == 0:
            print(f"{night_i=}, {wolf=}, {wolf_strength=}")

        if night_i % M == 0:
            clan_members = clan_dict[wolf]
            clan_dict[wolf] = [n + 1 for n in clan_members]
        median_strength = median(list(chain.from_iterable(clan_dict.values())))
        if night_i % 1000 == 0:
            print(f"{night_i=}, {median_history} {median_strength}")
        median_history += median_strength
    return median_history

def median(data):
    sorted_data = sorted(data)
    n = len(data)
    if n % 2 == 1:  # Odd length
        median_value = sorted_data[n // 2]
    else:  # Even length
        median_value = sorted_data[n // 2 - 1]
    return median_value

def calculate_strength_v1(total_nights, pattern, A, B, M):
    def strength_eq(xi_1):
        return ((xi_1 * A) + B) & ((1 << 20) - 1)

    # Heaps for median tracking
    low, high = [], []  # max-heap (negated), min-heap
    clan_offsets = defaultdict(int)
    clan_members = defaultdict(list)

    def add_value(val):
        if not low or val < -low[0]:
            heapq.heappush(low, -val)
        else:
            heapq.heappush(high, val)
        # rebalance
        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))

    def current_median():
        if len(low) == len(high):
            return -low[0]
        else:
            return -low[0]

    prev_strength = 0
    median_sum = 0
    test_med = []

    for night_i in range(1, total_nights + 1):
        wolf_i = (night_i - 1) % len(pattern)
        wolf = int(pattern[wolf_i])

        wolf_strength = strength_eq(prev_strength)
        prev_strength = wolf_strength

        # store in clan
        clan_members[wolf].append(wolf_strength)

        # increment clan offset every M nights
        if (night_i - 0) % M == 0:
            clan_offsets[wolf] += 1

        add_value(wolf_strength + clan_offsets[wolf])

        median_sum += current_median()
        # test_med.append(current_median())
    # print(test_med)
    return median_sum


def calculate_strength_v2(N, S, A, B, M):
    N, A, B, M = int(N), int(A), int(B), int(M)
    pattern_len = len(S)

    low, high = [], []  # max-heap, min-heap
    clan_increments = defaultdict(int)
    Xi = 0
    ans = 0

    for i in range(1, N + 1):
        Xi = (Xi * A + B) % (1 << 20)
        clan = S[(i - 1) % pattern_len]
        strength = Xi + clan_increments[clan]

        # insert into heaps
        if not low or strength <= -low[0]:
            heapq.heappush(low, -strength)
        else:
            heapq.heappush(high, strength)

        # rebalance
        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))

        # get base median
        median = -low[0]

        # if blood moon: increment now, affects *current* median
        if i % M == 0:
            clan_increments[clan] += 1
            median += 1  # because this clan's members just got +1

        ans += median        # print(f"Case #{t}: {ans}")
    return ans



solutions = []

for case_no, case_data in enumerate(data[1:], start=1):
    N, A, B, M, S = case_data.split(" ")
    if case_no in [1, 2, 3, 4]:
        calculate_strength = calculate_strength_v0
    else:
        calculate_strength = calculate_strength_v2
    case_strength = calculate_strength(int(N), list(S), int(A), int(B), int(M))
    solutions.append(f"Case #{case_no}: {(case_strength)}")
    print(solutions[-1])

output_file = "problem-halloween25-1C-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions) + "\n")