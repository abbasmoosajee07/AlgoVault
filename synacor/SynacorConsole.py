import os, re, time, copy
import html, hashlib, itertools, operator
from collections import defaultdict, deque
from IPython.display import display, HTML
from VirtualMachine import VirtualMachine
from VM_Disassembler import VM_Disassembler

class SynacorConsole:

    def __init__(self, software: bytes, spec_code: str, visualize: bool = True):
        self.software = software
        self.visualize = visualize
        self.spec_code = spec_code
        self.patched_software = None
        self.console = self.reset_console()

    def reset_console(self):
        """Reset console state and reinitialize the virtual machine."""
        console = VirtualMachine(self.software)
        self.challenge_codes = defaultdict(tuple)
        self.overall_commands = []
        self.valid_codes = set()
        self.code_no = 0
        self.start_time = time.time()
        self.prev_time = self.start_time
        self.__extract_codes(" ", [self.spec_code])  # Preload spec code
        return console

    def __extract_codes(self, text, codes = []):
        """
        Extract valid mixed-case challenge codes from the given text
        and record their MD5 hashes with timestamps.
        """
        # Pattern: must include at least one lowercase followed by uppercase and then lowercase again
        found = re.findall(r"[A-Za-z]*[a-z]+[A-Z]+[a-z]+[A-Za-z]*", text)
        codes.extend(found)

        new_codes = []
        current_time = time.time()

        for code in codes:
            if code not in self.valid_codes:
                self.code_no += 1
                total_time = f"{current_time - self.start_time:.5f}s"
                code_time = f"{current_time - self.prev_time:.5f}s"
                self.challenge_codes[self.code_no] = (
                    code, self.md5_hash(code), code_time, total_time,
                )
                new_codes.append(code)
                self.valid_codes.add(code)
                self.prev_time = current_time

        return new_codes

    @staticmethod
    def md5_hash(code):
        return hashlib.md5(code.encode('utf-8')).hexdigest()

    def create_room_id(self, room_description):
        h = self.md5_hash(room_description.strip())
        # Take first 4 hex digits, convert to int, and mod 10000 to get a 4-digit number
        return int(h[:8], 16) % 10000

    @staticmethod
    def parse_equation(eq_str):
        lhs, rhs = eq_str.split('=')
        rhs = int(rhs.strip())
        # Replace underscores with placeholder p[i]
        parts = re.split(r'(_)', lhs.strip())
        indices = [i for i, x in enumerate(parts) if x == '_']

        def equation(p):
            expr = parts[:]
            for i, idx in enumerate(indices):
                expr[idx] = str(p[i])
            expr_str = ''.join(expr).replace('^', '**')

            # Tokenize
            tokens = re.findall(r'\d+|[\+\-\*]{1,2}', expr_str)

            # Evaluate with operator precedence: ** > * > +/-
            def apply(ops, precedence):
                stack = []
                i = 0
                while i < len(ops):
                    if ops[i] in precedence:
                        a, b = int(stack.pop()), int(ops[i+1])
                        op_func = {'+': operator.add, '-': operator.sub,
                                    '*': operator.mul, '**': operator.pow}[ops[i]]
                        stack.append(str(op_func(a, b)))
                        i += 2
                    else:
                        stack.append(ops[i])
                        i += 1
                return stack
            # Handle ** first, then *, then +/-
            for prec in (['**'], ['*'], ['+', '-']):
                tokens = apply(tokens, prec)

            return int(tokens[0]) == rhs

        return equation

    def __format_terminal(self, text, code_color, input_color):
        """Highlight any detected code-like strings in the terminal."""
        lines = []
        for line in text.splitlines():
            # Simple input highlight: lines starting with '>'
            if line.strip().startswith('>>'):
                line = f"<span style='color:{input_color}'>{line}</span>"
            else:
                line = re.sub(      # Example: highlight code-like patterns
                    r"\b((?:[a-z]+[A-Z]+[a-z]|[A-Z]+[a-z]+[A-Z])\w*)\b",
                    rf"<span style='color:{code_color}'>\1</span>", line
                )
            lines.append(line)
        return "\n".join(lines)

    def display_terminal(self, terminal_text, actions=[], terminal_size = 100):
        """Format and display terminal output with highlighted codes and interleaved actions."""
        self.color_dict = {
            "background": "#282828", "terminal": "#33FF00",
            "codes": "#FF0000", "input": "#0073FF"
        }
        html_valid_text = html.escape(terminal_text)
        html_valid_text = re.sub(r'\n{3,}', '\n\n', html_valid_text.strip())
        parts = re.split(r'(What do you do\?)', html_valid_text)

        output_lines = []

        if actions:
            output_lines.append(f">> {actions[0]}")
        action_index = 1 if actions else 0

        i = 0
        while i < len(parts):
            output_lines.append(parts[i])
            input_prompt = "What do you do?"
            if i + 1 < len(parts) and parts[i + 1] == input_prompt:
                output_lines.append(input_prompt)
                if action_index < len(actions):
                    output_lines.append(f">> {actions[action_index]}")
                    action_index += 1
                i += 2
            else:
                i += 1

        combined_text = "\n".join(output_lines)

        # Wrap lines longer than 150 characters at word boundaries
        def wrap_line(line, limit=terminal_size):
            if len(line) <= limit:
                return [line]
            result = []
            while len(line) > limit:
                split_at = line.rfind(' ', 0, limit)
                if split_at == -1:
                    split_at = limit  # hard break if no space found
                result.append(line[:split_at])
                line = line[split_at:].lstrip()
            if line:
                result.append(line)
            return result

        wrapped_lines = []
        for line in combined_text.split('\n'):
            wrapped_lines.extend(wrap_line(line))

        final_text = "\n".join(wrapped_lines)

        html_formatted = (
            f"<div style='background-color: {self.color_dict['background']}; "
            f"width: {terminal_size + 2}ch; padding: 0.75ex;'>"
            f"<pre style='background-color: {self.color_dict['background']}; "
            f"color: {self.color_dict['terminal']}; margin: 0; font-family: monospace; "
            f"width: {terminal_size + 2}ch;'>"
            + self.__format_terminal(final_text, self.color_dict['codes'], self.color_dict['input'])
            + "</pre></div>"
        )

        display(HTML(html_formatted))

    def play_game_manually(self, actions = []):
        """
        Game Instructions:
        - `look`: You may merely 'look' to examine the room, or you may 'look ' (such as 'look chair') to examine something specific.
        - `go`: You may 'go ' to travel in that direction (such as 'go west'), or you may merely '' (such as 'west').
        - `inv`: To see the contents of your inventory, merely 'inv'.
        - `take`: You may 'take ' (such as 'take large rock').
        - `drop`: To drop something in your inventory, you may 'drop '.
        - `use`: You may activate or otherwise apply an item with 'use '.
        """
        if actions:
            self.overall_commands.extend(actions)
        full_terminal = self.console.run_computer(actions)
        current_terminal = full_terminal[-1]
        self.__extract_codes(current_terminal)
        if self.visualize:
            self.display_terminal(current_terminal, actions)
        return self.overall_commands, self.challenge_codes

    def __parse_game_state(self, terminal):
        lines = terminal.splitlines()
        location, description, things, exits = ("", "", [], [])

        current_section = None
        for line_no, line in enumerate(lines):
            line = line.strip()
            if line.startswith("==") and line.endswith("=="):
                location = line.strip("= ").strip()
                description = lines[line_no + 1]
            elif line.startswith("Things of interest here:"):
                current_section = "things"
            elif line.startswith("There") and "exit" in line:
                current_section = "exits"
            elif line.startswith("-") and current_section:
                item = line[2:].strip()
                if current_section == "things":
                    things.append(item)
                elif current_section == "exits":
                    exits.append(item)
            else:
                current_section = None

        return location, description, things, exits

    def build_patch(self, test_console):
        """
        Constructs a software patch function that:
        - Detects where register R7 is used.
        - Finds the correct value to set R7 so that Ackermann(4, 1, R7) == 6.
        - Injects that value at runtime by patching the Virtual Machine state.
        """
        disassembler = VM_Disassembler(test_console)
        M = disassembler.M
        R7 = M + 7

        # --- Step 1: Find the first instruction that uses R7 ---
        target_address = None

        for addr, instr in disassembler.vm.trace_log:
            if R7 in instr:
                target_address = addr

        if target_address is None:
            raise RuntimeError("Could not find usage of R7 in trace log.")

        # --- Step 2: Disassemble next 21 instructions from that point ---
        next_patch_point, _ = disassembler.disassemble(target_address, 21)

        # --- Step 3: Brute-force to find value for R7 so that A(4, 1, k) == 6 ---
        start_guess = 25730
        solution = next(
            filter(
                lambda k: disassembler.ackermann_func(4, 1, k, M) == 6,
                itertools.chain(range(start_guess, M), range(1, start_guess))
            )
        )

        # --- Step 4: Define and return the software patch ---
        def software_patch(pointer, registers, memory):
            if pointer == target_address:
                registers[7] = solution
                pointer += 1
            elif pointer == next_patch_point:
                memory[next_patch_point] = memory[next_patch_point + 1] = 21  # NOOP
                registers[0] = 6
                pointer += 2
            return pointer, registers, memory

        # Optional: print the patch function as a string for inspection or debugging
        self.patch_code_str = f"""
    def software_patch(pointer, registers, memory):
        if pointer == {target_address}:
            registers[7] = {solution}
            pointer += 1
        elif pointer == {next_patch_point}:
            memory[{next_patch_point}] = memory[{next_patch_point + 1}] = 21  # NOOP
            registers[0] = 6
            pointer += 2
        return pointer, registers, memory
        """

        self.patched_software = software_patch
        return software_patch

    def __use_items(self, item):
        """Return actions to collect and use the item, and what items will be added to inventory."""
        if item == "empty lantern":
            return [f"take {item}", "use can", "use lantern"], {"lit lantern"}
        elif item in ["strange book", "business card", "journal"]:
            return [f"take {item}", f"look {item}",], {item}
        elif "coin" in item:
            return [f"take {item}"], {item}
        else:
            return [f"take {item}", f"use {item}"], {item}

    def __solve_coins_puzzle(self, inventory, game_copy, equation):
        word_to_num = {
            "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9,
            "digon": 2, "triangle": 3, "square": 4, "pentagon": 5,
            "hexagon": 6, "heptagon": 7, "octagon": 8, "nonagon": 9,
        }

        coin_items = [item for item in inventory if "coin" in item]
        look_coins = [f"look {item}" for item in coin_items]

        coin_game = game_copy.replicate()
        *_, final_terminal = coin_game.run_computer(look_coins)
        coin_lines = [line for line in final_terminal.splitlines() if "coin" in line]

        # Build coin_dict: shape/number -> coin item name
        coin_dict = defaultdict(str)
        for item in coin_items:
            coin_type = item.replace("coin", "").strip()
            coin_type = "rounded" if coin_type == "concave" else coin_type

            matching_line = next((line for line in coin_lines if coin_type in line), "")
            match = next((num for word, num in word_to_num.items() if word in matching_line), None)

            if match:
                coin_dict[match] = item

        # Solve the equation by trying permutations of the coin values
        solution = next(filter(self.parse_equation(equation), itertools.permutations(coin_dict.keys())))

        # Use coins in the determined order
        use_coins = [f"use {coin_dict[num]}" for num in solution]
        return look_coins + use_coins

    def __solve_mystery_puzzle(self, game_copy, action_list):
        test_console = game_copy.reset_machine(trace_log = [])
        test_console.run_computer(action_list)
        test_patch = self.build_patch(test_console)
        return test_patch, ["use teleporter"]

    def bfs_exploration(self):
        """Perform BFS to explore and map out the game world."""
        collect_coins = {'concave coin', 'shiny coin', 'red coin', 'blue coin', 'corroded coin'}
        coins_puzzle, mystery_puzzle, grid_puzzle = (False, False, False)
        visited, complete_solution = (set(), [])
        steps,  MAX_STEPS = (0, 1000)

        # Each entry: (console_state, pending_actions, path_so_far, action_history)
        # Use deque for efficient popping from the left
        queue = deque([(self.console, set(), [], [])])

        while queue and steps < MAX_STEPS:
            game_state, game_inv, pending_actions, action_history = queue.popleft()
            future_actions = []
            steps += 1

            # Run actions on a fresh copy of the game state
            game_copy = game_state.replicate(steps)
            *_, last_terminal = game_copy.run_computer(pending_actions)
            self.__extract_codes(last_terminal)

            # Parse game state
            room, purpose, all_items, room_exits = self.__parse_game_state(last_terminal)
            room_id = self.create_room_id(purpose)

            if 'journal' in game_inv and room == "Vault Antechamber":
                complete_solution.append(action_history[:])
                # break

            # Skip if already visited with current inventory
            if (room_id, tuple(game_inv)) in visited:
                continue
            visited.add((room_id, tuple(game_inv)))

            # Clone game_inv for branching paths
            base_inv = game_inv.copy()

            # Condition: Check IF coin puzzle is reached
            if (len(collect_coins & game_inv) == 5 and room_id == 7578) and not coins_puzzle:
                equation = next((line.strip() for line in last_terminal.splitlines() if " = " in line), None)
                coin_solution = self.__solve_coins_puzzle(game_inv, game_copy, equation)
                action_history.extend(coin_solution)
                future_actions.extend(coin_solution)
                base_inv = {"all coins used", "lit lantern", "tablet"}
                queue.append((game_copy, base_inv, coin_solution, action_history))
                coins_puzzle = True

            # Condition: Check IF strange book has been collected
            if ("look strange book" in pending_actions) and not mystery_puzzle:
                patched_software, next_actions = self.__solve_mystery_puzzle(game_copy, action_history)
                game_copy.monkey_patching(patched_software)
                base_inv.add("patched software")
                action_history.append("patched software")
                action_history.extend(next_actions)
                future_actions.extend(next_actions)
                queue.append((game_copy, base_inv, future_actions, action_history))
                mystery_puzzle = True

            if 'journal' in game_inv and not grid_puzzle:
                n2 = 0

            # Handle item collection
            for item in all_items:
                # Skip collecting lantern unless can is collected
                if (item == "empty lantern") and ("can" not in game_inv):
                    continue
                item_actions, collected = self.__use_items(item)
                base_inv.update(collected)
                future_actions.extend(item_actions)
                action_history.extend(item_actions)
                queue.append((game_copy, base_inv, future_actions, action_history))

            # Explore exits
            for direction in room_exits:
                is_dark_passage = (room_id == 1376) # Dark Passages ID

                # If override: move twice in the same direction
                dir_sequence = [direction, direction] if is_dark_passage else [direction]
                next_actions = future_actions + dir_sequence
                next_history = action_history + dir_sequence
                queue.append((game_copy, base_inv, next_actions, next_history))

        print("Steps:",steps)
        return complete_solution, self.challenge_codes

    def __restructure_commands(self, command_list):
        regrouped_commands, current_group = ([[]], [])
        for action in command_list:
            if action == "patched software":
                if current_group:
                    regrouped_commands.append(current_group)
                regrouped_commands.append("patched software")
                current_group = []
            else:
                current_group.append(action)
        if current_group:
            regrouped_commands.append(current_group)
        return regrouped_commands

    def auto_play(self):
        """Automatic playthrough using the bfs exploration."""
        game_commands, bfs_times = self.bfs_exploration()
        regrouped_commands = self.__restructure_commands(game_commands[0])

        full_game_run = self.reset_console()
        for action_group in regrouped_commands:
            if action_group == "patched software":
                print(self.patch_code_str)
                full_game_run.monkey_patching(self.patched_software)
            else:
                *_, full_terminal = full_game_run.run_computer(action_group)
                self.display_terminal(full_terminal, action_group)
                self.__extract_codes(full_terminal)
        print(self.challenge_codes)
        return regrouped_commands, bfs_times
