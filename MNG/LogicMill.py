class TuringConfig:
    LEFT  = "L"
    RIGHT = "R"
    BLANK = "_"
    COMMENT_PREFIX = "//"
    TransitionType = tuple[str, str, str, str, str]

    MAX_STATES = 2**10         # 1024
    MAX_TAPE_LEN = 2**20      # 1 048 576 cells
    MAX_STATE_SIZE = 32       # 32 Chars
    TRANSITION_SIZE = 710_000 # 710,000 Chars

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

class LogicMill:
    """Logic Mill Implementation"""

    def __init__(
        self,
        transitions_list: list[TuringConfig.TransitionType],
        init_state: str = "INIT",
        halt_state: str = "HALT",
        blank_symbol: str = "_",
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

    def _render_tape(self, bounds, strip_blank: bool = True) -> str:
        min_pos, max_pos = bounds
        tape_str = ""
        for i in range(min_pos, max_pos + 1):
            tape_str += self.tape.get(i, self.blank_symbol)

        if strip_blank:
            tape_str = tape_str.strip(self.blank_symbol)
        return tape_str

    def _print_tape_state(self, visualize_state: bool = True):
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
        if visualize_state:
            print("\n".join(printed_state))
        return tape_str

    def run_logic(
        self,
        input_tape: str,
        MAX_STEPS: int = 1_000_000,
        visualize: bool = False
    ) -> tuple[str, int]:
        steps = 0
        self._set_tape(input_tape)
        if visualize:
            self._print_tape_state(visualize)
        while self.running and steps < MAX_STEPS:
            self.running = False

        tape, steps = (input_tape, 0)
        return tape, steps
