"""i18n Puzzles - Puzzle 18
Solution Started: Jun 6, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/18
Solution by: Abbas Moosajee
Brief: [Rex To Lynx]
"""

#!/usr/bin/env python3

import os, re, copy, time
import ast, operator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D18_file = "Day18_input1.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path, encoding="utf-8") as file:
    input_data = file.read().strip().split('\n')

class Scam_Checker:
    BIDI_CONTROLS = {
        # '\u200e': ("LRM", '⇉'), '\u200f': ("RLM", '⇇'),
        '\u202a': ("LRE", '→'), '\u202b': ("RLE", '←'),
        '\u202d': ("LRO", '}'), '\u202e': ("RLO", '{'),
        '\u2066': ("LRI", '>'), '\u2067': ("RLI", '<'),
        '\u2069': ("PDI", '^'), '\u202c': ("PDF", '◌'),
        '\u2068': ("FSI", '⋄'),
    }
    REVERSE_DICT = {'(':')', ')':'('}

    @staticmethod
    def convert_eq_dict(equation):
        return {char_idx: char for char_idx, char in enumerate(equation)}

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
            result = eval_node(tree.body)
            return int(result)
        except Exception as e:
            print(f"Error: {e}")
            return None

    def project_rex(self, og_bill: str = ""):
        stripped_text = []
        for c in og_bill:
            if c not in self.BIDI_CONTROLS.keys():
                stripped_text.append(c)
        strip_bill = ''.join(stripped_text)
        bill_value = self.evaluate_sum(strip_bill)
        return bill_value

    def visualize_bidi_algo(self, eq, bidi_pos):
        def build_equation(use_eq):
            return ''.join(Scam_Checker.BIDI_CONTROLS.get(c, (None, c))[1] for c in use_eq)
        fmt_eq = build_equation(eq)
        print("Input line short :", fmt_eq)
        return fmt_eq

    def project_lynx(self, equation: str = ""):
        # Input line short : 73 + (3 * (1 * ⏴(((3 + (6 - 2)) * 6) + ⏵((52 * 6) / ⏴(13 - (7 - 2))⏶)⏶)⏶))
        # Input line short : 73 + (3 * (1 * <(((3 + (6 - 2)) * 6) + >((52 * 6) / <(13 - (7 - 2))^)^)^))
        # Embedding levels : 00000000000000001112111121112111112111112222222222222344333343334332211000
        # Flips            :                                                       --
        #                                                                         --------------
        #                                                            -----------------------------
        #                                    -------------------------------------------------------
        # After 1st flip   : 73 + (3 * (1 * ⏴(((3 + (6 - 2)) * 6) + ⏵((52 * 6) / ⏴(31 - (7 - 2))⏶)⏶)⏶))
        # After 2nd flip   : 73 + (3 * (1 * ⏴(((3 + (6 - 2)) * 6) + ⏵((52 * 6) / ⏴((2 - 7) - 13)⏶)⏶)⏶))
        # After 3rd flip   : 73 + (3 * (1 * ⏴(((3 + (6 - 2)) * 6) + ⏵(⏶(31 - (7 - 2))⏴ / (6 * 25))⏶)⏶))
        # After 4th flip   : 73 + (3 * (1 * ⏴(⏶((52 * 6) / ⏴((2 - 7) - 13)⏶)⏵ + (6 * ((2 - 6) + 3)))⏶))
        # Result           : 73 + (3 * (1 * (((52 * 6) / ((2 - 7) - 13)) + (6 * ((2 - 6) + 3)))))

        bidi_pos = {}
        embed_level, embed_print = 0, ''
        eq_dict = self.convert_eq_dict(equation)

        matrix = []
        for char_idx, char in eq_dict.items():
            bidi_type, _ = self.BIDI_CONTROLS.get(char, (None, 0))
            if bidi_type is not None:
                bidi_pos[char_idx] = bidi_type
            embed_print += str(embed_level)
            if bidi_type in ["RLI", "LRI"]:
                embed_level += 1
            elif bidi_type == "PDI":
                embed_level -= 1
            else:
                matrix.append([char, embed_level])

        fmt_eq = self.visualize_bidi_algo(equation, bidi_pos)
        print("Embedding levels :", embed_print)
        # print('Embedding levels : 00000000000000001112111121112111112111112222222222222344333343334332211000')
        return 0

    def count_scams(self, bill_list, debug: bool = False):
        scam_counter = {}
        for bill_no, bill in enumerate(bill_list[-1:], start = 1):
            rex_value = self.project_rex(bill)
            lynx_value = self.project_lynx(bill)
            abs_diff = abs(rex_value - lynx_value)
            scam_counter[bill_no] = abs_diff
            if debug:
                print(f"Bill {bill_no}: Abs_diff = {abs_diff} | Lynx = {lynx_value} | Rex = {rex_value}")
        return scam_counter


total_scams = Scam_Checker().count_scams(input_data, True)
print("Total Scams Value:", sum(total_scams.values()))

print(f"Execution Time = {time.time() - start_time:.5f}s")

# Line 1 according to Lynx: 66, but according to Rex: 42. The absolute difference is: 24.
# Line 2 according to Lynx: 65, but according to Rex: 260. The absolute difference is: 195.
# Line 3 according to Lynx: 30720, but according to Rex: 15040. The absolute difference is: 15680.
# Line 4 according to Lynx: 5851, but according to Rex: 6300. The absolute difference is: 449.
# Line 5 according to Lynx: 139, but according to Rex: 2760. The absolute difference is: 2621.
# Line 6 according to Lynx: 3, but according to Rex: 316. The absolute difference is: 313.

