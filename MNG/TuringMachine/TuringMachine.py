import copy, time, psutil, click

class TuringConfig:
    LEFT  = "L"
    RIGHT = "R"
    BLANK = "_"
    COMMENT_PREFIX = "//"

    MAX_STATES = 2**10         # 1024
    MAX_TAPE_LEN = 2**20       # 1 048 576 cells
    MAX_STATE_SIZE = 32        # 32 Chars
    TRANSITION_SIZE = 710_000  # 710,000 Chars

    TransitionType = tuple[str, str, str, str, str]

    InvalidSymbolError = type('InvalidSymbolError', (Exception,), {
        '__doc__': 'Invalid symbol (parsing)'
    })
    """Exception raised when a symbol is invalid (parsing)."""

    InvalidStateError = type('InvalidStateError', (Exception,), {
        '__doc__': 'Invalid state (parsing)'
    })
    """Exception raised when a state is invalid (parsing)."""

    InvalidTransitionError = type('InvalidTransitionError', (Exception,), {
        '__doc__': 'Invalid transition (parsing)'
    })
    """Exception raised when a transition is invalid (parsing)."""

    MissingTransitionError = type('MissingTransitionError', (Exception,), {
        '__doc__': 'Missing transition (parsing)'
    })
    """Exception raised when a transition is missing (parsing)."""

