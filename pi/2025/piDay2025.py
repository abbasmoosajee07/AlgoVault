"""piDay Puzzles - 2025
Solution Started: Apr 6, 2025
Puzzle Link: https://ivanr3d.com/projects/pi/2025.html
Solution by: Abbas Moosajee
Brief: []
"""

#!/usr/bin/env python3

import os, re, copy, time, string
import pandas as pd

start_time = time.time()


# Load the input data from the specified file path
D2025_file = "Day2025_input.txt"
D2025_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D2025_file)

# Read and sort input data into a grid
with open(D2025_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    market_data = input_data[0].split('\n')
    cipher_text = input_data[1].split('\n')
    test_data = ['Day          Price($)          Ticker', '1            0.3                GST', '2            3.75               JVW', '3            2.64               SPI', '4            7.77               LCK', '5            1.6                HST', '6            1.8                NUM', '7            5.88               XIJ']

class piGhost:
    def __init__(self, market_data: list[str], cipher_data: list[str]):
        self.pi_key = "314159265358979323846264338327950288419716939937510"
        self.parse_data(market_data)
        self.cipher_grid = [i for line in cipher_data for i in line.split()]
        self.letter_list = list(string.ascii_uppercase)

    def parse_data(self, market_data: list[str]):
        rows = []
        ticker_dict = {}
        # Loop over the data and extract the relevant information
        for line in market_data[1:]:
            day, price, ticker = line.split(maxsplit=2)
            rows.append({"Day": int(day), "Price": float(price), "Ticker": ticker})
            ticker_dict[ticker]  = (int(day), price)
        self.market_df = pd.DataFrame(rows)
        self.ticker_dict = ticker_dict

    def find_secret_code(self):
        market_df = self.market_df.copy()
        data_key = self.pi_key[:32]  # First 32 digits of Pi
        manipulated_rows = []

        # Step 1: Identify manipulated rows
        for _, row in market_df.iterrows():
            price_str = str(row['Price']).replace('.', '')
            if price_str in data_key:
                manipulated_rows.append({"Day": row['Day'], "Price": row['Price'], "Ticker": row['Ticker']})

        # Step 2: Sort manipulated data by 'Day'
        manipulated_data = pd.DataFrame(manipulated_rows)
        sorted_df = manipulated_data.sort_values(by="Day", ascending=True)
        self.manipulated_data = sorted_df

        # Step 3: Initialize the base price from the first manipulated day
        base_price = sorted_df.iloc[0]['Price']

        # Step 4: Apply operations based on even/odd day numbers
        for _, row in sorted_df.iloc[1:].iterrows():  # Skip the first row as it's already used
            if row['Day'] % 2 == 0:  # If day is even, multiply
                base_price *= row['Price']
            else:  # If day is odd, divide
                base_price /= row['Price']

        # Step 5: Return the base price after removing non-numeric characters
        return str(base_price).replace('.', '')  # Only return numeric characters (no decimals)

    def find_secret_phase(self):
        phrase = []

        for _, row in self.manipulated_data.iterrows():
            price, ticker = (row['Price'], row['Ticker'])

            # Convert price to int (remove decimal)
            price_int = int(str(price).replace('.', ''))

            # Shift each character in the ticker by price_int
            shifted_ticker = ''.join(
                self.letter_list[(self.letter_list.index(ch) + price_int) % 26]
                for ch in ticker
            )

            # Look up new ticker in dictionary
            other_day, other_price = self.ticker_dict[shifted_ticker]

            # Get letter using other_price from cipher grid
            other_price_int = int(str(other_price).replace('.', ''))
            letter = self.cipher_grid[other_price_int % 256]

            phrase.append((other_day, letter))

        # Sort by day and join letters to form the secret phrase
        secret_phrase = ''.join(letter for _, letter in sorted(phrase))
        return secret_phrase


laptop = piGhost(market_data, cipher_text)
secret_code = laptop.find_secret_code()
print("Secret Code:", (secret_code[:10]))

secret_phase = laptop.find_secret_phase()
print("Secret Phrase:", secret_phase)

print(f"Execution Time = {time.time() - start_time:.5f}s")
