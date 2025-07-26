# Turing Machine Simulator

This project implements a configurable and extensible **Turing Machine Simulator** in Python. It supports custom state transitions, dynamic memory tape, error handling, and optional visualization of the computation process.

## Modules Overview

### 1. `TuringConfig` — Configuration and Constants
This class holds:
- **Constants**: like directions (`L`, `R`), blank symbol (`_`), limits (max states, max tape size).
- **TransitionType**: a tuple of `(current_state, current_symbol, new_state, new_symbol, move_direction)`.
- **Custom Exceptions**:
  - `InvalidSymbolError`: raised if symbols are not 1-character.
  - `InvalidStateError`: state name too long.
  - `InvalidTransitionError`: bad format or duplicates.
  - `MissingTransitionError`: no rule for a symbol-state pair.

---

### 2. `MachineLogic` — Core Logic Engine
This is the "CPU" of the Turing Machine. It handles:
- Parsing validated transition rules into a nested dictionary.
- Executing step-by-step logic using those rules.
- Dynamically growing tape using a `dict[int, str]`.
- Optionally printing the tape and state on each step.

#### Key Methods:
- `_build_transition_dict`: Validates and indexes rules.
- `_set_tape`: Converts input string into sparse tape.
- `_print_tape_state`: Visualizes current tape & head position.
- `run_logic`: Main loop that executes transitions until `HALT`.

---

### 3. `TuringMachine` — User Interface Layer
A wrapper for setting up and running the Turing machine from human-readable instructions.

#### Key Features:
- **`parse_transition_rules()`**: Parses multiline strings into validated transition tuples.
- **`run_machine(init_tape, visualize=True)`**:
  - Initializes logic engine.
  - Runs computation with optional tape visualization.
  - Returns:
    - Transition rules used.
    - Final tape result, step count, and rule count.
    - Resource usage stats (time and memory).

---

### 4. `Turing_GUI` — Graphical User Interface Layer

A Tkinter-based GUI for stepping through and visualizing Turing machine execution.

#### Features:

* **Tape Visualization**: 21-cell window with current head position highlighted using a red border.

* **Interactive Controls**
  * `Step`: Run one or more steps manually.
  * `Run` / `Pause`: Auto-run with adjustable speed.
  * `Reset`: Reinitialize with original tape.

* **Live Feedback**: Displays current state, step count, and HALTED/STUCK status if applicable.

* **Configurable Speed**
  * Adjustable delay (ms) and steps per action via entry boxes.

#### Example Usage of both interfaces:

```python
init_rules = """
    INIT | FIND | R
    FIND | FIND | R
    FIND _ HALT | R
    """

init_tape = "||||"

# Turing Machine Basic Run
_, basic_results, basic_resources = TuringMachine(init_rules).run_machine(init_tape, play_type = 0, visualize=True)

# Turing Machine GUI Interface
_, gui_results, gui_resources = TuringGUI(init_rules).run_simulator(init_tape)
```