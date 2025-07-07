"""Synacor Challenge
Solution Started: Jul 1, 2025
Solution by: Abbas Moosajee
Brief: [Synacor virtual Machine]
"""

import os, copy, time
from VirtualMachine import VirtualMachine
start_time = time.time()


# Load the input data from the specified file path
program_file = "challenge.bin"
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), program_file)
vm_program = open(file_path, "rb").read()

vm = VirtualMachine(vm_program)
out = vm.run_computer(["A"])
# echo -n "Test" | md5sum

print(out[-1])
# vm.save_log()

print(f"Execution Time = {time.time() - start_time:.5f}s")

