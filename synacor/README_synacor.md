# Synacor Challenge: Virtual Machine & Automated Console Solver

This project is a Python implementation of the [Synacor Challenge (Archive)](https://github.com/Aneurysm9/vm_challenge/tree/main), consisting of:

- A full-featured virtual machine (VM) capable of executing Synacor bytecode.
- An intelligent console system that can interpret game output, extract codes, manage inventory, and explore the text-based adventure world via automation.

---

## 🧠 Project Structure

### 1. `VirtualMachine` — Synacor VM Emulator

Implements the full Synacor spec with:

- **15-bit memory** (32K words)
- **8 general-purpose registers**
- **Stack operations**, function calls, and conditional jumps
- **Instruction logging and state replication** for controlled execution
- **Interactive input/output** buffering
- **Debug logging** an optional log that can be turned on to store each operation performed, and saved to a .txt file.
- **Replication** allows for creating a copy of the vm at a specific state, allowing for search algorithms like BFS/DFS to be used.

The structure mirrors the classic Intcode VM from *Advent of Code 2019*, making the architecture modular, transparent, and extendable.

---

### 2. `SynacorConsole` — Automated Game Interaction Layer

Built to automate the process of exploring and solving the text adventure portion of the challenge.

Key features:

- **Text parsing & UI**
  Interprets room descriptions, exits, and item listings from game output.

- **Code extraction**
  Detects and stores special challenge codes using regex, along with their MD5 hashes.

- **HTML terminal renderer**
  Visually formats game output with syntax highlighting for easier debugging and review.

- **Breadth-First Search (BFS)** world traversal
  Systematically explores the game map, simulating user input and tracking visited rooms.

- **Inventory & item interaction management**
  Implements logic for item collection, conditional usage (e.g., filling and lighting a lantern), and backtracking prevention.

---

## 🚧 Challenges Encountered

### Room Uniqueness

One major challenge was identifying and tracking distinct rooms during BFS traversal.
Initially, room uniqueness was determined using an MD5 hash of the room description. However, this approach failed when rooms shared identical descriptions but were logically different (e.g., symmetrical branches or hidden exits),.

**Current workaround**:
- Room IDs are derived from hashed descriptions.
- Additional logic or in-game cues may be needed to disambiguate identical rooms.
- Overcame identical rooms, next to each other by a hardcoded solution.
- Removed the backtracking prevention, to allow for a more holistic solution, albeit coming at the cost of a longer solution.
- Solving the coins puzzle equation uses a over complicated solution, that could be simplified with a more hardcoded solution.

This remains an area for future improvement, potentially using exit structure, inventory state, or dynamic tagging of room paths.

---
## 🧩 Dependencies

- Python 3.8+
- `IPython.display` (for HTML terminal rendering)
- Standard libraries: `re`, `hashlib`, `collections`, `os`, `copy`, `itertools`

## 🚀 Getting Started

To run the automated exploration:

```python
console = SynacorConsole(software=program_bytes, spec_code="startCodeHere")
console.play_game()
