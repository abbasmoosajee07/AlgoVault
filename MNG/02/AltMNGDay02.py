"""Marches And Gnatts - Puzzle 2
Solution Started: Jul 26, 2025
Puzzle Link: https://mng.quest/quest/2/unary-even-odd
Solution by: Abbas Moosajee
Brief: [Unary Even Odd]
"""


#!/usr/bin/env python3
import os, re, copy, time, sys
from pathlib import Path

# Add the TuringMachineSim folder to path
turing_path = Path(__file__).resolve().parent.parent / "TuringMachineSim"
sys.path.insert(0, str(turing_path))

from TuringModules import TuringMachine, TuringGUI

# Soln 1: steps = 20379, rules = 5
even_odd_rules_v1 = """
    INIT | ODD  _ R
    ODD  | EVEN _ R
    EVEN | ODD  _ R
    ODD  _ HALT O R
    EVEN _ HALT E R
    """

# Soln 1: steps = 20379, rules = 4
even_odd_rules = """
    INIT | ODD  _ R
    ODD  | INIT _ R
    ODD  _ HALT O R
    INIT _ HALT E R
    """

even_odd_tape = "|||||||"

if __name__ == "__main__":
    _, results, used_resources = TuringMachine(even_odd_rules).run_machine(even_odd_tape, visualize=True)
    print_info = results + [""] + used_resources
    print("\n".join(print_info))

