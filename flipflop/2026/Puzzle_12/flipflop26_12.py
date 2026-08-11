"""FlipFlop 2026: BitFlop Internship - Puzzle 12
Solution Started: August 10, 2026
Puzzle Link: https://flipflop.slome.org/2026/12
Solution by: Abbas Moosajee
Brief: [Bingo Bango Bongo]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict

# Load input file
input_file = "puzzle_12_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().split("\n\n")


class FlipFlopBingo:
    def __init__(self, bingo_cards):
        self.bingo_cards = bingo_cards

    @staticmethod
    def parse_2d_cards(bingo_cards):
        val_pos = defaultdict(list)
        for card_no, card_data in enumerate(bingo_cards.split("\n")):
            numbers = [int(n) for n in card_data.split()]
            rows = [numbers[i:i + 5] for i in range(0, len(numbers), 5)]
            for row_no, row_data in enumerate(rows):
                for col_no, val in enumerate(row_data):
                    val_pos[int(val)].append((card_no, row_no, col_no))
        return val_pos

    @staticmethod
    def _find_2d_bingos(total_rows, total_cols):
        rows = [[(row_no, col_no) for col_no in range(total_cols)] for row_no in range(total_rows)]
        cols = [[(row_no, col_no) for row_no in range(total_rows)] for col_no in range(total_cols)]
        diagonals = []
        if total_rows == total_cols:
            n = total_rows
            diagonals.append([(i, i) for i in range(n)])
            diagonals.append([(i, n - 1 - i) for i in range(n)])
        return rows + cols + diagonals

    @staticmethod
    def _check_bingos(marked_cards, valid_bingos):
        bingo_count = 0
        for marks in marked_cards.values():
            for possible_bingo in valid_bingos:
                if set(possible_bingo) <= marks:
                    bingo_count += 1
        return bingo_count

    def play_bingo(self, calls):
        val_pos = self.parse_2d_cards(self.bingo_cards)
        valid_bingos = self._find_2d_bingos(5, 5)

        marked_cards = defaultdict(set)
        for val in calls.split():
            for card_no, row, col in val_pos[int(val)]:
                marked_cards[card_no].add((row, col))
            if self._check_bingos(marked_cards, valid_bingos) >= 5:
                return val
        return -1

flip_bingo = FlipFlopBingo(data[1])

print("FlipFlop 2026, Puzzle 12")
print("Part 1:", flip_bingo.play_bingo(data[0]))
