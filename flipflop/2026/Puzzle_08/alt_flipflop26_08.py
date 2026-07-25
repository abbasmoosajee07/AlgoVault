"""FlipFlop 2026: BitFlop Internship - Puzzle 8
Solution Started: July 25, 2026
Puzzle Link: https://flipflop.slome.org/2026/8
Solution by: Abbas Moosajee
Brief: [The Amazing Digital Stoats]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
# Load input file
input_file = "puzzle_08_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

data1 = ['A A C', 'A B C', 'A C B', 'B B A B A', 'B C B A', 'C C B B']

class DigitalStoats:
    def __init__(self, rules):
        self.rules = rules

    def basic_evolution(self, total_gens, base = "AB"):
        rules_dict = defaultdict(list)
        for rule_Str in self.rules:
            stripped_rule = rule_Str.replace(" ", "")
            rules_dict[stripped_rule[0]].append(stripped_rule[1:])
        for gen_no in range(1, total_gens + 1):
            next_gen = ""
            for parent in base:
                next_gen += rules_dict[parent][0]
            base = next_gen
            # print(f"Gen {gen_no}: {len(base)} in length")
        return len(base)

    def two_stoat_evolution(self, total_gens, base = "AB"):
        rules_dict = defaultdict(list)
        for rule_Str in self.rules:
            stripped_rule = rule_Str.replace(" ", "")
            key, value = stripped_rule[:2], stripped_rule[2:]
            rules_dict[key].append(value)
            rules_dict[key[::-1]].append(value)
        for gen_no in range(1, total_gens + 1):
            next_gen = base[0]
            idx = 0
            for parent_1, parent_2 in zip(base[:-1], base[1:]):
                idx += 1
                child = rules_dict[parent_1 + parent_2][0]
                next_gen += child + parent_2
                if len(next_gen) % 1000000 == 0:
                    print(f"Gen {gen_no}: {idx} / {len(base)} | New = {len(next_gen)}")
            base = next_gen
            print(f"Gen {gen_no}: {len(base)} in length")
        return len(base)

stoats = DigitalStoats(data)
print("FlipFlop 2026, Puzzle 08")
print("Part 1:", stoats.basic_evolution(7))
print("Part 2:", stoats.two_stoat_evolution(7))
print("Part 2:", stoats.two_stoat_evolution(21))