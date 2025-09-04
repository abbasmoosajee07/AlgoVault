"""Eldarverse Puzzles - Problem B
Solution Started: September 4,
Puzzle Link: https://www.eldarverse.com/problem/B
Solution by: Abbas Moosajee
Brief: [Sparse Rankings]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "problem-sep-25-long-B-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()
    tournaments = [tuple(map(int, line.split())) for line in data[1:]]


from collections import Counter

def possible_point_distributions(N: int):
    """
    Dynamic programming to get all possible point distributions
    without enumerating 2^(N*(N-1)) tables.
    """
    matches = [(i, j) for i in range(N) for j in range(N) if i != j]
    dp = Counter()
    dp[(0,) * N] = 1  # start: all teams 0 points

    for (i, j) in matches:
        new_dp = Counter()
        for scores, count in dp.items():
            scores = list(scores)

            # case 1: home team wins
            s1 = scores[:]
            s1[i] += 1
            new_dp[tuple(s1)] += count

            # case 2: away team wins
            s2 = scores[:]
            s2[j] += 1
            new_dp[tuple(s2)] += count

        dp = new_dp

    return dp

possible_rankings = {}
for TEST_N in range(2, 6 + 1):
    dist = possible_point_distributions(TEST_N)
    possible_rankings[TEST_N] = dist

solutions = []
for t_no, (N, K) in enumerate(tournaments, start=1):
    count_t = 0
    for rankings, cnt in list(possible_rankings[N].items()):
        sparse = max(rankings) - min(rankings)
        if sparse > K:
            count_t += cnt
    solutions.append(f"Case #{t_no}: {count_t}")
    print(solutions[-1])


output_file = "problem-sep-25-long-B-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions) + "\n")