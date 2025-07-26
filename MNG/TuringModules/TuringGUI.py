import tkinter as tk
from tkinter import ttk, messagebox
import ctypes, platform, time, psutil
from TuringMachine import MachineLogic, TuringConfig, TuringMachine

class TuringGUI:
    def __init__(self, transition_rules_str: str):
        self.set_dpi_awareness()
        self.root = tk.Tk()
        self.root.title("Turing Machine Simulator")

        # Disables resizing both horizontally and vertically
        self.root.resizable(False, False)

        self.turing = TuringMachine(transition_rules_str)
        self.cpu = MachineLogic(self.turing.transition_rules)

        self.MAX_STEPS = 1_000_000
        self.BASE_STEP = 1
        self.DELAY = 300

        self.init_time = TuringConfig.get_timestamp()
        self.init_memory = TuringConfig.get_current_memory_mb()

    def _build_gui(self):
        self.main = ttk.Frame(self.root, padding=10)
        self.main.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Title
        ttk.Label(self.main, text="Turing Machine Simulator", font=("Helvetica", 20, "bold")).grid(column=0, columnspan=2, pady=10)

        # --- Tape Display ---
        tape_card = ttk.LabelFrame(self.main, text="Tape", padding=10)
        tape_card.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.tape_cells = []
        self.tape_frame = ttk.Frame(tape_card)
        self.tape_frame.pack()
        for _ in range(21):
            lbl = tk.Label(self.tape_frame, text="_", width=2, height=1, font=("Courier", 16), relief="solid", borderwidth=1, bg="white")
            lbl.pack(side="left", padx=2)
            self.tape_cells.append(lbl)

        # --- Status Display ---
        status_card = ttk.LabelFrame(self.main, text="Status", padding=10)
        status_card.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.status_label = ttk.Label(status_card, text="State: INIT | Step: 0", font=("Helvetica", 12))
        self.status_label.pack()
        self.halt_label = tk.Label(status_card, text="", fg="red", font=("Helvetica", 12, "bold"))
        self.halt_label.pack()

        # --- Configuration Frame (left) ---
        config_frame = ttk.LabelFrame(self.main, text="Configuration", padding=10)
        config_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Label(config_frame, text="Transition Rules:").grid(row=0, column=0, sticky="w")
        self.rules_text = tk.Text(config_frame, height=6, width=40)
        self.rules_text.insert("1.0", "INIT | FIND | R\nFIND | FIND | R\nFIND _ HALT | R")
        self.rules_text.grid(row=1, column=0, pady=5)

        ttk.Label(config_frame, text="Initial Tape:").grid(row=2, column=0, sticky="w")
        self.tape_input = ttk.Entry(config_frame, width=30)
        self.tape_input.insert(0, self.initial_tape)
        self.tape_input.grid(row=3, column=0, pady=5)

        ttk.Button(config_frame, text="Reset", command=self.__reset).grid(row=4, column=0, pady=5)

        # --- Controls Frame (right) ---
        ctrl_frame = ttk.LabelFrame(self.main, text="Controls", padding=10)
        ctrl_frame.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

        ttk.Label(ctrl_frame, text="Steps:").grid(row=0, column=0, sticky="w")
        self.step_entry = ttk.Entry(ctrl_frame, width=10)
        self.step_entry.insert(0, str(self.BASE_STEP))
        self.step_entry.grid(row=0, column=1, padx=5)

        ttk.Label(ctrl_frame, text="Max Steps:").grid(row=1, column=0, sticky="w")
        self.max_steps = ttk.Entry(ctrl_frame, width=10)
        self.max_steps.insert(0, str(self.MAX_STEPS))
        self.max_steps.grid(row=1, column=1, padx=5)

        ttk.Label(ctrl_frame, text="Speed (ms):").grid(row=2, column=0, sticky="w")
        self.delay_entry = ttk.Entry(ctrl_frame, width=10)
        self.delay_entry.insert(0, str(self.DELAY))
        self.delay_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = ttk.Frame(ctrl_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(btn_frame, text="Step", command=self._step).grid(row=0, column=0, padx=4)
        self.run_button = ttk.Button(btn_frame, text="Run", command=self.__run)
        self.run_button.grid(row=0, column=1, padx=4)
        self.pause_button = ttk.Button(btn_frame, text="Pause", command=self.__pause, state="disabled")
        self.pause_button.grid(row=0, column=2, padx=4)

    @staticmethod
    def set_dpi_awareness():
        """Enable DPI awareness for clearer UI rendering on Windows."""
        if platform.system() == "Windows":
            try:
                # For Windows 8.1 or later
                ctypes.windll.shcore.SetProcessDpiAwareness(1)  # PROCESS_SYSTEM_DPI_AWARE
            except AttributeError:
                try:
                    # Fallback for older Windows (Vista+)
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass  # Unsupported, ignore
            except Exception:
                pass  # Other error, ignore

    def __reset(self):
        rules = self.rules_text.get("1.0", "end-1c")
        self.turing = TuringMachine(rules)
        self.cpu = MachineLogic(self.turing.transition_rules)
        self.initial_tape = self.tape_input.get()
        self.cpu._set_tape(self.initial_tape)
        self.cpu.input_tape = self.initial_tape
        self.cpu.running = True
        self.step_count = 0
        self.running = False
        self.halt_label.config(text="")
        self.run_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.update_display()

    def __run(self):
        self.running = True
        self.run_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self._auto_step()

    def __pause(self):
        self.running = False
        self.run_button.config(state="normal")
        self.pause_button.config(state="disabled")

    def _step(self):
        try:
            steps_to_run = int(self.step_entry.get())
        except ValueError:
            steps_to_run = self.BASE_STEP

        try:
            max_allowed = int(self.max_steps.get())
        except ValueError:
            max_allowed = self.MAX_STEPS

        for _ in range(steps_to_run):
            if self.step_count >= max_allowed:
                self.halt_label.config(text=f"Max steps ({max_allowed}) reached")
                self.running = False
                self.run_button.config(state="normal")
                self.pause_button.config(state="disabled")
                break

            if self.cpu.current_state == self.cpu.halt_state:
                self.halt_label.config(text="Machine HALTED")
                self.running = False
                self.run_button.config(state="normal")
                self.pause_button.config(state="disabled")
                break

            try:
                self.cpu._step_logic()
                self.step_count += 1
            except TuringConfig.MissingTransitionError as e:
                messagebox.showerror("Transition Error", str(e))
                self.halt_label.config(text="Machine STUCK")
                self.running = False
                break

        self.update_display()

    def _auto_step(self):
        if not self.running:
            return
        if self.cpu.current_state == self.cpu.halt_state:
            self.halt_label.config(text="Machine HALTED")
            self.__pause()
            return
        self._step()
        try:
            delay = int(self.delay_entry.get())
        except ValueError:
            delay = self.DELAY
        self.root.after(delay, self._auto_step)

    def update_display(self):
        min_pos = self.cpu.head_position - 10
        for i, label in enumerate(self.tape_cells):
            pos = min_pos + i
            symbol = self.cpu.tape.get(pos, self.cpu.blank_symbol)
            label.config(text=symbol, )

            if pos == self.cpu.head_position:
                label.config( highlightbackground="blue", highlightcolor="blue",
                    highlightthickness=2, font=("Courier", 16, "bold"),
                )
            else:
                label.config(bg="white", fg="black", relief="solid", bd=0.25)
        self.status_label.config(text=f"State: {self.cpu.current_state} | Step: {self.step_count}")

    def run_simulator(self, init_tape: str):
        transition_rules = self.turing.transition_rules.copy()
        self.initial_tape = init_tape
        self.step_count = 0
        self.running = False
        self._build_gui()
        self.__reset()

        self.root.mainloop()

        resources_used = [
            f"   Time run: {TuringConfig.get_timestamp() - self.init_time:.5f}s",
            f"Memory used: {TuringConfig.get_current_memory_mb()}MB"
        ]

        final_tape = self.cpu._print_tape_state(False)
        results = [
            f"Result Tape: '{final_tape}'",
            f"Steps Count: {self.step_count}",
            f"Total Rules: {len(transition_rules)}",
        ]

        return transition_rules, results, resources_used
