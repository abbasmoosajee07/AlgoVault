"""Codyssi Puzzles - Problem 17
Solution Started: May 10, 2025
Puzzle Link: https://www.codyssi.com/view_problem_21?
Solution by: Abbas Moosajee
Brief: [Spiralling Stairs]
"""

#!/usr/bin/env python3

import os, re, copy, time
start_time = time.time()
from functools import cache

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    steps = input_data[0].split("\n")
    possible_moves = list(map(int, (input_data[1].split(":")[1]).strip().split(",")))

class Staircase:
    def __init__(self, steps, possible_moves):
        self.staircase_data = {data[0]: data for line in steps for data in [self.__parse_step(line)]}
        self.valid_moves = possible_moves

        basic_structure = {}
        for branch in self.staircase_data.values():
            basic_structure = self.__build_staircase(basic_structure, branch)

        self.basic_structure = basic_structure.copy()
        self.expanded_structure = self.__identify_shortcuts(basic_structure.copy())

    def __parse_step(self, raw_info):
        info_list = raw_info.split()
        useful = (info_list[0], int(info_list[2]), int(info_list[4]),
                    info_list[7], info_list[9])
        return useful

    def identify_start_end(self, target_step):
        start_point = f"{target_step}_{self.staircase_data[target_step][1]}"
        end_point = f"{target_step}_{self.staircase_data[target_step][2]}"
        return start_point, end_point

    def __build_staircase(self, structure, stair_info):
        """ `S{X} : {N1} -> {N2} : FROM S{A} TO S{B}` """
        S_X, N1, N2, S_A, S_B = stair_info

        sx_start, sx_end = f"{S_X}_{N1}",  f"{S_X}_{N2}"
        branch_point, return_point = f"{S_A}_{N1}",  f"{S_B}_{N2}"
        if S_A != "START" or S_B != "END":
            structure.setdefault(branch_point, set()).add((sx_start, 1))
            structure.setdefault(sx_end, set()).add((return_point, 1))

        avail_steps = list(range(N1, N2 + 1))
        for step_idx, start_step in enumerate(avail_steps):
            fwd_steps = avail_steps[step_idx + 1:]
            for next_idx, next_step in enumerate(fwd_steps, start=1):
                if next_idx in self.valid_moves:
                    structure.setdefault(f"{S_X}_{start_step}", set()).add((f"{S_X}_{next_step}", next_idx))

        return structure

    def __identify_shortcuts(self, structure):

        def step_tracker(base_step, standing_step):
            for connected_step in structure.get(standing_step[0], []):
                next_move = (connected_step[0], standing_step[1] + connected_step[1])
                if next_move[1] > max(valid_moves):
                    continue
                step_tracker(base_step, next_move)  # Recurse properly
                if any(next_move[0] == move for move, _ in complete_moves[base_step]):
                    continue
                if next_move[1] in valid_moves:
                    complete_moves.setdefault(base_step, set()).add(next_move)

        complete_moves =  structure.copy()
        valid_moves = self.valid_moves

        for base_step in structure:
            for next_step in list(complete_moves[base_step]):
                step_tracker(base_step, next_step)

        return complete_moves

    def __dfs_algorithm(self, current, end_step, structure, history = {}, multi_level = True):
        if current == end_step: # If current is final step, count 1
            history[current] = 1
            return 1
        if current in history: # If current is in history return to that point
            return history[current]
        total = 0
        for (next_step, mag) in structure.get(current, []):
            if multi_level:
                total += self.__dfs_algorithm(next_step, end_step, structure, history, multi_level)
            else:
                current_branch = int(current.split('_')[0][1:])
                next_branch = int(next_step.split('_')[0][1:])
                if current_branch != next_branch:
                    continue
                total += self.__dfs_algorithm(next_step, end_step, structure, history, multi_level)

        history[current] = total
        if multi_level:
            self.history_multi = history
        else:
            self.history_basic = history
        return total

    def __visualize_all_paths(self, current, end_step, structure, valid_paths = [], multi_level = True, visualize = True):
        """
        Prints each possible path created, but takes too long for large stair structures
        """
        for next_step, mag in structure.get(current[-1], []):
            new_path = current + [next_step]
            if next_step == end_step:
                joined_path = '-'.join(new_path)
                valid_paths.append(joined_path)
                if visualize:
                    print(f"{len(valid_paths)}: {joined_path}")
            else:
                if multi_level:
                    valid_paths = self.__visualize_all_paths(new_path, end_step, structure, valid_paths, multi_level, visualize)
                else:
                    current_branch = int(current.split('_')[0][1:])
                    next_branch = int(next_step.split('_')[0][1:])
                    if current_branch == next_branch:
                        valid_paths = self.__visualize_all_paths(new_path, end_step, structure, valid_paths, multi_level, visualize)

        return valid_paths

    def count_stair_paths(self, target_step, structure_type = "multiple"):

        start_point, end_point = self.identify_start_end(target_step)

        if structure_type == "single":
            multi_level = False
            stair_structure = self.basic_structure.copy()
        elif structure_type == "multiple":
            multi_level = True
            stair_structure = self.expanded_structure.copy()

        count = self.__dfs_algorithm(start_point, end_point, stair_structure, {}, multi_level)
        return count

    def __build_desired_path(self, start, end, desired_rank):

        @cache
        def extract_numbers(step):
            match = re.compile(r'S(\d+)_(\d+)').match(step[0])
            return int(match.group(1)), int(match.group(2))

        stair_structure = self.expanded_structure
        history = self.history_multi

        path = [start]
        while path[-1] != end:
            state = path[-1]
            reachable_states = set(stair_structure[state])
            reachable_states_sorted = sorted(reachable_states,  key=extract_numbers)
            path += [reachable_states_sorted]
            for state_next, _ in reachable_states_sorted:
                path[-1] = state_next
                if desired_rank - history[state_next] <= 0:
                    break
                desired_rank -= history[state_next]
        return '-'.join(path)

    def find_safest_path(self, target_step, total_paths):
        target_rank = 100000000000000000000000000000
        path_rank = min(target_rank, total_paths)
        start_point, end_point = self.identify_start_end(target_step)
        path_built = self.__build_desired_path(start_point, end_point, path_rank)

        return path_built

stairs = Staircase(steps, possible_moves)

single_stair = stairs.count_stair_paths("S1", "single")
print("Part 1:", single_stair)

multiple_stairs = stairs.count_stair_paths("S1", "multiple")
print("Part 2:", multiple_stairs)

ranked_path = stairs.find_safest_path("S1", multiple_stairs)
print("Part 3:", ranked_path)

# print(f"Execution Time = {time.time() - start_time:.5f}s")

