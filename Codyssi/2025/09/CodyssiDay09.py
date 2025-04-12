"""Codyssi Puzzles - Problem 9
Solution Started: Apr 11, 2025
Puzzle Link: https://www.codyssi.com/view_problem_13?
Solution by: Abbas Moosajee
Brief: [Windy Bargain]
"""

#!/usr/bin/env python3

import os, re, copy

# Load the input data from the specified file path
D09_file = "Day09_input.txt"
D09_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D09_file)

# Read and sort input data into a grid
with open(D09_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    acc_dict = {name: int(val) for line in input_data[0].splitlines() for name, val in [line.split(" HAS ", 1)]}
    transac_list = [(line.split(' ')[1],line.split(' ')[3], int(line.split(' ')[-1])) for line in input_data[1].splitlines()]

class AccountManager:
    def __init__(self, acc_dict, transac_list):
        self.original_acc_dict = acc_dict
        self.transac_list = transac_list

    def complete_transactions(self, limit: bool = True):
        """
        Processes the list of transactions and computes the sum of the top 3 account balances 
        after all transactions are applied.

        If `limit` is True, a transaction from an account only transfers up to the available balance.\n
        If `limit` is False, it assumes unlimited.

        Args:
            limit (bool, optional): If True, restricts transfers to available balance.
                                    If False, transfers the full amount regardless of balance.
                                    Defaults to True.

        Returns:
            int or float: Sum of the top 3 highest balances after processing all transactions.
        """
        acc_dict = self.original_acc_dict.copy()
        for from_acc, to_acc, amt in self.transac_list:
            available = acc_dict[from_acc]
            transfer_amt = min(amt, available) if limit else amt
            acc_dict[from_acc] -= transfer_amt
            acc_dict[to_acc] += transfer_amt
        sorted_balances = sorted(acc_dict.values(), reverse=True)
        return sum(sorted_balances[:3])

    @staticmethod
    def settle_all_debts(acc_dict, debt_dict):
        progress = True
        while progress:
            progress = False
            updated_debt_dict = {}

            for account in list(debt_dict.keys()):
                debts = debt_dict[account]    # Outstading debts to be paid
                available = acc_dict[account] # Available Balance
                new_debts = []                # Remaining Debts

                for pay_to, debt_amt in debts:
                    if available == 0:        # Could not make a payment
                        new_debts.append((pay_to, debt_amt))
                        continue

                    if debt_amt <= available: # Completed Debt
                        acc_dict[account] -= debt_amt
                        acc_dict[pay_to] += debt_amt
                        available -= debt_amt
                        progress = True
                    else:                     # Made Partial Debt Payment
                        acc_dict[account] -= available
                        acc_dict[pay_to] += available
                        new_debts.append((pay_to, debt_amt - available))
                        available = 0
                        progress = True

                if new_debts:
                    updated_debt_dict[account] = new_debts

            debt_dict.clear()
            debt_dict.update(updated_debt_dict)

            return acc_dict, debt_dict

    def balance_books(self):
        acc_dict = self.original_acc_dict.copy()
        debt_dict = {}

        for (from_acc, to_acc, amt) in transac_list[:]:
            avail_val = acc_dict[from_acc]

            if amt > avail_val:
                acc_dict[from_acc] = 0
                acc_dict[to_acc] += avail_val
                debt_dict.setdefault(from_acc, []).append((to_acc, amt - avail_val))
            else:
                acc_dict[from_acc] -= amt
                acc_dict[to_acc] += amt

            # Settle all possible debts after this transaction
            acc_dict, debt_dict = self.settle_all_debts(acc_dict, debt_dict)

        sorted_balances = sorted(acc_dict.values(), reverse=True)
        return sum(sorted_balances[:3])

manager = AccountManager(acc_dict, transac_list)
print("Part 1:", manager.complete_transactions(False))
print("Part 2:", manager.complete_transactions(True))
print("Part 3:", manager.balance_books())

