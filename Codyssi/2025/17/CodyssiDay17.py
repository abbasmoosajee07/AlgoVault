"""Codyssi Puzzles - Problem 17
Solution Started: May 10, 2025
Puzzle Link: https://www.codyssi.com/view_problem_21?
Solution by: Abbas Moosajee
Brief: [Spiralling Stairs]
"""

#!/usr/bin/env python3

import os, re, copy, time, functools
start_time = time.time()

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

        self.basic_structure = copy.deepcopy(basic_structure)
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

        complete_moves =  copy.deepcopy(structure)
        valid_moves = self.valid_moves

        for base_step in structure:
            for next_step in list(complete_moves[base_step]):
                step_tracker(base_step, next_step)

        return complete_moves

    def __dfs_algorithm(self, current, end_step, structure, history = {}, multi_level = True):
        if current == end_step: # If current is final step, count 1
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
            self.history_multi = history.copy()
        else:
            self.history_basic = history.copy()
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
    def extract_numbers(self, s):
        # Use regex to extract the numbers after 'S' and after '_'
        match = re.match(r'S(\d+)_(\d+)', s)
        return (int(match.group(1)), int(match.group(2)))

    def __build_desired_path(self, start, end, target):
        # print(f"{start} -> {end}: Rank {desired_rank}")
        stair_structure = self.expanded_structure.copy()
        # reachable_states = {}
        # for step, connections in stair_structure.items():
        #     corrected_states = set(step for step, _ in connections)
        #     reachable_states[step] = corrected_states
        dp = self.history_multi.copy()
        dp[end] = 1

        path = [start]
        while path[-1] != end:
            state = path[-1]
            reachable_states = sorted(step for step, _ in stair_structure[state])
            reachable_states_sorted = sorted(reachable_states,  key=self.extract_numbers)
            print(state, reachable_states_sorted)
            path += [reachable_states_sorted]
            for state_next in reachable_states_sorted:
                path[-1] = state_next
                if target - dp[state_next] <= 0:
                    break
                target -= dp[state_next]
        return path

    def find_safest_path(self, target_step, total_paths, target_rank = 1E+29):
        path_rank = min(target_rank, total_paths)
        start_point, end_point = self.identify_start_end(target_step)
        path_built = self.__build_desired_path(start_point, end_point, path_rank)

        return '-'.join(path_built)

stairs = Staircase(steps, possible_moves)

single_stair = stairs.count_stair_paths("S1", "single")
print("Part 1:", single_stair)

multiple_stairs = stairs.count_stair_paths("S1", "multiple")
print("Part 2:", multiple_stairs)

ranked_path = stairs.find_safest_path("S1", multiple_stairs)
print("Part 3:", ranked_path)

from collections import defaultdict

blocks = [block.splitlines() for block in open(D17_file_path, "r").read().split("\n\n")]

# read staircases, build set of states and map of directed, single steps
states = set()
steps = defaultdict(list)
start, end = (-1, -1), (-1, -1)
for line in blocks[0]:
    s = line.split()
    id, level_start, level_end, sid_from, sid_to = int(s[0][1:]), int(s[2]), int(s[4]), s[7], s[9]
    for level in range(level_start, level_end + 1):
        states.add((id, level))
        if level < level_end:
            steps[(id, level)] += [(id, level + 1)]
    if id == 1:
        start, end = (id, level_start), (id, level_end)
    else:
        id_from, id_to = int(sid_from[1:]), int(sid_to[1:])
        steps[(id_from, level_start)] += [(id, level_start)]
        steps[(id, level_end)] += [(id_to, level_end)]

# read moves
moves = set(map(int, re.findall(r"[-+]?\d+", blocks[1][0])))
max_move = max(moves)

# build map of all states that are reachable from a state in a full move
reachable_states = defaultdict(set)
for state in states:
    states_tmp = {state}
    for k in range(1, max_move + 1):
        states_tmp_new = set()
        for s in states_tmp:
            states_tmp_new.update(steps[s])
        states_tmp = states_tmp_new
        if k in moves:
            reachable_states[state].update(states_tmp)

# topological sort of states
n_states = len(states)
in_degree = defaultdict(int)
for lst in steps.values():
    for v in lst:
        in_degree[v] += 1
sorted_states = []
stack = [s for s in states if in_degree[s] == 0]
while stack:
    v = stack.pop()
    sorted_states += [v]
    for u in steps[v]:
        in_degree[u] -= 1
        if in_degree[u] == 0:
            stack += [u]
assert len(sorted_states) == n_states

dp = defaultdict(int)
dp[start] = 1
for i in range(0, end[1] + 1):
    state = (1, i)
    for reachable_state in reachable_states[state]:
        if reachable_state[0] == 1:
            dp[reachable_state] += dp[state]
ans1 = dp[end]

dp = defaultdict(int)
dp[end] = 1
for state in reversed(sorted_states):
    for reachable_state in reachable_states[state]:
        dp[state] += dp[reachable_state]
ans2 = dp[start]


target = 100000000000000000000000000000
path = [start]
while path[-1] != end:
    state = path[-1]
    reachable_states_sorted = sorted(reachable_states[state])
    print(state, reachable_states_sorted)
    path += [reachable_states_sorted[0]]
    for state_next in reachable_states_sorted:
        path[-1] = state_next
        if target - dp[state_next] <= 0:
            break
        target -= dp[state_next]
ans3 = "-".join(f"S{state[0]}_{state[1]}" for state in path)
print(f"part 3: {ans3}")
print(f"Execution Time = {time.time() - start_time:.5f}s")

