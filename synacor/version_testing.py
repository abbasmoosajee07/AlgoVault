# %% [markdown]
# # Synacor Challenge
# **Author**: Abbas Moosajee
# Testing Solutions with different Challenge versions

import os, re, time, copy, gc
import sys, importlib
import pandas as pd
from tabulate import tabulate

# %% [markdown]
# This reset_and_reload of the console has by far been one of the most baffling problems I have come across,
# and while I am not completely sure why it occured, so far I have debugged it to be some from a memory remaining
# over from previous iterations of the code. I suspect it may be due to the multiple iterations it goes through
# during the first bfs exploration, but alas I am not certain.
#
# Having tried various approacches to cleaning the memory, from pre_loading all consoles to shutting it down by
# erasing all its memory, the only solution I found to work was essentially reloading the whole memory again.

def reset_and_reload_console(module_name, class_name):
    """
    Completely resets and reloads a console class from a module.

    Args:
        module_name (str): Name of the module containing the class
        class_name (str): Name of the class to reload

    Returns:
        The freshly reloaded class
    """
    # 1. Clear existing references
    for module in list(sys.modules.values()):
        if hasattr(module, '__dict__'):
            module.__dict__.pop(class_name, None)  # Clear class reference
            module.__dict__.pop(module_name, None)  # Clear module reference

    # 2. Force Python to forget the module completely
    sys.modules.pop(module_name, None)

    # 3. Dynamic import using importlib
    module = importlib.import_module(module_name)
    importlib.reload(module)

    # 4. Get the class dynamically
    console_class = getattr(module, class_name)
    return console_class

def test_challenge_version(version_no):
    """Test a specific version of the Synacor challenge solution.
    Args:
        version_no (int/str): Version number to test
    """
    version_dict = {
        0: "LDOb7UGhTi",   1: "UpiNqTKzQPcV", 2: "fNCoeXxLEawt",
        3: "SIyXxPoysNHd", 4: "fbCcIPhFoGGd", 5: "zmBcfmVUfShk",
        6: "wDoVYBGtiHiP", 7: "GXOfgPQxcRix",
    }
    try:
        spec_code = version_dict[version_no]

        # 1. Load program data
        version_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "different_versions", f"v{version_no}")
        program_path = os.path.join(version_dir, "challenge.bin")

        with open(program_path, "rb") as f:
            program_data = f.read()

        # 2. Get fresh console class
        SynacorConsole = reset_and_reload_console(
            module_name="SynacorConsole", class_name="SynacorConsole"
        )

        # 3. Run test
        init_time = time.time()
        # print(f"\nTesting Version {version_no}")
        console = SynacorConsole(
            copy.deepcopy(program_data),
            spec_code, visualize=False
        )

        _, bfs_time = console.auto_play(reset_deque=True)
        final_time = f"{time.time() - init_time:.5f}s"
        # test = console.benchmark_solution()
        run_props = [final_time]
        for code_data in bfs_time.values():
            run_props.append(code_data[1])
        return run_props

    except KeyError:
        print(f"Error: Version {version_no} not found in version_dict")
    except FileNotFoundError:
        print(f"Error: Program file not found for version {version_no}")
    except Exception as e:
        print(f"Error testing version {version_no}: {str(e)}")

# Create data as a dictionary
df_rows = {
    'Challenge Code': ['Time(s)', 'Spec(1)', 'Running VM(2)', 'Self Test(3)', 'Use Tablet(4)',
        'Lit Lantern(5)', 'Teleport_v1(6)', 'Teleport_v2(7)', 'Mirrored(8)'],
}

# Create the DataFrame
version_df = pd.DataFrame(df_rows)

# Run solution on all versions
for ver_no in range(0, 7 + 1):
    version_test = test_challenge_version(ver_no)
    version_df[f"Version {ver_no}"] = version_test


# Prepare the formatted table string
table_string = tabulate(version_df, headers='keys', tablefmt='grid')

# Write it to a text file
with open("version_table.txt", "w", encoding="utf-8") as f:
    f.write(table_string)
