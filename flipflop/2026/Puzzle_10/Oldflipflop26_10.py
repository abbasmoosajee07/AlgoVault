"""FlipFlop 2026: BitFlop Internship - Puzzle 10
Solution Started: July 29, 2026
Puzzle Link: https://flipflop.slome.org/2026/10
Solution by: Abbas Moosajee
Brief: [The Banena™ Programming Language]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque, Counter
import time

# Load input file
input_file = "puzzle_10_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

class BanenaProg:

    def __init__(self, main_prog):
        self.registers = [0] * 16
        self.pointer = 0
        self.main_prog = main_prog
        self.labels = {}

    @staticmethod
    def process_line(raw_line):
        if raw_line.startswith("ba"):
            stripped = raw_line.replace("ba", "", 1)
            na_split = stripped.split("ne")
        elif raw_line.startswith("be"):
            stripped = raw_line.replace("be", "", 1)
            na_split = stripped.split("ne")
        else:
            raise ValueError(f"Invalid line: {raw_line}")
        return na_split

    def count_nas(self, base_str):
        mapped = []
        for targ in base_str:
            na_count = targ.count("na")
            mapped.append(na_count)
        return mapped[0], mapped[1:]

    def preprocess_labels(self):
        self.labels = {}
        for idx, line in enumerate(self.main_prog):
            if line.startswith("be"):
                parsed = self.process_line(line)
                label_id, _ = self.count_nas(parsed)
                self.labels[label_id] = idx + 1

    def op_function(self, op, map_targ):
        MOD = 65536
        if op == 0:
            self.registers[map_targ[1]] = map_targ[0] % MOD
        elif op == 1:
            self.registers[map_targ[1]] = self.registers[map_targ[0]] % MOD
        elif op == 2:
            self.registers[map_targ[2]] = (self.registers[map_targ[0]] + self.registers[map_targ[1]]) % MOD
        elif op == 3:
            self.registers[map_targ[2]] = (self.registers[map_targ[0]] - self.registers[map_targ[1]]) % MOD
        elif op == 4:
            self.registers[map_targ[2]] = (self.registers[map_targ[0]] * self.registers[map_targ[1]]) % MOD
        elif op == 5:
            divisor = self.registers[map_targ[1]]
            if divisor == 0:
                self.registers[map_targ[2]] = 0
            else:
                self.registers[map_targ[2]] = (self.registers[map_targ[0]] % divisor) % MOD
        elif op == 6:
            self.registers[map_targ[0]] = (self.registers[map_targ[0]] + 1) % MOD
        elif op == 7:
            self.registers[map_targ[0]] = (self.registers[map_targ[0]] - 1) % MOD
        elif op == 8:
            return self.labels[map_targ[0]]
        elif op == 9:
            if self.registers[map_targ[0]] == 0:
                return self.labels[map_targ[1]]
        elif op == 10:
            if self.registers[map_targ[0]] != 0:
                return self.labels[map_targ[1]]
        return self.pointer + 1

    def run_program(self):
        self.pointer = 0
        self.preprocess_labels()
        self.counter = 0
        visited = set()

        while self.pointer < len(self.main_prog):
            self.counter += 1
            state = (self.pointer, tuple(self.registers))
            if state in visited:
                return False
            visited.add(state)
            if self.counter >= 5000000:
                return False
            line = self.main_prog[self.pointer]

            if line.startswith("be"):
                # Labels are not executed, just skip over them
                self.pointer += 1
                continue

            parsed = self.process_line(line)
            op_code, map_codes = self.count_nas(parsed)
            post_jump = self.op_function(op_code, map_codes)
            self.pointer = post_jump

        return self.registers

def run_tests(base_prog):
    infinite_count = 0
    run_count = 0
    for init_r0 in range(99 + 1):
        start_time = time.time()
        run_count += 1
        test_banena = BanenaProg(base_prog)
        test_banena.registers[0] = init_r0
        completed = test_banena.run_program()
        print(f"R={run_count}, Time={time.time() - start_time:.5f}s, ({init_r0}, {test_banena.counter})")
        if completed is False:
            infinite_count += 1
            print(f"Cycle Detected IC={infinite_count}")
    return infinite_count

def run_tests_p3(base_prog):
    infinite_count = 0
    run_count = 0
    for init_r1 in range(3 + 1):
        r1_time = time.time()
        for init_r0 in range(65535 + 1): # 65535
            start_time = time.time()
            run_count += 1
            test_banena = BanenaProg(base_prog)
            test_banena.registers[0] = init_r0
            test_banena.registers[1] = init_r1
            completed = test_banena.run_program()
            if init_r0 % 1000 == 0:
                print(f"R={run_count}, Time={time.time() - start_time:.5f}s,IC={infinite_count}, (({init_r1},{init_r0}), {test_banena.counter})")
            if completed is False:
                infinite_count += 1
        print(f"R1 = {init_r1}, IC={infinite_count}, Time={time.time() - r1_time:.5f}s")
    return infinite_count

print("FlipFlop 2026, Puzzle 10")
print("Part 1:", BanenaProg(data).run_program()[0])
# print("Part 2:", run_tests(data))
# print("Part 3:", run_tests_p3(data))
