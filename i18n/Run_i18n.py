# Challenge - 2025
# # Solved in {2025}
# Puzzle Link: https://i18n-puzzles.com/
# Solution by: [Abbas Moosajee]
# Brief: [Run all i18n scripts]

#!/usr/bin/env python3

from pathlib import Path
from challenge_utils import ChallengeBenchmarks

if __name__ == "__main__":

    base_dir = Path.cwd() / str("i18n")
    script_dir = Path(__file__).parent.resolve()
    selected_dir = base_dir
    config_file = "i18n_challenge.json"
    PROBLEMS_TO_RUN = list(range(1, 21))  # Problems 1-25

    analyzer = ChallengeBenchmarks(
        base_dir = selected_dir,
        config_file = config_file,
    )

    results = analyzer.analyze(
        problems_to_run= PROBLEMS_TO_RUN,  # Problems 1-25
        iterations=3,
        save_results=True,
        custom_dir= script_dir / "analysis"
    )

    print("\nAnalysis complete!")
    print(results.head(21))