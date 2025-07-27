"""Marches And Gnatts - Puzzle 3
Solution Started: Jul 27, 2025
Puzzle Link: https://mng.quest/quest/3/binary-increment
Solution by: Abbas Moosajee
Brief: [Binary Increment]
"""

#!/usr/bin/env python3
import os, re, copy, time, sys
from pathlib import Path

# Add the TuringMachineSim folder to path
turing_path = Path(__file__).resolve().parent.parent / "TuringMachineSim"
sys.path.insert(0, str(turing_path))

from TuringModules import TuringMachine, TuringGUI

# for num in range(0, 12):
#     bin_num = bin(num)[2:]  # Removes the '0b' prefix
#     print(f"{num} -> {bin_num} ")
#     # {int(bin_num, 2)}

# Soln 1: steps = 652, rules = 6
bin_inc_rules = """
    INIT 0 INIT 0 R
    INIT 1 INIT 1 R
    INIT _ FIND _ L
    FIND 1 FIND 0 L
    FIND 0 HALT 1 R
    FIND _ HALT 1 R
    """

bin_inc_tape = "1010"

if __name__ == "__main__":
    # _, results, used_resources = TuringGUI(bin_inc_rules).run_simulator(bin_inc_tape)

    _, results, used_resources = TuringMachine(bin_inc_rules).run_machine(bin_inc_tape, visualize=True)

    print_info = results + [""] + used_resources
    print("\n".join(print_info))
