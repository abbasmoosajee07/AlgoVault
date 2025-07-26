from TuringMachine import TuringMachine, MachineLogic, TuringConfig
from TuringGUI import TuringGUI

TuringMachine = TuringMachine
MachineLogic = MachineLogic
TuringConfig = TuringConfig
TuringGUI = TuringGUI

if __name__ == "__main__":
    init_rules = """
        INIT | FIND | R
        FIND | FIND | R
        FIND _ HALT | R
        """

    init_tape = "||||"

    # Turing Machine Basic Run
    _, basic_results, basic_resources = TuringMachine(init_rules).run_machine(init_tape, play_type = 0, visualize=True)
    basic_info = basic_results + [""] + basic_resources
    print("\n".join(basic_info))

    # Turing Machine GUI Interface
    _, gui_results, gui_resources = TuringGUI(init_rules).run_simulator(init_tape)
    gui_info = gui_results + [""] + gui_resources
    print("\n".join(gui_info))