class MachineLogic:
    """Logic Mill Implementation"""

    def __init__(
        self,
        transitions_list: list[TuringConfig.TransitionType],
        init_state: str = "INIT",
        halt_state: str = "HALT",
        blank_symbol: str = TuringConfig.BLANK,
    ) -> None:

        self.init_state = init_state
        self.halt_state  = halt_state
        self.blank_symbol = blank_symbol

        self.MAX_STATES = TuringConfig.MAX_STATES
        self.MAX_STATE_SIZE = TuringConfig.MAX_STATE_SIZE

        self.transitions_list = transitions_list
        self.transitions_dict = self._build_transition_dict(
            transitions_list, init_state, halt_state
        )

        # Initialize Tape
        self.head_position: int = None
        self.current_state: str = None
        self.tape: dict[int, str] = {}

        self.running = True

    def _validate_transitions(
        self,
        transition: TuringConfig.TransitionType
        ) -> TuringConfig.TransitionType:
        if len(transition) != 5:
            raise TuringConfig.InvalidTransitionError(
                f"Invalid transition: {transition}. Expected 5 elements: ",
                    "(currentState, currentSymbol, newState, newSymbol, moveDirection)."
            )

        current_state, current_symbol, new_state, new_symbol, direction = transition

        if direction not in {TuringConfig.LEFT, TuringConfig.RIGHT}:
            raise TuringConfig.InvalidTransitionError(f"Invalid move direction: {direction!r}. Must be 'L' or 'R'.")

        for symbol, label in [(current_symbol, "current"), (new_symbol, "new")]:
            if len(symbol) != 1:
                raise TuringConfig.InvalidSymbolError(f"Invalid {label}_symbol: {symbol!r}. Must be a single character.")

        for state, label in [(current_state, "current"), (new_state, "new")]:
            if len(state) > self.MAX_STATE_SIZE:
                raise TuringConfig.InvalidSymbolError(f"Invalid {label}_state: {state} size={len(current_state)}. State Size must be less than {self.MAX_STATE_SIZE} characters.")

        return current_state, current_symbol, new_state, new_symbol, direction

    def _build_transition_dict(
        self,
        transitions_list: list[TuringConfig.TransitionType],
        init_state: str,
        halt_state: str,
        ) -> dict[str, dict[str, tuple[str, str, str]]]:

        transition_dict: dict[str, dict[str, tuple[str, str, str]]] = {}
        has_halt_state = False
        for transitions in transitions_list:
            current_state, current_symbol, new_state, new_symbol, move_direction = self._validate_transitions(transitions)

            # Check if current_state is present in dict
            if current_state not in transition_dict:
                transition_dict[current_state] = {}

            # Check for duplication error
            if current_symbol in transition_dict[current_state]:
                raise TuringConfig.InvalidTransitionError(
                    f"Duplicate transition for state {current_state} and symbol {current_symbol}"
                )

            transition_dict[current_state][current_symbol] = (
                new_state, new_symbol, move_direction,
            )

            if new_state == halt_state:
                has_halt_state = True

        if len(transition_dict) > self.MAX_STATES:
            raise TuringConfig.InvalidTransitionError(
                f"Too many states: {len(transition_dict)}. Maximum is {self.MAX_STATES}."
            )

        if init_state not in transition_dict:
            raise TuringConfig.InvalidTransitionError(
                f"Initial state {init_state} not found in the transitions"
            )

        if not has_halt_state:
            raise TuringConfig.InvalidTransitionError(
                f"Halt state {halt_state} not found in the transitions"
            )
        return transition_dict

    def _set_tape(self, input_tape: str) -> None:
        if " " in input_tape:
            raise TuringConfig.InvalidSymbolError("Input tape must not contain spaces")

        self.head_position = 0
        self.current_state = self.init_state
        self.tape = {
            idx: symbol for idx, symbol in enumerate(input_tape)
            if symbol != self.blank_symbol
            }

    def _get_tape_boundaries(self, window: int = 10) -> tuple[int, int]:
        min_pos = min(self.tape.keys() if self.tape else self.head_position - window)
        max_pos = max(self.tape.keys() if self.tape else self.head_position + window)

        min_pos = min(min_pos, self.head_position - window)
        max_pos = max(max_pos, self.head_position + window)
        return min_pos, max_pos

    def _print_tape_state(self, visualize_state: bool = True) -> str:
        min_pos, max_pos = self._get_tape_boundaries()
        head_pos_in_window = self.head_position - min_pos

        tape_str = ""
        for i in range(min_pos, max_pos + 1):
            tape_str += self.tape.get(i, self.blank_symbol)

        printed_state = [
            tape_str,
            f"{' ' * head_pos_in_window}^",
            self.current_state,
            ""
        ]
        if visualize_state:
            print("\n".join(printed_state))
        tape_only = tape_str.strip(self.blank_symbol)
        return tape_only

    def _step_logic(self) -> None:
        """Internal helper for stepping forward one transition."""
        state_transitions = self.transitions_dict.get(self.current_state, None)
        if not state_transitions:
            raise TuringConfig.MissingTransitionError(
                f"No transitions for state {self.current_state} with input tape {self.input_tape}"
            )

        current_symbol = self.tape.get(self.head_position, self.blank_symbol)
        transition = state_transitions.get(current_symbol, None)
        if not transition:
            raise TuringConfig.MissingTransitionError(
                f"No transition for symbol {current_symbol or self.blank_symbol} "
                f"in state {self.current_state} with input tape {self.input_tape}"
            )

        new_state, new_symbol, move_direction = transition

        # Write new symbol to tape
        if new_symbol == self.blank_symbol:
            self.tape.pop(self.head_position, None)
        else:
            self.tape[self.head_position] = new_symbol

        # Move head
        shift = {"L": -1, "R": +1}[move_direction]

        self.current_state = new_state
        self.head_position += shift

    def run_logic(
        self,
        input_tape: str,
        *,
        MAX_STEPS: int = 1_000_000,
        visualize: bool = False
    ) -> tuple[str, int, int]:

        self.input_tape = input_tape
        self._set_tape(input_tape)
        self._print_tape_state(visualize)

        step_count = 0
        while self.running and step_count < MAX_STEPS:
            if self.current_state == self.halt_state:
                self.running = False
                if visualize:
                    print(f"HALTED after {step_count} steps")
                continue

            self._step_logic()
            tape = self._print_tape_state(visualize)
            step_count += 1

        return tape, step_count, len(self.transitions_list)

    def run_step(self, input_tape, visualize: bool = True, MAX_STEPS=1_000_000):
        print("Turing Machine Initialized:")
        self.input_tape = input_tape
        self._set_tape(input_tape)
        self._print_tape_state(visualize)

        step_count = 0
        tape = ""  # in case machine halts before any steps

        while self.running and step_count < MAX_STEPS:
            if self.current_state == self.halt_state:
                self.running = False
                if visualize:
                    print(f"HALTED after {step_count} steps")
                break

            click.echo("Press Enter/Space to step, digit to step N times, or 'q' to quit:\n")
            key = click.getchar()

            if key == 'q':
                print("Machine Stopped Manually")
                break

            elif key in ['\r', '\n', ' ']:
                self._step_logic()
                step_count += 1
                tape = self._print_tape_state(visualize)

            elif key.isdigit():
                steps_to_run = int(key)
                for _ in range(steps_to_run):
                    if self.current_state == self.halt_state or not self.running:
                        break
                    self._step_logic()
                    step_count += 1
                    tape = self._print_tape_state(visualize)

            else:
                print(f"Unrecognized key: {repr(key)}")

        return tape, step_count, len(self.transitions_list)

