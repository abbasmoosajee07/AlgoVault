"""Marches And Gnatts - Puzzle 1
Solution Started: Jul 26, 2025
Puzzle Link: https://mng.quest/quest/1/unary-addition
Solution by: Abbas Moosajee
Brief: [Unary Addition]
"""

#!/usr/bin/env python3
import os, re, copy, time, sys
from pathlib import Path

# Add the TuringMachineSim folder to path
turing_path = Path(__file__).resolve().parent.parent / "TuringMachineSim"
sys.path.insert(0, str(turing_path))

from TuringModules import TuringMachine, TuringGUI

# Allows for Multiple additions in same tape, more holistic.
# Orignal Solution: 57,954 Steps MNG
add_rules_v1 = """
    INIT | FIND _ R
    FIND | FIND | R
    FIND + FIND | R
    FIND _ HALT _ R
    """

# Only single addition, stops at first +, fastest solution.
# Final Solution: 28,143 Steps MNG
add_rules = """
    INIT | FIND _ R
    FIND | FIND | R
    FIND + HALT | R
    """

add_tape = "|||+||||"

if __name__ == "__main__":
    _, results, used_resources = TuringMachine(add_rules).run_machine(add_tape, play_type = 0, visualize=True)
    print_info = results + [""] + used_resources
    print("\n".join(print_info))
