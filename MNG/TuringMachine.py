import time, psutil
from LogicMill import LogicMill

class TuringMachine:
    LEFT  = "L"
    RIGHT = "R"
    BLANK = "_"
    COMMENT_PREFIX = "//"
    TransitionType = tuple[str, str, str, str, str]

    def __init__(self):
        self.init_time = self.get_timestamp()
        self.init_memory = self.get_current_memory_mb()

    @staticmethod
    def get_timestamp() -> float:
        return time.time()

    @staticmethod
    def get_current_memory_mb() -> float:
        process = psutil.Process()
        mem_bytes = process.memory_info().rss  # Resident Set Size (physical memory)
        return round(mem_bytes / (1024 * 1024), 2)  # Convert bytes to MB

    def parse_transition_rules(self, transition_rules_str: str) -> list[TransitionType]:
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
        transitions_list = []
        for raw_line in transition_rules_str.split("\n"):
            line = raw_line.strip()
            if not line or line.startswith(self.COMMENT_PREFIX):
                continue

            # Remove inline comments
            line = line.split(self.COMMENT_PREFIX, 1)[0].strip()

            values = [val for val in line.split(" ") if val.strip()]

            if len(values) != 5:
                raise ValueError(f"Invalid transition rule (expected 5 elements): Recieved {len(values)} elements in line \n'{line}'")

            current_state, current_symbol, new_state, new_symbol, direction = values
            if direction not in (self.LEFT, self.RIGHT):
                raise ValueError(f"Invalid move direction '{direction}' in rule: '{line}'")

            transitions_list.append((current_state, current_symbol, new_state, new_symbol, direction))
        return transitions_list

    def run_machine(self):
        return
