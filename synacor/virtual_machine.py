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

# echo -n "Test" | md5sum
vm = VirtualMachine(vm_program)
out = vm.run_computer(["A"])
script_dir = os.path.dirname(os.path.abspath(__file__))

print(out[-1])
vm1 = vm.replicate()
vm1.save_log(file_loc=script_dir)

print(f"Execution Time = {time.time() - start_time:.5f}s")

