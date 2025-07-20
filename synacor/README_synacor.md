# 🧠 Synacor Challenge: Virtual Machine & Automated Console Solver

A Python implementation of the [Synacor Challenge](https://github.com/Aneurysm9/vm_challenge/tree/main), featuring:

- A fully compliant virtual machine (VM) for executing Synacor bytecode.
- An intelligent automation layer for exploring and solving the in-game text adventure.

---

## Project Structure

### 1. `VirtualMachine` — Synacor VM Emulator

Faithfully implements the Synacor architecture:

- **15-bit address space** (32,768 words of memory)
- **8 general-purpose registers**
- **Stack operations**, function calls, and conditional jumps
- **Input/output buffering** with optional interactive mode
- **State replication** for search algorithms (e.g., BFS/DFS)
- **Debug logging** to trace every operation (optional output to `.txt`)
- **Modular architecture**, similar to my solution for *[Advent of Code 2019](https://github.com/abbasmoosajee07/AdventofCode/blob/main/2019/Intcode_Computer/Intcode_Computer.py)*’s Intcode VM

> Replication enables state cloning at any point—critical for exploring alternate execution paths and game states.

---

### 2. `SynacorConsole` — Automated Game Console

An automation layer that interfaces with the VM to interact with the Synacor text adventure.

#### Key Features:

- **Text Parsing**: Extracts room names, descriptions, exits, and items from game output.
- **Game Map Traversal**:Uses **Breadth-First Search (BFS)** to explore all reachable rooms.
- **Inventory Management**: Automatically collects, uses, and manages items based on game logic.
- **Code Extraction**: Uses regex to identify challenge codes and compute their MD5 hashes.
- **HTML Terminal Renderer**: Renders clean output for easier debugging and visualization.

---

## Core Algorithms

### Room Uniqueness & Mapping

Room identity is critical to traversal. Originally based on `md5(description)`, which fails for visually identical but logically distinct rooms.

**Current strategy:**
- Room ID is based on the **room purpose** (description beyond the name).
- Hardcoded exceptions help disambiguate edge cases.
- Backtracking is now allowed to ensure complete coverage.

---
## Puzzles
- Three specific puzzles within the adventure game, that had to be solved using different approaches.
- If conditions used to activate these solutions based on being in correct room and having correct items in inventory.
- Once a solution is reached for first time allow option to reset queue, improving speed by clearing other options.

### Coin Puzzle Solver

- Maps words like `two`, `triangle`, or `seven` to integers (2–9).
- Uses `itertools.permutations` to try every arrangement.
- Evaluates equations using a custom (non-`eval`) parser.
- Could be simplified further via hardcoded structure recognition.

---

### Mystery Puzzle (Debugger-Based)

- Solved using direct VM introspection:
  - Inspects stack, memory, and register states.
  - Injects breakpoints and traces for logical deduction.
  - Built the `VM_Debugger`, which prints disassembles and prints out a small portion of the program to debug at which pointer the R7 register must be called.
  - Modified Ackermann func, as shown below, allows the target_address to be calculated.

$$
A(m, n) =
\begin{cases}
(n + 1) \mod M & \text{if } m = 0 \\\\
(n + k + 1) \mod M & \text{if } m = 1 \\\\
((n + 2) \cdot k + n + 1) \mod M & \text{if } m = 2 \\\\
A(m - 1, k) & \text{if } n = 0 \text{ and } m > 2 \\\\
A(m - 1, A(m, n - 1)) & \text{otherwise}
\end{cases}
$$

---

### Maze Grid Puzzle

- Reading the journal provides a series of entries that tell you the next step is a math based grid.
- First, you need to map out the complete grid, before solving it to get the desired instructions.
- Mini BFS solution to find the perfect path through the maze that validates the target value.

## Benchmarking
- Total Paths Explored and Max queue ize at any given point.
- Time for BFS and Peak Memory Use.
- Individual breakdown of how long it took to obtain each code in the BFS.

---
## Dependencies
- Python 3.8+
- Standard library:
  - `re`, `hashlib`, `collections`, `os`, `copy`, `itertools`
- Optional:
  - `IPython.display` — for rich HTML-based terminal output

---

## Getting Started
To launch the automated console:

```python
console = SynacorConsole(software=program_bytes, spec_code="startCodeHere")
console.auto_play()
