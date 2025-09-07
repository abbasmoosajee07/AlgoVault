from pathlib import Path
from challenge_utils import ScriptBuilder

# Constants
PROBLEM_NO = 2
CHALLENGE = "aquaq"
CHOSEN_LANGUAGE = "rust"

AUTHOR = "Abbas Moosajee"

CONFIG_DICT = {
    "MNG": ("MNG", "MNG_challenge.json"),
    "aquaq": ("AquaQ", "AquaQ_challenge.json"),
}

def main() -> None:
    """Main function to create challenge files."""

    repo_dir = Path(__file__).parent
    folder, config_file = CONFIG_DICT[CHALLENGE]
    challenge_dir = repo_dir / folder

    try:
        builder = ScriptBuilder(AUTHOR, challenge_dir, config_file)

        filepath = builder.create_files(
            prob_no=PROBLEM_NO,
            language=CHOSEN_LANGUAGE,
            txt_files=1,
        )

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()