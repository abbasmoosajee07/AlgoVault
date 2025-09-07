"""Eldarverse Puzzles - Problem N
Solution Started: September 7,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-N
Solution by: Abbas Moosajee
Brief: [Maze Solitaire]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import deque

# Load input file
input_file = "problem-sep-25-long-N-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

print("Input Data:", data)


solutions = []

MOD = 1_000_000_009

# card values for one suit: A=1, 2..10, J/Q/K = 11 (three cards)
SUIT_VALUES = [1,2,3,4,5,6,7,8,9,10,11,11,11]  # 13 cards

# precompute factorials up to 13
FACT = [1] * 14
for i in range(1, 14):
    FACT[i] = (FACT[i-1] * i) % MOD

def bfs_path(grid, n, m, start, end):
    """Return list of coordinates of unique path from start to end (inclusive)."""
    q = deque([start])
    parent = {start: None}
    dirs = [(-1,0), (1,0), (0,-1), (0,1)]
    while q:
        x,y = q.popleft()
        if (x,y) == end:
            break
        for dx,dy in dirs:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] != 'X' and (nx,ny) not in parent:
                parent[(nx,ny)] = (x,y)
                q.append((nx,ny))
    if end not in parent:
        return []  # no path (shouldn't happen given problem)
    # reconstruct
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

def direction(from_cell, to_cell):
    """Return a direction label 'N','S','W','E' for movement from from_cell to to_cell."""
    fx,fy = from_cell
    tx,ty = to_cell
    if tx == fx-1 and ty == fy:
        return 'N'
    if tx == fx+1 and ty == fy:
        return 'S'
    if tx == fx and ty == fy-1:
        return 'W'
    if tx == fx and ty == fy+1:
        return 'E'
    raise ValueError("Non-adjacent cells")

def suit_for_direction(d):
    """Map direction to suit index 0..3 (we'll use indices for suits)"""
    # Diamonds (D) → North (up)
    # Hearts (H) → South (down)
    # Clubs (C) → West (left)
    # Spades (S) → East (right)
    if d == 'N': return 0  # Diamonds
    if d == 'S': return 1  # Hearts
    if d == 'W': return 2  # Clubs
    if d == 'E': return 3  # Spades
    raise ValueError("Unknown direction")

def count_ways_for_suit(run_lengths):
    """
    Given a list of run lengths (in order) that correspond to this suit,
    count number of ways to assign disjoint ordered sequences of the 13 distinct suit-cards
    so that each run's sum equals its corresponding length.
    """
    if len(run_lengths) == 0:
        return 1

    # Precompute for all subset masks: sum value and size
    N = 13
    TOTAL_MASK = 1 << N
    subset_sum = [0] * TOTAL_MASK
    subset_size = [0] * TOTAL_MASK
    for mask in range(1, TOTAL_MASK):
        # build by lowbit
        lb = mask & -mask
        i = (lb.bit_length() - 1)
        prev = mask ^ lb
        subset_sum[mask] = subset_sum[prev] + SUIT_VALUES[i]
        subset_size[mask] = subset_size[prev] + 1

    # For each run length, list all subset masks whose sum equals that length
    valid_subsets_per_run = []
    for d in run_lengths:
        cur_list = []
        # any subset with sum d (size may be 0 if d==0, but run lengths are positive)
        for mask in range(1, TOTAL_MASK):
            if subset_sum[mask] == d:
                cur_list.append((mask, subset_size[mask]))
        # if none, impossible
        if not cur_list:
            return 0
        valid_subsets_per_run.append(cur_list)

    # DP over masks
    dp = [0] * TOTAL_MASK
    dp[0] = 1
    for cur_list in valid_subsets_per_run:
        newdp = [0] * TOTAL_MASK
        # for each used mask so far, try each subset for this run that's disjoint
        for used_mask in range(TOTAL_MASK):
            if dp[used_mask] == 0:
                continue
            base = dp[used_mask]
            for (submask, sz) in cur_list:
                if (used_mask & submask) == 0:
                    nm = used_mask | submask
                    # multiply by number of orderings of chosen cards = sz!
                    newdp[nm] = (newdp[nm] + base * FACT[sz]) % MOD
        dp = newdp
    # total ways for this suit is sum over dp[mask] (final used masks)
    return sum(dp) % MOD

def solve_case(grid, n, m):
    # find S and E
    start = end = None
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'S':
                start = (i,j)
            if grid[i][j] == 'E':
                end = (i,j)
    path = bfs_path(grid, n, m, start, end)  # list of coords
    if not path:
        return 0

    # compute moves and runs
    moves = []
    for i in range(len(path)-1):
        d = direction(path[i], path[i+1])
        moves.append(d)

    # group into runs with lengths
    runs_by_suit = [[] for _ in range(4)]
    if moves:
        cur_dir = moves[0]
        cur_len = 1
        for k in range(1, len(moves)):
            if moves[k] == cur_dir:
                cur_len += 1
            else:
                suit = suit_for_direction(cur_dir)
                runs_by_suit[suit].append(cur_len)
                cur_dir = moves[k]
                cur_len = 1
        # last run
        suit = suit_for_direction(cur_dir)
        runs_by_suit[suit].append(cur_len)

    # For each suit compute ways, multiply
    ans = 1
    for s in range(4):
        ways = count_ways_for_suit(runs_by_suit[s])
        ans = (ans * ways) % MOD
        if ans == 0:
            break
    return ans

t = int(data[0].strip())
idx = 1
for case in range(1, t+1):
    while data[idx].strip() == "":
        idx += 1
    n,m = map(int, data[idx].split())
    idx += 1
    grid = []
    for _ in range(n):
        line = data[idx].rstrip('\n')
        grid.append(list(line))
        idx += 1
    ans = solve_case(grid, n, m)
    solutions.append(f"Case #{case}: {ans}")
print("\n".join(solutions))

output_file = "problem-sep-25-long-N-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions))

