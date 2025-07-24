class ERROR:
    InvalidSymbol = type('InvalidSymbolError', (Exception,), {
        '__doc__': 'Invalid symbol (parsing)'
    })
    """Exception raised when a symbol is invalid (parsing)."""

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

        self.MAX_STATES = 2**10,       # 1024
        self.MAX_TAPE_LEN = 2**20      # 1 048 576 cells
        self.MAX_STATE_SIZE = 32       # 32 Chars
        self.TRANSITION_SIZE = 710_000 # 710,000 Chars

    def _set_tape(self, input_tape: str) -> None:
        if " " in input_tape:
            raise ERROR.InvalidSymbol(
                "Input tape must not contain spaces"
            )

        self.head_position: int = 0
        self.current_state: str = self.init_state
        self.tape: dict[int, str] = {
            i: symbol for i, symbol in enumerate(input_tape)
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

    def _print_tape_state(self, input_tape: str):
        move_syms = {"L":"<", "R":">"}
        bounds = self._get_tape_boundaries()
        head_pos_in_window = self.head_position - min(bounds)
        tape_str = self._render_tape(bounds, strip_blank=False)
        printed_state = []
        printed_state.append(tape_str)
        printed_state.append((" " * head_pos_in_window + "^"))
        printed_state.append(self.current_state)
        printed_state.append("")
        print("\n".join(printed_state))

    def run_logic(
        self,
        input_tape: str,
        MAX_STEPS: int = 1_000_000,
        visualize: bool = False
    ) -> tuple[str, int]:

        self._set_tape(input_tape)
        if visualize:
            self._print_tape_state(input_tape)

        tape, steps = (input_tape, 0)
        return tape, steps

