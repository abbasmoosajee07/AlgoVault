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
        # self.memory: list = [0] * self.MODULUS
        # self.memory[:len(self.program)] = self.program
        self.memory = {i: v for i, v in enumerate(self.program)}

        self.op_log = []

        self.opcode_map = {
            0:  self.__terminate,
            1:  lambda: self.__set(3),
            2:  lambda: self.__push(2),
            3:  lambda: self.__pop(2),
            4:  lambda: self.__equal_to(4),
            5:  lambda: self.__greater(4),
            6:  lambda: self.__jump(2),
            7:  lambda: self.__jump_to(3),
            8:  lambda: self.__jump_if(3),
            9:  lambda: self.__arithmetic(4, "add"),
            10: lambda: self.__arithmetic(4, "mul"),
            11: lambda: self.__arithmetic(4, "mod"),
            12: lambda: self.__and_or(4, "and"),
            13: lambda: self.__and_or(4, " or"),
            21: lambda: self.__noop(1)
        }

    def __name(self, args_reqd):
        """Func"""
        a = self.__get_args(args_reqd)
        info = f"[{self.pointer:05}: NAME] "
        self.op_log.append(info)
        self.pointer += args_reqd


    def check_num(self, val):
        """Validate number"""
        if 0 <= val <= 32767:
            sel_val = val
        elif 32768 <= val <= 32775:
            sel_val = self.__mod_math(val)
        elif 32776 <= val <= 65535:
            raise ValueError(f"Number {val} is invalid.")
        return sel_val

    def __mod_math(self, val):
        """Calculate modular for the number"""
        return val % self.MODULUS

    def __get_args(self, total_args: int):
        """Retrieve a list of arguments from memory starting from the current pointer position."""
        args_list = []
        for arg_no in range(1, total_args):
            args = self.memory.get(self.pointer + arg_no, 0)
            sel_args = self.check_num(args)
            args_list.append(sel_args)
        return args_list

    def __set(self, args_reqd):
        """Set register `a` to the value of `b`."""
        a, b = self.__get_args(args_reqd)
        self.registers[a] = b
        info = f"[{self.pointer:05}: SET] reg[{a}] = {b}"
        self.op_log.append(info)
        self.pointer += args_reqd

    def __push(self, args_reqd):
        """Push `a` onto the stack."""
        a = self.__get_args(args_reqd)[0]
        self.output_stack.append(a)
        info = f"[{self.pointer:05}: PSH] Pushed Value({a}) onto stack"
        self.op_log.append(info)
        self.pointer += args_reqd

    def __pop(self, args_reqd):
        """Pop from the stack into register `a`. Raises error if empty."""
        a = self.__mod_math(self.__get_args(args_reqd)[0])
        pop_val = self.output_stack.pop(0)
        self.registers[a] = pop_val
        info = f"[{self.pointer:05}: POP] Pop {pop_val} from stack onto reg[{a}]"
        self.op_log.append(info)
        self.pointer += args_reqd

    def __equal_to(self, args_reqd):
        """Set `a` to 1 if `b == c`, else 0."""
        a, b, c = self.__get_args(args_reqd)
        value = int(b == c)
        self.registers[a] = value
        condition = "==" if value else "!="
        info = f"[{self.pointer:05}: EQL] reg[{a}] = {value} (cond: {b} {condition} {c})"
        self.op_log.append(info)
        self.pointer += args_reqd

    def __greater(self, args_reqd):
        """Set `a` to 1 if `b > c`, else 0."""
        a, b, c = self.__get_args(args_reqd)
        value = int(b > c)
        self.registers[a] = value
        condition = ">" if value else "<="
        info = f"[{self.pointer:05}: GRT] reg[{a}] = {value} (cond: {b} {condition} {c})"
        self.op_log.append(info)
        self.pointer += args_reqd

    def __jump(self, args_reqd):
        """Jump to address `a`."""
        a, = self.__get_args(args_reqd)
        info = f"[{self.pointer:05}: JMP] Jump pointer to {a:05}"
        self.op_log.append(info)
        self.pointer = a

    def __jump_to(self, args_reqd):
        """Jump to `b` if `a` != 0, else proceed."""
        a, b = self.__get_args(args_reqd)
        jump = b if a != 0 else self.pointer + args_reqd
        condition = "!=" if a != 0 else "=="
        info = f"[{self.pointer:05}: JTO] Jump pointer to {jump:05} (cond: {a} {condition} 0)"
        self.op_log.append(info)
        self.pointer = jump

    def __jump_if(self, args_reqd):
        """Jump to `b` if `a` == 0, else proceed."""
        a, b = self.__get_args(args_reqd)
        jump = b if a == 0 else self.pointer + args_reqd
        condition = "==" if a == 0 else "!="
        info = f"[{self.pointer:05}: JIF] Jump pointer to {jump:05} (cond: {a} {condition} 0)"
        self.op_log.append(info)
        self.pointer = jump

    def __arithmetic(self, args_reqd, operation):
        """Aritmethic Operation: `add`, `mul`, and `mod`"""
        op_sign = {'add':'+', 'mul':'x', 'mod':'%'}[operation]
        a, b, c = self.__get_args(args_reqd)
        if operation == "add":
            value = self.__mod_math(b + c)
        elif operation == "mul":
            value = self.__mod_math(b * c)
        elif operation == "mod":
            value = (b % c)
        self.registers[a] = value
        info = f"[{self.pointer:05}: {operation.upper()}] reg[{a}] = {value} (eq: {b} {op_sign} {c})"
        self.op_log.append(info)
        self.pointer += args_reqd

    def __and_or(self, args_reqd, op_type):
        """Bitwise `and`|`or` operations for values `b` and `c`"""
        op_sign = {'and':'&', ' or':'|'}[op_type]
        a, b, c = self.__get_args(args_reqd)
        if op_type == "and":
            value = b & c
        elif op_type == " or":
            value = b | c
        self.registers[a] = value
        info = f"[{self.pointer:05}: {op_type.upper()}] reg[{a}] = {value} (bit_op: {b} {op_sign} {c}) "
        self.op_log.append(info)
        self.pointer += args_reqd

    def __noop(self, args_reqd):
        """No Operation"""
        info = f"[{self.pointer:05}: NOP] No Operation Performed"
        self.op_log.append(info)
        self.pointer += args_reqd

    def __terminate(self):
        """ Stop Execution and Terminate the program. """
        self.running = False
        info = f"[{self.pointer:05}: HALT] __PROGRAM TERMINATED__"
        self.op_log.append(info)

    def run_computer(self):
        self.program = [
            1, 32768, 123,           # 1: set reg0 = 123
            2, 32768,                # 2: push reg0
            3, 32769,                # 3: pop reg1
            4, 32770, 32768, 32769,  # 4: eq reg2 = (reg0 == reg1)
            5, 32771, 32768, 32769,  # 5: gt reg3 = (reg0 > reg1)
            6, 17,                   # 6: jmp to instruction index 17 (skips jt/jf)
            # 7, 32771, 9999,          # 7: jt reg3 (0), should not jump
            # 8, 32770, 9999,          # 8: jf reg2 (1), should not jump
            9, 32772, 32768, 32769,  # 9: add reg4 = reg0 + reg1
            10, 32773, 32772, 2,     # 10: mult reg5 = reg4 * 2
            11, 32774, 32773, 3,     # 11: mod reg6 = reg5 % 3
            12, 32775, 32773, 255,   # 12: and reg7 = reg5 & 255
            13, 32768, 32774, 256,   # 13: or reg0 = reg6 | 256
            # 14, 32769, 32768,        # 14: not reg1 = ~reg0
            # 15, 32770, 50,           # 15: rmem reg2 = mem[50]
            # 16, 50, 42,              # 16: wmem mem[50] = 42
            # 17, 36,                  # 17: call jump to 36
            # 18,                      # 18: ret (returns to 36+1 = 37)
            # 19, 65,                  # 19: out 'A' (ASCII 65)
            # 20, 32775,               # 20: in → reg7
            21,                      # 21: noop
            0                        # 0: halt
        ]
        self.memory = {i: v for i, v in enumerate(self.program)}
        print(self.memory)

        while self.running and not self.paused:
            opcode = self.memory[self.pointer]
            opcode = self.check_num(opcode)

            if opcode not in self.opcode_map:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")

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

# from Intcode_Computer import Intcode_CPU
# intcode_prog = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
# cpu = Intcode_CPU(intcode_prog, init_inputs=[2], debug=True).process_program()


print(f"Execution Time = {time.time() - start_time:.5f}s")

