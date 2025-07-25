class ERROR:
    InvalidSymbol = type('InvalidSymbolError', (Exception,), {
        '__doc__': 'Invalid symbol (parsing)'
    })
    """Exception raised when a symbol is invalid (parsing)."""

    InvalidState = type('InvalidStateError', (Exception,), {
        '__doc__': 'Invalid state (parsing)'
    })
    """Exception raised when a state is invalid (parsing)."""

    InvalidTransition = type('InvalidTransitionError', (Exception,), {
        '__doc__': 'Invalid transition (parsing)'
    })
    """Exception raised when a transition is invalid (parsing)."""

    MissingTransition = type('MissingTransitionError', (Exception,), {
        '__doc__': 'Missing transition (parsing)'
    })
    """Exception raised when a transition is missing (parsing)."""

class LogicMill:
    """Logic Mill Implementation"""
    # The tape length is limited to 2^20 cells (1 048 576 cells).
    # The number of states is limited to 2^10 (1024 states).
    # State might be any string of up to 32 chars.
    # The list of the transition rules is limited to 710 000 characters.
    # The Mill has one tape and one head.
    TransitionType = tuple[str, str, str, str, str]

    def __init__(
        self,
        transitions_list: list,
        init_state: str = "INIT",
        halt_state: str = "HALT",
        blank_symbol: str = "_",
    ) -> None:
        self.init_state = init_state
        self.halt_state  = halt_state
        self.blank_symbol = blank_symbol

        self.head_position: int = None
        self.current_state: str = None
        self.tape: dict[int, str] = {}

        self.MAX_STATES = 2**10     # 1024
        self.MAX_TAPE_LEN = 2**20      # 1 048 576 cells
        self.MAX_STATE_SIZE = 32       # 32 Chars
        self.TRANSITION_SIZE = 710_000 # 710,000 Chars
        self.running = True

        self.transitions_list = transitions_list
        self.transitions_dict = self._build_transition_dict(
            transitions_list, init_state, halt_state
        )

    def _validate_transitions(self, transition):
        if len(transition) != 5:
            raise ERROR.InvalidTransition(
                f"Invalid transition: {transition}. Expected 5 elements: ",
                    "(currentState, currentSymbol, newState, newSymbol, moveDirection)."
            )

        current_state, current_symbol, new_state, new_symbol, direction = transition

        if direction not in {"L", "R"}:
            raise ERROR.InvalidTransition(f"Invalid move direction: {direction!r}. Must be 'L' or 'R'.")

        for symbol, label in [(current_symbol, "current"), (new_symbol, "new")]:
            if len(symbol) != 1:
                raise ERROR.InvalidSymbol(f"Invalid {label}_symbol: {symbol!r}. Must be a single character.")

        for state, label in [(current_state, "current"), (new_state, "new")]:
            if len(state) > self.MAX_STATE_SIZE:
                raise ERROR.InvalidSymbol(f"Invalid {label}_state: {state} size={len(current_state)}. State Size must be less than {self.MAX_STATE_SIZE} characters.")

        return current_state, current_symbol, new_state, new_symbol, direction

    def _build_transition_dict(
        self,
        transitions_list,
        init_state: str,
        halt_state: str,
        ) -> dict[str, dict[str, tuple[str, str, str]]]:

        transition_dict: dict[str, dict[str, tuple[str, str, str]]] = {}
        has_halt_state = False
        for transitions in transitions_list:
            current_state, current_symbol, new_state, new_symbol, move_direction = self._validate_transitions(transitions)

            # Check if current_state is present
            if current_state not in transition_dict:
                transition_dict[current_state] = {}

            if current_symbol in transition_dict[current_state]:
                raise ERROR.InvalidTransition(
                    f"Duplicate transition for state {current_state} and symbol {current_symbol}"
                )

            transition_dict[current_state][current_symbol] = (
                new_state, new_symbol, move_direction,
            )

            if new_state == halt_state:
                has_halt_state = True

        if len(transition_dict) > self.MAX_STATES:
            raise ERROR.InvalidTransition(
                f"Too many states: {len(transition_dict)}. Maximum is {self.MAX_STATES}."
            )

        if init_state not in transition_dict:
            raise ERROR.InvalidTransition(
                f"Initial state {init_state} not found in the transitions"
            )

        if not has_halt_state:
            raise ERROR.InvalidTransition(
                f"Halt state {halt_state} not found in the transitions"
            )
        return transition_dict

    def _set_tape(self, input_tape: str) -> None:
        if " " in input_tape:
            raise ERROR.InvalidSymbol("Input tape must not contain spaces")

        self.head_position = 0
        self.current_state = self.init_state
        self.tape = {
            idx: symbol for idx, symbol in enumerate(input_tape)
            if symbol != self.blank_symbol
            }

    def _get_tape_boundaries(self, tape = None, window: int = 10) -> tuple[int, int]:
        if not tape:
            tape = self.tape
        min_pos = min(tape.keys() if tape else self.head_position - window)
        max_pos = max(tape.keys() if tape else self.head_position + window)

        min_pos = min(min_pos, self.head_position - window)
        max_pos = max(max_pos, self.head_position + window)
        return min_pos, max_pos

    def _render_tape(self, bounds, strip_blank: bool = True) -> str:
        min_pos, max_pos = bounds
        tape_str = ""
        for i in range(min_pos, max_pos + 1):
            tape_str += self.tape.get(i, self.blank_symbol)

        if strip_blank:
            tape_str = tape_str.strip(self.blank_symbol)
        return tape_str

    def _print_tape_state(self, input_tape: dict):
        move_syms = {"L":"<", "R":">"}
        bounds = self._get_tape_boundaries()
        head_pos_in_window = self.head_position - min(bounds)
        tape_str = self._render_tape(bounds, strip_blank=False)
        printed_state = [
            tape_str,
            f"{' ' * head_pos_in_window}^",
            self.current_state,
            ""
        ]
        return tape_str, "\n".join(printed_state)

    def run_logic(
        self,
        input_tape: str,
        MAX_STEPS: int = 1_000_000,
        visualize: bool = False
    ) -> tuple[str, int]:

        self._set_tape(input_tape)
        if visualize:
            _, full_state = self._print_tape_state(input_tape)
            print(full_state)

        tape, steps = (input_tape, 0)
        return tape, steps
