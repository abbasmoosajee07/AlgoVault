"""i18n Puzzles - Puzzle 17
Solution Started: Jun 2, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/17
Solution by: Abbas Moosajee
Brief: [X marks the spot]
"""

#!/usr/bin/env python3

import os, re, copy, time, binascii, more_itertools, math
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()
# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    blocks = [item.splitlines() for item in input_data]

heights = [len(block) for block in blocks]
gcd_height = math.gcd(*heights)

def get_byte_type(byte):
    # Byte to be 2-char long hex
    # valid utf-8 encodings are A, BE, CEE, DEEE.
    first_digit = int(byte[0],16)
    mapping = 'AAAAAAAAEEEEBBCD'
    return mapping[first_digit]

def get_block_type(block):
    # get byte types for all bytes in block
    return [''.join(get_byte_type(byte) for byte in more_itertools.chunked(line,2)) for line in block]

def get_start_type(block_type):
    # number of Es that each line starts with
    output = []
    for line in block_type:
        count = 0
        while line.startswith('E'):
            count += 1
            line = line[1:]
        output.append(count)
    return output

def get_end_type(block_type):
    # number of Es you need to have in the next block for it to match
    output = []
    for line in block_type:
        e_count = 0
        while line[-1-e_count] == 'E':
            e_count += 1
        last_char = line[-1-e_count]
        total_e_count = 'ABCD'.index(last_char)
        remaining_count = total_e_count-e_count
        output.append(remaining_count)
    return output
        
class Block:
    def __init__(self,block,block_id=0):
        self.block_id = block_id
        self.block = block
        self.block_type = get_block_type(block)
        self.start_type = get_start_type(self.block_type)
        self.end_type = get_end_type(self.block_type)
        self.start_match_ids = [False for _ in self.start_type]
        self.end_match_ids = [False for _ in self.end_type]
        self.height = len(block)
        if max(self.start_type) == 0:
            self.start_match = [True for _ in self.start_type]
        else:
            self.start_match = [False for _ in self.start_type]
        if max(self.end_type) == 0:
            self.end_match = [True for _ in self.end_type]
        else:
            self.end_match = [False for _ in self.end_type]
    def __repr__(self):
        return '\n'.join(line for line in self.block)
            
blocks = [Block(block,index) for index,block in enumerate(blocks)]

def get_match(block):
    if all(block.end_match):
        return []
    else:
        output = []
        start_index = block.end_match.index(False)
        for other in blocks:
            if other.block_id == block.block_id:
                continue
            if start_index == 0: # consider all mappings where it goes above
                for other_start in range(0,other.height,gcd_height):
                    overlap_blocks = list(zip(block.end_type,other.start_type[other_start:]))
                    if all(a==b for a,b in overlap_blocks):
                        output.append([other.block_id,-other_start,len(overlap_blocks)])
            else: # consider mappings where it goes below
                overlap_blocks = list(zip(block.end_type[start_index:],other.start_type))
                if all(a==b for a,b in overlap_blocks):
                    output.append([other.block_id,start_index,len(overlap_blocks)])
        return output

while True:
    remaining_blocks = sum(not item for block in blocks for item in block.start_match+block.end_match)
    if not remaining_blocks:
        break
    else:
        for block_id,block in enumerate(blocks):
            matches = get_match(block)
            if len(matches)==1:
                match = more_itertools.one(matches)
                other_id,start_index,overlap = match
                other = blocks[other_id]
                if start_index >= 0:
                    block_start = start_index
                    block_end = start_index+overlap
                    other_start = 0
                    other_end = overlap
                else:
                    block_start = 0
                    block_end = overlap
                    other_start = -start_index
                    other_end = -start_index+overlap
                block.end_match[block_start:block_end] = [True for _ in range(overlap)]
                block.end_match_ids[block_start:block_end] = [[other_id,i] for i in range(other_start,other_end)]
                other.start_match[other_start:other_end] = [True for _ in range(overlap)]
                other.start_match_ids[other_start:other_end] = [[block_id,i] for i in range(block_start,block_end)]

