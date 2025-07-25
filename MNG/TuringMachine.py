import os, re, copy, time, psutil
from LogicMill import LogicMill, TuringConfig

class TuringMachine:
    LEFT  = TuringConfig.LEFT
    RIGHT = TuringConfig.RIGHT
    BLANK = TuringConfig.BLANK
    COMMENT_PREFIX = TuringConfig.COMMENT_PREFIX

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

    def run_machine(self, instructions, init_tape):
        transition_rules = self.parse_transition_rules(instructions)
        mill = LogicMill(transition_rules)
        result, steps = mill.run_logic(init_tape, visualize =True)
        # print(f"Result: '{result}', Steps: {steps}")

        return transition_rules
