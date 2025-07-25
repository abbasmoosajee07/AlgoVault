import time, psutil
import tkinter as tk
from tkinter import messagebox

# --- Paste your TuringConfig, MachineLogic, and TuringMachine classes above this line ---
from TuringMachine import MachineLogic, TuringConfig, TuringMachine

class TuringGUI:
    def __init__(self, root, transition_rules_str: str, initial_tape: str):
        self.root = root
        self.root.title("Turing Machine Simulator")

        self.turing = TuringMachine(transition_rules_str)
        self.cpu = MachineLogic(self.turing.transition_rules)
        self.initial_tape = initial_tape
        self.step_count = 0

        # --- GUI elements (create first) ---
        self.tape_label = tk.Label(root, text="", font=("Courier", 16))
        self.tape_label.pack(pady=10)

        self.state_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.state_label.pack(pady=5)

        self.step_button = tk.Button(root, text="Step", command=self.step)
        self.step_button.pack(side="left", padx=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side="left", padx=10)

        self.halt_label = tk.Label(root, text="", fg="red", font=("Helvetica", 12, "bold"))
        self.halt_label.pack(pady=10)

        # --- Now it's safe to call reset --s-
        self.reset()

    def reset(self):
        self.cpu = MachineLogic(self.turing.transition_rules)
        self.cpu._set_tape(self.initial_tape)
        self.cpu.input_tape = self.initial_tape
        self.cpu.running = True
        self.step_count = 0
        self.halt_label.config(text="")
        self.update_display()

    def step(self):
        if self.cpu.current_state == self.cpu.halt_state:
            self.halt_label.config(text="Machine HALTED")
            return
        try:
            self.cpu._step_logic()
            self.step_count += 1
            if self.cpu.current_state == self.cpu.halt_state:
                self.halt_label.config(text="Machine HALTED")
        except TuringConfig.MissingTransitionError as e:
            messagebox.showerror("Transition Error", str(e))
            self.halt_label.config(text="Machine STUCK")

        self.update_display()

    def update_display(self):
        min_pos, max_pos = self.cpu._get_tape_boundaries(window=10)
        tape_display = ""
        for i in range(min_pos, max_pos + 1):
            symbol = self.cpu.tape.get(i, self.cpu.blank_symbol)
            tape_display += symbol

        # Mark head
        head_marker = " " * (self.cpu.head_position - min_pos) + "^"

        self.tape_label.config(text=tape_display)
        self.state_label.config(
            text=f"Step: {self.step_count} | State: {self.cpu.current_state}"
        )

        self.cpu._print_tape_state()

# Example usage
if __name__ == "__main__":
    sample_instructions = """
    INIT | FIND | R
    FIND | FIND | R
    FIND _ HALT | R
    """
    input_tape = "||||"

    root = tk.Tk()
    app = TuringGUI(root, sample_instructions, input_tape)
    root.mainloop()