top_left_block = more_itertools.one(block for block in blocks if block.block[0].startswith('e29594'))
top_left_id = top_left_block.block_id
top_left_block.x=0
top_left_block.y=0
queue = {top_left_id}
cleared = set()
while queue:
    block_id = queue.pop()
    cleared.add(block_id)
    block = blocks[block_id]
    start_others = [line for line in block.start_match_ids if line]
    end_others = [line for line in block.end_match_ids if line]
    x = block.x
    y = block.y
    for block_index,(other_id,other_index) in enumerate(start_others):
        if other_id not in queue and other_id not in cleared:
            queue.add(other_id)
            other = blocks[other_id]
            other.x = x+block_index-other_index
            other.y = y-1
    for block_index,(other_id,other_index) in enumerate(end_others):
        if other_id not in queue and other_id not in cleared:
            queue.add(other_id)
            other = blocks[other_id]
            other.x = x+block_index-other_index
            other.y = y+1

full_height = max(block.x+block.height for block in blocks)
full_width = max(block.y+1 for block in blocks)

full_grid = np.full([full_height,full_width],'g',dtype=object)
for block in blocks:
    x_start = block.x
    x_end = block.x+block.height
    y = block.y
    full_grid[x_start:x_end,y] = block.block

full_grid = [''.join(line) for line in full_grid]
assert all('g' not in line for line in full_grid)

def convert(word):
    output = [int(''.join(item),16) for item in more_itertools.chunked(word,2)]
    return bytes(output).decode('utf-8')

full_grid = [convert(line) for line in full_grid]
# print('\n'.join(full_grid))
x,y = more_itertools.one((x,y) for x,line in enumerate(full_grid) for y,char in enumerate(line) if char=='╳')
answer = x*y
print(answer)

print(f"Execution Time = {time.time() - start_time:.5f}s")

# ╔-═-═-═-═-═-═-═--═-═-═-╗
# |~≋≋ññ≋~~ñ𑀍≋ñ~~ñ≋~ññ𑀍~ñ|
# ║ññ≋~~≋𑀍~≋~ññ~ñ~ñññ≋ñ~~║
# |~ññ𑀍ñ≋𑀍-¯~ñññññññ−-¯¯ñ|
# ║~≋ñ~¯-𐲣-¯¯¯ñ~≋𑀍≋ñ----ñ║
# |ñ≋ññ−-𐲣-¯¯-ñññ𑀍ñ¯¯−¯-~|
# ║ñ≋~~¯−𐲣--¯¯-~ñ𑀍≋~¯--ññ║
# |~≋ññ𐲣-−¯¤¯−-≋~≋~ñ≋¯≋~~|
# ║~~ññ~𐲣𐲣¯¯𐲣---ññ~ñ~~≋ññ║
# |~ñ≋𑀍~≋≋--¯¯¯≋ñ~~𑀍~≋ñ~≋|
# ║ñ≋ñññ~𑀍ñ~¯ññ~~𑀍~~~ñ~≋ñ║
# |ññ≋~≋ñ≋~≋-ñ╳~≋≋-−-¯−~ñ|
# ║ñ~ññññ≋~ññ≋𑀍~~𑀍--¯-¯-ñ║
# |≋ñ~≋ñ≋~ññ~𑀍ñ~≋𑀍¯¯¯−--~|
# ║~~𑀍~~ñ≋≋-ñ≋~ñ~𐲣•.¤-−-~║
# |ñ≋ññññ𑀍-¯~-¯≋−𐳓:¤..¯¯≋|
# ║~ñ𑀍≋~~¯¯−-𐲣--¤𐳓¨¨¤.--~║
# |~ññ≋≋-𐲣--𐲣-¯𐲣.𐳓¤..−¯-ñ|
# ║≋~ñ𑀍--𐲣−-−--¯-𐳓.¤¤.¯-~║
# |≋ñ≋¯¯¯¯-𐲣-¯¯-¯−¯¯-−¯-≋|
# ║ñ≋-¯¯-−-ñ¯~≋~≋≋--¯¯¯¯ñ║
# |≋ñ¯¯¯≋≋≋~~~𑀍ñ~ñ≋~≋~ñ-≋|
# ║ñ~~~𑀍~≋ñ~~≋ññ≋≋ñññ~≋~~║
# ╚-═-═-═-═-═-═-═--═-═-═-╝

