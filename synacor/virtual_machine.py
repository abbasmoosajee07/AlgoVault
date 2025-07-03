"""Synacor Challenge
Solution Started: Jul 1, 2025
Solution by: Abbas Moosajee
Brief: [Synacor virtual Machine]
"""

import os, copy, time
from VirtualMachine import VirtualMachine
start_time = time.time()

class VirtualMachine:
    MODULUS = 32768

    def __init__(self, program_bytes: bytes, debug: bool = False):
        """
        Initialize the Virtual Machine
        """
        # Create an initial copy of the bytes program
        self.program_bytes = copy.deepcopy(program_bytes)

        # Flags for execution state
        self.paused = False    # Indicates if the program is paused (e.g., waiting for input)
        self.running = True    # Indicates if the program is still running (not halted)

        # Debugging mode flag
        self.debug: bool = debug     # If True, additional debug information can be printed/logged

        # Pointer
        self.pointer: int = 0

        # Convert binary program to list of integers
        self.program: list[int] = [
            (high << 8) | low
            for low, high in zip(program_bytes[::2], program_bytes[1::2])
        ]

        # Registers
        self.registers: dict = {
            reg_no: 0 for reg_no in range(8)
        }

        # Unbounded stack
        self.output_stack: list = []

        # Memory: 15-bit address space 32K words of 16-bit values
        self.memory: list = [0] * self.MODULUS
        # self.memory[:len(self.program)] = self.program

        self.op_log = []

        self.opcode_map = {
            0: self.__terminate,
            1: lambda: self.__set(2),
            2: lambda: self.__push(1),
            3: lambda: self.__pop(1),
            4: lambda: self.__equal_to(3),
            5: lambda: self.__greater_than(5),
        }

    def __name(self, args_reqd):
        """
        Func
        """
        a = self.__get_args(args_reqd)

        info = f"[{self.pointer:07}: EQTO] "
        self.op_log.append(info)

        self.pointer += args_reqd

    def __mod_math(self, val):
        return val % self.MODULUS

    def __get_args(self, total_args: int):
        """
        Retrieve a list of arguments from memory starting from the current pointer position.
        """
        args_list = []
        for arg_no in range(1, total_args):
            args = self.memory.get(self.pointer + arg_no, 0)
            args_list.append(args)
        return args_list

    def __set(self, args_reqd):
        """
        Set register `a` to the value of `b`
        """
        a, b = self.__get_args(args_reqd)
        self.registers[a] = b

        info = f"[{self.pointer:07}:  SET] Set register {a} to {b}"
        self.op_log.append(info)

        self.pointer += args_reqd

    def __push(self, args_reqd):
        """
        Push `a` onto the stack
        """
        a = self.__get_args(args_reqd)[0]
        self.output_stack.append(a)

        info = f"[{self.pointer:07}: PUSH] Add {a} to value to stack"
        self.op_log.append(info)

        self.pointer += args_reqd

    def __pop(self, args_reqd):
        """
        Remove the top element from the stack and write it into `a`;
        empty stack = error
        """
        a = self.__mod_math(self.__get_args(args_reqd)[0])
        pop_val = self.output_stack.pop(0)
        self.registers[a] = pop_val

        info = f"[{self.pointer:07}:  POP] Set register {a} to {pop_val}"
        self.op_log.append(info)

        self.pointer += args_reqd

    def __equal_to(self, args_reqd):
        """
        Set `a` to 1 if `b` is equal to `c`; set it to 0 otherwise
        """
        a, b, c = self.__get_args(args_reqd)
        value = 1 if b == c else 0
        self.registers[a] = value

        condition = "==" if value == 1 else "!="
        info = f"[{self.pointer:07}: EQTO] Set register {a} to {value} as {b} {condition} {c}"
        self.op_log.append(info)
        if self.debug:
            print(info)

        self.pointer += args_reqd

    def __greater_than(self, args_reqd):
        """
        Set `a` to 1 if `b` is greater than `c`; set it to 0 otherwise
        """
        a, b, c = self.__get_args(args_reqd)
        value = 1 if b > c else 0
        self.registers[a] = value

        condition = ">" if value == 1 else "<"
        info = f"[{self.pointer:07}:GREAT] Set register {a} to {value} as {b} {condition} {c}"
        self.op_log.append(info)

        self.pointer += args_reqd

    def __terminate(self):
        """
        Stop Execution and Terminate the program.
        """
        self.running = False

        info = f"[{self.pointer:07}: STOP] Program stopped"
        self.op_log.append(info)

    def run_computer(self):

        while self.running and not self.paused:
            instruction = self.memory[self.pointer]
            opcode = instruction % 100
            # self.modes = [(instruction // 10 ** i) % 10 for i in range(2, 5)]  # Parse parameter modes

            # if opcode not in self.opcode_map:
            #     raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")

            self.opcode_map[opcode]()  # Execute the corresponding operation
            if self.debug:
                print(self.op_log[-1])


        return

# Load the input data from the specified file path
program_file = "challenge.bin"
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), program_file)
vm_program = open(file_path, "rb").read()

vm = VirtualMachine(vm_program, True)
vm.run_computer()

print(f"Execution Time = {time.time() - start_time:.5f}s")

