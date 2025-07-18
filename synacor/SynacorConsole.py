import os, re, time, copy
import html, hashlib, itertools, operator
from collections import defaultdict, deque
from IPython.display import display, HTML
from VirtualMachine import VirtualMachine
from VM_Disassembler import VM_Disassembler

class SynacorConsole:
    DIRECTIONS = {
            'south': (-1,0), 'north': (1, 0), 'east':  (0,1), 'west':  (0, -1),
        }
    OP_DICT = {
            '+': operator.add, '-': operator.sub, '*': operator.mul, '**': operator.pow
        }

    def __init__(self, software: bytes, spec_code: str, visualize: bool = True):
        self.software = software
        self.spec_code = spec_code
        self.visualize = visualize

        self.console = VirtualMachine(software)

        self.patched_software = None
        self.overall_commands = []
        self.maze_grid = None

        self.challenge_codes = defaultdict(tuple)
        self.valid_codes = set()
        self.code_no = 0

        self.start_time = time.time()
        self.prev_time = self.start_time

        # Preload spec code
        self.__extract_codes(" ", [spec_code])

    def mirror_image(self, string):
        """Return the mirror image of a string with mirrored 'b', 'p', 'q', 'd'."""
        mirror_map = {'b': 'd', 'p': 'q', 'q': 'p', 'd': 'b'}
        return re.sub(r"[bpqd]", lambda m: mirror_map[m.group()], string[::-1])

    def __extract_codes(self, text, codes = []):
        """
        Extract valid mixed-case challenge codes from the given text
        and record their MD5 hashes with timestamps.
        """
        # Pattern: must include at least one lowercase followed by uppercase and then lowercase again
        found = re.findall(r"[A-Za-z]*[a-z]+[A-Z]+[a-z]+[A-Za-z]*", text)
        if self.code_no == 7:
            all_strings = re.findall(r'"([\w]+)"', text)
            for test in all_strings:
                self.valid_codes.add(test)
            found = [self.mirror_image(test) for test in all_strings]
        codes.extend(found)
        current_time = time.time()

        for code in codes:
            if code not in self.valid_codes:
                self.code_no += 1
                total_time = f"{current_time - self.start_time:.5f}s"
                code_time = f"{current_time - self.prev_time:.5f}s"
                self.challenge_codes[self.code_no] = (
                    code, self.md5_hash(code), code_time, total_time,
                )
                self.valid_codes.add(code)
                self.prev_time = current_time

    @staticmethod
    def md5_hash(code):
        return hashlib.md5(code.encode('utf-8')).hexdigest()

    def __room_id(self, room_description):
        h = self.md5_hash(room_description.strip())
        # Take first 4 hex digits, convert to int, and mod 10000 to get a 4-digit number
        return int(h[:8], 16) % 10000

    def parse_equation(self, eq_str):
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
                        op_func = self.OP_DICT[ops[i]]
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
                # Escape any regex-special characters in valid codes
                pattern = r'\b(' + '|'.join(html.escape(code) for code in self.valid_codes) + r')\b'
                line = re.sub(
                    pattern, lambda m: f"<span style='color:{code_color}'>{m.group(1)}</span>",
                    line
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

    def __use_items(self, item):
        """Return actions to collect and use the item, and what items will be added to inventory."""
        if item == "empty lantern":
            return [f"take {item}", "use can", "use lantern"], {"lit lantern"}
        elif item in {"strange book", "business card"}:
            return [f"take {item}", f"look {item}"], {item}
        elif item in ["journal", "orb"] or "coin" in item:
            return [f"take {item}"], {item}
        else:
            return [f"take {item}", f"use {item}"], {item}

    def __solve_coins_slot(self, inventory, game_copy, equation):
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
        solution = next(filter(self.parse_equation(equation),
                        itertools.permutations(coin_dict.keys())))

        # Use coins in the determined order
        use_coins = [f"use {coin_dict[num]}" for num in solution]
        return look_coins + use_coins

    def __debug_vm(self, test_console):
        """
        Constructs a software patch function that:
        - Detects where register R7 is used.
        - Finds the correct value to set R7 so that Ackermann(4, 1, R7) == 6.
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
        ackermann_soln = next(
            filter(
                lambda k: disassembler.ackermann_func(4, 1, k, M) == 6,
                itertools.chain(range(start_guess, M), range(1, start_guess))
            )
        )
        return target_address, next_patch_point, ackermann_soln

    def build_software_patch(self, game_copy, action_list):
        test_console = game_copy.reset_machine(trace_log = [])
        test_console.run_computer(action_list)
        target_address, next_patch_point, ackermann_soln = self.__debug_vm(test_console)

        def patched_software(pointer, registers, memory):
            if pointer == target_address:
                registers[7] = ackermann_soln
                pointer += 1
            elif pointer == next_patch_point:
                memory[next_patch_point] = memory[next_patch_point + 1] = 21  # NOOP
                registers[0] = 6
                pointer += 2
            return pointer, registers, memory

        # Optional: print the patch function as a string for inspection or debugging
        patch_str = f"""
        def software_patch(pointer, registers, memory):
            if pointer == {target_address}:
                registers[7] = {ackermann_soln}
                pointer += 1
            elif pointer == {next_patch_point}:
                memory[{next_patch_point}] = memory[{next_patch_point + 1}] = 21  # NOOP
                registers[0] = 6
                pointer += 2
            return pointer, registers, memory
            """

        self.patched_software = patched_software
        self.patch_code_str = patch_str
        return patched_software, patch_str

    def build_maze(self, init_maze, next_action):
        """Explore and build a maze using BFS traversal from the initial maze state."""
        def extract_symbol(text):
            """Extract the first symbol or number ('*', '+', '-', or digits) from room text."""
            matches = re.findall(r"'([*+\-]|\d+)'", text)
            return matches if matches else ' '

        start, goal, eq_sum = ((0, 0), None, None)
        visited, maze_dict = (set(), defaultdict(str))
        queue = deque([(init_maze.replicate(), next_action, start)])

        while queue:
            maze_state, actions, pos = queue.popleft()
            if pos in visited:
                continue
            visited.add(pos)

            # Run VM and parse state
            maze_vm = maze_state.replicate()
            *_, terminal_output = maze_vm.run_computer(actions)
            room_name, _, _, exits = self.__parse_game_state(terminal_output)

            if room_name == "Tropical Cave":
                continue

            symbols = extract_symbol(terminal_output)
            maze_dict[pos] = symbols[0]
            if "vault" in exits:
                goal = pos
                eq_sum, sym_2 = symbols
                maze_dict[pos] = sym_2

            # Queue neighboring rooms
            for direction in exits:
                delta = self.DIRECTIONS.get(direction)
                if delta:
                    new_pos = (pos[0] + delta[0], pos[1] + delta[1])
                    queue.append((maze_vm, [direction], new_pos))
        self.maze_grid = (maze_dict, (start, goal), eq_sum)
        return maze_dict

    def render_grid(self, grid_props):
        """Render a 2D grid dictionary with (y, x) coordinates into a string with visual spacing."""
        maze_dict, (start, goal), eq_sum = grid_props
        if not maze_dict:
            return ""

        # Compute bounds
        xs = [x for _, x in maze_dict.keys()]
        ys = [y for y, _ in maze_dict.keys()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)


        output = []

        for y in reversed(range(min_y, max_y + 1)):
            row = []
            for x in range(min_x, max_x + 1):
                val = maze_dict.get((y, x), ' ')
                formatted = f"({int(val):02})" if val.isdigit() else f"({val:>2})"

                if (y, x) == goal:
                    formatted = f"{formatted} = {eq_sum}"
                elif (y, x) == start:
                    formatted = f"S -> {formatted}"
                elif x == start[1]:
                    formatted = f"     {formatted}"

                row.append(formatted)
            output.append(" --- ".join(row))

            # Build connector row (skip after bottom row)
            if y > min_y:
                connectors = []
                for x in range(min_x, max_x + 1):
                    if (y, x) in maze_dict and (y - 1, x) in maze_dict:
                        connector = "  | "
                        if x == start[1]:
                            connector = "     " + connector
                        connectors.append(connector)
                    else:
                        connectors.append("    ")
                output.append("     ".join(connectors))

        return output

    def __solve_grid_puzzle(self, game_copy, pending_actions):

        next_action = ["look journal"]
        maze_copy = game_copy.replicate()

        # *_, journal_entry = maze_copy.run_computer(next_action)
        # self.display_terminal(journal_entry, next_action)

        maze_formed= self.build_maze(maze_copy, pending_actions)

        return []

    def bfs_exploration(self):
        """Perform BFS to explore and map out the game world."""
        collect_coins = {'concave coin', 'shiny coin', 'red coin', 'blue coin', 'corroded coin'}
        coins_puzzle, mystery_puzzle, grid_puzzle = (False, False, False)
        visited, complete_solution = (set(), [])
        steps,  MAX_STEPS = (0, 1500)

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
            if "mirror" in game_inv:
                # self.display_terminal(last_terminal, pending_actions)
                complete_solution.append(action_history[:])
                break

            # Parse game state
            room, purpose, all_items, room_exits = self.__parse_game_state(last_terminal)
            room_id = self.__room_id(purpose)

            # if 'journal' in game_inv and room == "Vault Antechamber" and "take orb" in action_history:
            #     complete_solution.append(action_history[:])

            if 'mirror' in game_inv:
                complete_solution.append(action_history[:])

            # Skip if already visited with current inventory
            if (room_id, tuple(game_inv)) in visited:
                continue
            visited.add((room_id, tuple(game_inv)))

            # Clone game_inv for branching paths
            base_inv = game_inv.copy()

            # Condition: Check IF coin puzzle is reached
            if (len(collect_coins & game_inv) == 5 and room_id == 7578) and not coins_puzzle:
                equation = next((line.strip() for line in last_terminal.splitlines() if " = " in line), None)
                coin_solution = self.__solve_coins_slot(game_inv, game_copy, equation)
                action_history.extend(coin_solution)
                future_actions.extend(coin_solution)
                base_inv = {"all coins used", "lit lantern", "tablet"}
                queue.append((game_copy, base_inv, coin_solution, action_history))
                coins_puzzle = True

            # Condition: Check IF strange book has been collected
            if ("look strange book" in pending_actions) and not mystery_puzzle:
                patched_software, patch_str = self.build_software_patch(game_copy, action_history)
                next_actions, item_made = (["use teleporter"], "patched software")
                game_copy.monkey_patching(patched_software)
                base_inv.add(item_made)
                action_history.append(item_made)
                action_history.extend(next_actions)
                future_actions.extend(next_actions)
                queue.append((game_copy, base_inv, future_actions, action_history))
                mystery_puzzle = True

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

            # Condition: Check if journal/orb is collected and solve grid puzzle
            if (room_id == 5141 and "journal" in game_inv and "take orb" in action_history) and not grid_puzzle:
                grid_actions = self.__solve_grid_puzzle(game_state, pending_actions)
                base_inv.update("enter maze")
                future_actions.extend(grid_actions)
                action_history.append("enter maze")
                action_history.extend(grid_actions)
                queue.append((game_copy, base_inv, future_actions, action_history))
                grid_puzzle = True

        print("Steps:",steps)
        return complete_solution, self.challenge_codes

    def __restructure_commands(self, command_list):
        regrouped_commands, current_group = ([[]], [])
        for action in command_list:
            if action in ["patched software", "enter maze"]:
                if current_group:
                    regrouped_commands.append(current_group)
                regrouped_commands.append(action)
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

        full_game_run = self.console.replicate()
        for action_group in regrouped_commands:
            if action_group == "patched software":
                if self.visualize:
                    print(self.patch_code_str)
                full_game_run.monkey_patching(self.patched_software)
            elif action_group == "enter maze":
                rendered_maze = self.render_grid(self.maze_grid)
                if self.visualize:
                    print(f"        Math Maze Discovered:")
                    for line in rendered_maze:
                        print(' ' * 15 + line)
            else:
                *_, full_terminal = full_game_run.run_computer(action_group)
                # if self.visualize:
                #     self.display_terminal(full_terminal, action_group)
        return regrouped_commands, bfs_times
