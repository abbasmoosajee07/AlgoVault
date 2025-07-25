"""Marches And Gnatts - Puzzle 0
Solution Started: Jul 25, 2025
Puzzle Link: https://mng.quest/quest/tutorial
Solution by: Abbas Moosajee
Brief: [Binary Increment]
"""

#!/usr/bin/env python3

import os, re, copy, time, sys

turing_path = os.path.join(os.path.dirname(__file__), "..", "TuringMachine")
sys.path.append(turing_path)
from TuringMachine import MachineLogic, TuringConfig, TuringMachine

init_rules = """
    INIT | FIND | R
    FIND | FIND | R
    FIND _ HALT | R
    """
init_tape = "||||"

if __name__ == "__main__":
    _, results, used_resources = TuringMachine(init_rules).run_machine(init_tape, play_type = 0, visualize=True)
    print_info = results + [""] + used_resources
    print("\n".join(print_info))