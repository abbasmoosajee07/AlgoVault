"""i18n Puzzles - Puzzle 18
Solution Started: Jun 6, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/18
Solution by: Abbas Moosajee
Brief: [Rex To Lynx]
"""

#!/usr/bin/env python3

import os, re, copy, time, ast, operator
start_time = time.time()

# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path, encoding="utf-8") as file:
    input_data = file.read().strip().split('\n')

class Scam_Checker:
    BIDI_CONTROLS = {'\u2067': '<', '\u2066': '>', '\u2069': '^'}
    REVERSE_DICT  = {'(':')', ')':'(', '[': ']', ']': '[', '{': '}', '}': '{'}

    def parse_equation(self, init_eq):
        token_pattern = re.compile(
            fr'([{re.escape("".join(self.BIDI_CONTROLS))}])|(\d+)|([()+\-*/])'
        )
        return [m.group(0) for part in init_eq.split() for m in token_pattern.finditer(part)]

    @staticmethod
    def evaluate_sum(equation: str):
        ops = {
            ast.Add: operator.add,  ast.Sub: operator.sub,
            ast.Mult: operator.mul, ast.Div: operator.truediv,
            ast.USub: operator.neg,
        }
        def eval_node(node):
            if isinstance(node, ast.BinOp):
                return ops[type(node.op)](eval_node(node.left), eval_node(node.right))
            elif isinstance(node, ast.UnaryOp):
                return ops[type(node.op)](eval_node(node.operand))
            elif isinstance(node, ast.Constant):  # For Python 3.8+
                return node.value
            else:
                raise ValueError("Unsupported expression")
        try:
            tree = ast.parse(equation, mode='eval')
            return round(eval_node(tree.body))
        except Exception as e:
            print(f"Error: {e}")
            return None

    def __strip_eq(self, full_eq):
        stripped_text = []
        for c in full_eq:
            if c not in self.BIDI_CONTROLS.keys():
                stripped_text.append(c)
        return ''.join(stripped_text)

    def project_rex(self, og_bill):
        strip_bill = self.__strip_eq(og_bill)
        bill_value = self.evaluate_sum(strip_bill)
        return bill_value, strip_bill

    def __equation_str(self, use_eq):
        return ''.join(self.BIDI_CONTROLS.get(c, c) for c, _ in use_eq.values())

    def __identify_stretch(self, eq_dict, for_embed):
        streaks, streak = ([], [])
        max_idx = sorted(idx for idx, (_, level) in eq_dict.items() if level == for_embed)
        for idx in max_idx:
            if streak and idx != streak[-1] + 1:
                streaks.append(streak)
                streak = []
            streak.append(idx)
        if streak:
            streaks.append(streak)
        return max(streaks, key=len)

    def __reverse_string(self, eq_dict):
        rev_eq = copy.deepcopy(eq_dict)
        max_embed = max(emb for _, emb in eq_dict.values())
        stretch = self.__identify_stretch(eq_dict, max_embed)
        if len(stretch) <= 1:
            rev_eq[stretch[0]][1] -=1
        else:
            for c1, c2 in zip(stretch, stretch[::-1]):
                init_char, base_embed = eq_dict[c2]
                rev_char = self.REVERSE_DICT.get(init_char, init_char)
                rev_eq[c1] = [rev_char, base_embed - 1]
        return rev_eq, stretch

    def project_lynx(self, equation, debug: bool = False):
        eq_dict, embed_level, max_embed, flip_no = ({}, 0, 0, 0)
        for char_idx, char in enumerate(equation):
            # Determine effective embed level for this character
            level = embed_level + 1 if (char.isdigit() and embed_level % 2 == 1) else embed_level
            eq_dict[char_idx] = [char, level]
            max_embed = max(max_embed, level)
            # Update embedding level based on BIDI control characters
            if char in {"\u2067", "\u2066"}:  # RLI, LRI
                embed_level += 1
            elif char == "\u2069":  # PDI
                embed_level = max(embed_level - 1, 0)
                eq_dict[char_idx][1] = embed_level  # override level for PDI
        if debug:
            embed_str = [str(eq_dict[idx][1]) * len(str(eq_dict[idx][0])) for idx in sorted(eq_dict)]
            print("Input line short :", self.__equation_str(eq_dict))
            print("Embedding levels :", ''.join(embed_str))

        while max_embed >= 1:
            eq_dict, flip_stretch = self.__reverse_string(eq_dict)
            max_embed = max(level for (_, level) in eq_dict.values())
            if debug and len(flip_stretch) >= 2:
                flip_no += 1
                flip_str = ''.join(
                    '_' * len(char) if idx in flip_stretch else ' ' * len(char)
                    for idx, (char, _) in eq_dict.items()
                )
                print(f"  Flip Positions :", flip_str)
                print(f"  After {flip_no:02d} flips : {self.__equation_str(eq_dict)}")
        flipped_bill = ''.join(char for char, _ in eq_dict.values())
        stripped_bill = self.__strip_eq(flipped_bill)
        bill_value = self.evaluate_sum(stripped_bill)
        return bill_value, stripped_bill

    def count_scams(self, bill_list, debug: bool = False):
        scam_counter = {}
        for bill_no, bill in enumerate(bill_list, start = 1):
            parsed_bill = self.parse_equation(bill)
            rex_value, rex_eq = self.project_rex(parsed_bill)
            lynx_value, lynx_eq = self.project_lynx(parsed_bill, debug)
            abs_diff = abs(rex_value - lynx_value)
            scam_counter[bill_no] = abs_diff
            if debug:
                print(" Rex Eq:", rex_eq)
                print("Lynx Eq:", lynx_eq)
                print(f"Bill {bill_no}: Abs_diff = {abs_diff} | Lynx = {lynx_value} | Rex = {rex_value}")
        return scam_counter

total_scams = Scam_Checker().count_scams(input_data)
print("Total Scams Value:", sum(total_scams.values()))

# print(f"Execution Time = {time.time() - start_time:.5f}s")
