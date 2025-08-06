"""Marches And Gnatts - Puzzle 0
Solution Started: Jul 25, 2025
Puzzle Link: https://mng.quest/quest/tutorial
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

    # _, results, used_resources = TuringGUI(init_rules).run_simulator(init_tape)
