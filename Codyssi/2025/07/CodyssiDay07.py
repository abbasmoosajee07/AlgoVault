"""Codyssi Puzzles - Problem 7
Solution Started: Apr 9, 2025
Puzzle Link: https://www.codyssi.com/view_problem_11?
Solution by: Abbas Moosajee
Brief: [Siren Disruption]
"""

#!/usr/bin/env python3

import os, re, copy

# Load the input data from the specified file path
D07_file = "Day07_input.txt"
D07_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D07_file)

# Read and sort input data into a grid
with open(D07_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    og_frequencies = {idx: num for idx, num in enumerate(list(map(int, input_data[0].split('\n'))), start=1)}
    swap_tracks = [tuple(map(int, track.split('-'))) for track in input_data[1].split('\n')]
    test_index = int(input_data[2])

frequencies_p1 = copy.deepcopy(og_frequencies)
for (track_x, track_y) in swap_tracks:
    swap_freq_p1 = frequencies_p1.copy()
    swap_freq_p1[track_x] = frequencies_p1[track_y]
    swap_freq_p1[track_y] = frequencies_p1[track_x]
    frequencies_p1 = swap_freq_p1.copy()
print("Part 1:", frequencies_p1[test_index])

frequencies_p2 = copy.deepcopy(og_frequencies)
for swap_idx, (track_x, track_y) in enumerate(swap_tracks):
    track_z = swap_tracks[((swap_idx + 1) % len(swap_tracks))][0]
    swap_freq_p2 = frequencies_p2.copy()
    swap_freq_p2[track_x] = frequencies_p2[track_z]
    swap_freq_p2[track_y] = frequencies_p2[track_x]
    swap_freq_p2[track_z] = frequencies_p2[track_y]
    frequencies_p2 = swap_freq_p2.copy()
print("Part 2:", frequencies_p2[test_index])

def swap_tracks_func(freq_dict: dict, swaps: tuple) -> dict:
    track_x, track_y = swaps
    swap_freq = freq_dict.copy()

    # Convert to list of track numbers (assuming 1-based and consecutive)
    track_nums = list(freq_dict.keys())
    n = len(track_nums)

    # Ensure X and Y are valid tracks
    if track_x not in freq_dict or track_y not in freq_dict:
        return swap_freq

    # Index positions (0-based) for X and Y in the sorted track list
    ix = track_nums.index(track_x)
    iy = track_nums.index(track_y)

    # Find the maximum block size
    max_block = 0
    while (ix + max_block < n and iy + max_block < n and
            track_nums[ix + max_block] == track_nums[ix] + max_block and
            track_nums[iy + max_block] == track_nums[iy] + max_block and
            abs((track_nums[ix + max_block]) - (track_nums[iy + max_block])) >= max_block + 1):
        max_block += 1

    # Perform the block-wise swap
    for i in range(max_block):
        tx = track_nums[ix + i]
        ty = track_nums[iy + i]
        swap_freq[tx], swap_freq[ty] = swap_freq[ty], swap_freq[tx]

    return swap_freq

frequencies_p3 = copy.deepcopy(og_frequencies)
for swap_idx, swap_inst in enumerate(swap_tracks):
    # print("\nBefore:", list(frequencies_p3.values()))
    # print(f"swap {swap_idx + 1}: {swap_inst}")
    frequencies_p3 = swap_tracks_func(frequencies_p3,swap_inst)
    # print("After:", list(frequencies_p3.values()))
print("Part 3:", frequencies_p3[test_index])