class TuringMachine:
    LEFT  = TuringConfig.LEFT
    RIGHT = TuringConfig.RIGHT
    BLANK = TuringConfig.BLANK
    COMMENT_PREFIX = TuringConfig.COMMENT_PREFIX

    def __init__(self, instructions):
        self.init_time = self.get_timestamp()
        self.init_memory = self.get_current_memory_mb()
        self.transition_rules = self.parse_transition_rules(instructions)

    @staticmethod
    def get_timestamp() -> float:
        return time.time()

    @staticmethod
    def get_current_memory_mb() -> float:
        process = psutil.Process()
        mem_bytes = process.memory_info().rss  # Resident Set Size (physical memory)
        return round(mem_bytes / (1024 * 1024), 2)  # Convert bytes to MB

    def parse_transition_rules(
        self,
        transition_rules_str: str
        ) -> list[TuringConfig.TransitionType]:
        """
        Parse a string into a list of transition rules for the logic mill.
        Args:
            transition_rules_str: A string containing transition rules, with each rule on a new line.
                Each rule should be space-separated values in the format:
                currentState currentSymbol newState newSymbol moveDirection
        Returns:
            A list of transition tuples:
            (currentState, currentSymbol, newState, newSymbol, moveDirection)
        Raises:
            ValueError: If a rule is invalid (e.g., wrong number of tokens or invalid direction).
        """

        transitions_list: list[TuringConfig.TransitionType] = []
        raw_rule_list = transition_rules_str.split("\n")
        for raw_line in raw_rule_list:
            line = raw_line.strip()
            if not line or line.startswith(self.COMMENT_PREFIX):
                continue

            # Remove inline comments
            line = line.split(self.COMMENT_PREFIX, 1)[0].strip()
            values = [val for val in line.split(" ") if val.strip()]

            if len(values) != 5:
                raise TuringConfig.InvalidTransitionError(
                    f"Invalid transition: {values}. Expected 5 elements got {len(values)}  ",
                )

            current_state, current_symbol, new_state, new_symbol, direction = values
            if direction not in (self.LEFT, self.RIGHT):
                raise TuringConfig.InvalidTransitionError(f"Invalid moveDirection: {direction}. Must be L or R")

            for symbol, label in [(current_symbol, "current"), (new_symbol, "new")]:
                if len(symbol) != 1:
                    raise TuringConfig.InvalidSymbolError(f"Invalid {label}_symbol: {symbol!r}. Must be a single character.")

            transitions_list.append((current_state, current_symbol, new_state, new_symbol, direction))
        return transitions_list

    def run_machine(self, init_tape, play_type: 0, visualize: bool = True):
        """
        Run the Turing machine on the initial tape with optional visualization.
        0: Auto_play
        1: Manual_play
        """
        transition_rules = self.transition_rules.copy()

        cpu = MachineLogic(transition_rules)
        if play_type == 0:
            final_tape, steps, rules_no = cpu.run_logic(init_tape, visualize=visualize)
        elif play_type == 1:
            final_tape, steps, rules_no = cpu.run_step(init_tape, visualize=visualize)

        resources_used = [
            f"   Time run: {self.get_timestamp() - self.init_time:.5f}s",
            f"Memory used: {self.get_current_memory_mb()}MB"
        ]

        results = [
            f"Result Tape: '{final_tape}'",
            f"Steps Count: {steps}",
            f"Total Rules: {rules_no}",
        ]

        return transition_rules, results, resources_used

if __name__ == "__main__":

    init_rules = """
        INIT | FIND | R
        FIND | FIND | R
        FIND _ HALT | R
        """
    init_tape = "||||"

    _, results, used_resources = TuringMachine(init_rules).run_machine(init_tape, play_type = 1, visualize=True)
    print_info = results + [""] + used_resources
    print("\n".join(print_info))