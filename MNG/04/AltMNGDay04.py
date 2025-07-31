"""Marches And Gnatts - Puzzle 4
Solution Started: Jul 31, 2025
Puzzle Link: https://mng.quest/quest/4/
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D04_file = "MNGDay04.js"
D04_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D04_file)

"""Marches And Gnatts - Puzzle 4
Solution Started: Jul 28, 2025
Puzzle Link: https://mng.quest/quest/4/unary-multiplication
Solution by: Abbas Moosajee
Brief: [Unary Multiplication]
"""


#!/usr/bin/env python3
import os, re, copy, time, sys
from pathlib import Path

# Add the TuringMachineSim folder to path
turing_path = Path(__file__).resolve().parent.parent / "TuringMachineSim"
sys.path.insert(0, str(turing_path))

from TuringModules import TuringMachine, TuringGUI

mult_tape = "||||||||*|||"

# Soln 1: steps = 1,442,415, rules = 19
mult_rules1 = """
    INIT  | toB   _ R   // Erase | from a, move to copy b
    INIT  * SKIP  _ R   // All of a consumed, erase '*' and move to HALT

    toB   | toB   | R
    toB   * eachB * R   // Move to start copying b

    nextA _ INIT  _ R   // After one copy of b, move back to INIT
    nextA | nextA | L
    nextA * nextA * L

    SKIP  | SKIP  _ R   // Erase b
    SKIP  _ HALT  _ R

    eachB _ nextA _ L   // No more b to copy
    eachB | sep   _ R   // Copy this '|', erase original

    sep   _ add   _ R
    sep   | sep   | R

    add   _ sepL  | L   // Add copy of b to end
    add   | add   | R

    sepL  _ nextB _ L
    sepL  | sepL  | L

    nextB _ eachB | R   // Go back to copy next '|'
    nextB | nextB | L
    """

# Soln |: steps =  , rules =
mult_rules = """
    INIT  | toB   _ R   // Erase | from a, move to copy b
    INIT  * SKIP  _ R   // All of a consumed, erase '*' and move to HALT

    toB   | toB   | R
    toB   * eachB * R   // Move to start copying b

    nextA _ INIT  _ R   // After one copy of b, move back to INIT
    nextA | nextA | L
    nextA * nextA * L

    SKIP  | SKIP  _ R   // Erase b
    SKIP  _ HALT  _ R

    eachB _ nextA _ L   // No more b to copy
    eachB | sep   _ R   // Copy this '|', erase original

    sep   _ add   _ R
    sep   | sep   | R

    add   _ sepL  | L   // Add copy of b to end
    add   | add   | R

    sepL  _ nextB _ L
    sepL  | sepL  | L

    nextB _ eachB | R   // Go back to copy next '|'
    nextB | nextB | L
    """


if __name__ == "__main__":
    _, results, used_resources = TuringGUI(mult_rules).run_simulator(mult_tape)

    # _, results, used_resources = TuringMachine(mult_rules).run_machine(mult_tape, visualize=True)

    print_info = results + [""] + used_resources
    print("\n".join(print_info))