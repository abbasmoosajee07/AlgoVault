"""Eldarverse Puzzles - Problem I
Solution Started: September 5,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-I
Solution by: Abbas Moosajee
Brief: [Friend Suggestions]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict

# Load input file
input_file = "problem-sep-25-long-I-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def parse_raw_data(raw_data):
    parsed_data = []
    new_test = True
    for line_no, line_data in enumerate(raw_data[1:], 1):
        if new_test:
            usernames, operations = [], []
            N, M = tuple(map(int, line_data.split()))
            add_usernames = N + line_no
            add_operations = M + N + line_no
            new_test = False
        elif line_no <= add_usernames:
            usernames.append(line_data.strip(" "))
        elif line_no <= add_operations:
            operations.append(tuple(line_data.split()))
            if line_no == add_operations:
                new_test = True
                parsed_data.append([usernames, operations])
    return parsed_data

class SocialNetwork:
    def __init__(self, all_usernames):
        self.usernames = all_usernames
        self.network_dict = defaultdict(set)
        for user in all_usernames:
            self.network_dict[user] = set()

    @staticmethod
    def is_lexicographically_smaller(A: str, B: str) -> bool:
        """
        Returns True if string A is lexicographically smaller than B,
        False otherwise.
        """
        n, m = len(A), len(B)
        min_len = min(n, m)

        # Compare character by character
        for i in range(min_len):
            if A[i] < B[i]:  # earlier in alphabet
                return True
            elif A[i] > B[i]:  # later in alphabet
                return False

        # If all characters so far are equal,
        # then shorter string is smaller (prefix rule).
        return n < m

    def run_operations(self, all_operations):
        suggested_friends = []
        for operation in all_operations:
            if operation[0] == "ADD":
                name1, name2 = operation[1], operation[2]
                self.network_dict[name1].add(name2)
                self.network_dict[name2].add(name1)
            elif operation[0] == "REMOVE":
                name1, name2 = operation[1], operation[2]
                self.network_dict[name1].remove(name2)
                self.network_dict[name2].remove(name1)
            elif operation[0] == "SUGGEST":
                name_x = operation[1]
                friends_x = self.network_dict[name_x]
                potential = defaultdict(list)
                for user_y, friends_y in self.network_dict.items():
                    if user_y in friends_x or name_x == user_y:
                        continue
                    mutuals = friends_x & friends_y
                    potential[len(mutuals)].append(user_y)

                if not potential:
                    continue  # no suggestions

                # Pick the candidates with the maximum mutuals
                max_mutual = max(potential.keys())
                chosen = potential[max_mutual]

                # Tie-break: lexicographically smallest using our function
                suggested = chosen[0]
                for candidate in chosen[1:]:
                    if self.is_lexicographically_smaller(candidate, suggested):
                        suggested = candidate

                suggested_friends.append(suggested)
        return '\n'.join(suggested_friends)

test_cases = parse_raw_data(data)
solutions = []

for case_no, case_data in enumerate(test_cases, start = 1):
    usernames, operations = case_data
    case_network = SocialNetwork(usernames)
    suggested_friends = case_network.run_operations(operations)
    solutions.append(f"Case #{case_no}:\n" + suggested_friends)
    print(solutions[-1])


output_file = "problem-sep-25-long-I-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions))

