"""Turing Modules Test
"""

#!/usr/bin/env python3

import sys
from pathlib import Path

# Add the TuringMachineSim folder to path
turing_path = Path(__file__).resolve().parent / "TuringMachineSim"
sys.path.insert(0, str(turing_path))

from TuringMachineSim.TuringModules import TuringGUI, TuringMachine

TuringMachine = TuringMachine
TuringGUI = TuringGUI

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

    _, results, used_resources = TuringGUI(init_rules).run_simulator(init_tape)
