import copy

class VirtualMachine:
    MODULUS = 32768

    def __init__(self, program_bytes: bytes, debug: bool = False):
        """
        Initialize the Virtual Machine.
        """
        # Create an initial copy of the bytes program
        self.program_bytes = copy.deepcopy(program_bytes)

        # Flags for execution state
        self.paused: bool = False    # Indicates if the program is paused (e.g., waiting for input)
        self.running: bool = True    # Indicates if the program is still running (not halted)

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
        self.memory[:len(self.program)] = self.program

        # Log of all operations performed by the computer
        self.op_log = []

        self.input_terminal = []
        self.output_terminal = [""]

        self.opcode_map = {
            0:  self.__terminate,
            1:  lambda: self.__set(2),
            2:  lambda: self.__push(1),
            3:  lambda: self.__pop(1),
            4:  lambda: self.__equal_to(3),
            5:  lambda: self.__greater(3),
            6:  lambda: self.__jump(1),
            7:  lambda: self.__jump_to(2),
            8:  lambda: self.__jump_if(2),
            9:  lambda: self.__arithmetic(3, "add"),
            10: lambda: self.__arithmetic(3, "mul"),
            11: lambda: self.__arithmetic(3, "mod"),
            12: lambda: self.__and_or(3, "and"),
            13: lambda: self.__and_or(3, " or"),
            14: lambda: self.__not(2),
            15: lambda: self.__rmem(2),
            16: lambda: self.__wmem(2),
            17: lambda: self.__call(1),
            18: lambda: self.__ret(0),
            19: lambda: self.__out(1),
            20: lambda: self.__input(1),
            21: self.__noop
        }

    def get_num(self, val):
        """Validate number"""
        if 0 <= val <= 32767:
            sel_val = val
        elif 32768 <= val <= 32775:
            sel_val = self.__mod_math(val)
            # print(val, sel_val, self.registers[sel_val])
        elif 32776 <= val <= 65535:
            raise ValueError(f"Number {val} is invalid.")
        return sel_val

    def __mod_math(self, val):
        """Calculate modular for the number"""
        return val % self.MODULUS

    def __get_args(self, total_args: int, corrected: bool = True):
        """Retrieve a list of arguments from memory starting from the current pointer position."""
        args_list = []
        for arg_no in range(1, total_args + 1):
            args = self.memory[self.pointer + arg_no]
            sel_args = self.get_num(args) if corrected else args
            args_list.append(sel_args)
        return args_list[:]

    def __set(self, args_reqd):
        """Set register `a` to the value of `b`."""
        a, b = self.__get_args(args_reqd)
        self.registers[a] = b
        info = f"[{self.pointer:05}: SET] reg[{a}] = {b}"
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def __push(self, args_reqd):
        """Push `a` onto the stack."""
        a = self.__get_args(args_reqd)[0]
        self.output_stack.append(a)
        info = f"[{self.pointer:05}: PSH] Pushed Value({a}) onto stack"
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def __pop(self, args_reqd):
        """Pop from the stack into register `a`. Raises error if empty."""
        a = self.__mod_math(self.__get_args(args_reqd)[0])
        pop_val = self.output_stack.pop(0)
        self.registers[a] = pop_val
        info = f"[{self.pointer:05}: POP] Pop {pop_val} from stack onto reg[{a}]"
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def __equal_to(self, args_reqd):
        """Set `a` to 1 if `b == c`, else 0."""
        a, b, c = self.__get_args(args_reqd)
        value = int(b == c)
        self.registers[a] = value
        condition = "==" if value else "!="
        info = f"[{self.pointer:05}: EQL] reg[{a}] = {value} (cond: {b} {condition} {c})"
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def __greater(self, args_reqd):
        """Set `a` to 1 if `b > c`, else 0."""
        a, b, c = self.__get_args(args_reqd)
        value = int(b > c)
        self.registers[a] = value
        condition = ">" if value else "<="
        info = f"[{self.pointer:05}: GRT] reg[{a}] = {value} (cond: {b} {condition} {c})"
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def set_ip(self, value, push_return_address=False):
        if push_return_address:
            self.stack.append(self.ip+2)
        self.ip = value
        lambda a: self.set_ip((a)-2),                                 # jmp
        lambda a, b: self.set_ip((b)-3 if (a) != 0 else self.ip),     # jt
        lambda a, b: self.set_ip((b)-3 if (a) == 0 else self.ip),     # jf

    def __jump(self, args_reqd):
        """Jump to address `a`."""
        a, = self.__get_args(args_reqd)
        info = f"[{self.pointer:05}: JMP] Jump pointer to {a:05}"
        self.op_log.append(info)
        self.pointer = a

    def get(self, n):
        return n if n < self.MODULUS else self.registers[n-self.MODULUS]

    def __jump_to(self, args_reqd):
        """Jump to `b` if `a` != 0, else proceed."""
        a_raw, b_raw = self.__get_args(args_reqd, False)
        # a_val = self.registers[self.get_num(a_raw)]
        a_val = self.get(a_raw)
        b_val = self.get(b_raw)
        if a_val != 0:
            jump = b_val  # jump target is absolute
            condition = "!="
        else:
            jump = self.pointer + args_reqd + 1  # skip over instruction + args
            condition = "=="

        info = f"[{self.pointer:05}: JTO] Jump pointer to {jump:05} (cond: {a_val} {condition} 0)"
        self.op_log.append(info)
        self.pointer = jump

    def __jump_if(self, args_reqd):
        """Jump to `b` if `a` == 0, else proceed."""
        a, b = self.__get_args(args_reqd)
        jump = b if a == 0 else (self.pointer + args_reqd +1)
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
        self.pointer += args_reqd + 1

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
        self.pointer += args_reqd + 1

    def __not(self, args_reqd):
        """Stores 15-bit bitwise inverse of `b` in `a`"""
        a, b = self.__get_args(args_reqd)
        inv_bits = (~b) & (self.MODULUS - 1)       # Invert and mask to 15 bits
        self.registers[a] = inv_bits
        info = f"[{self.pointer:05}: NOT] reg[{a}] = {inv_bits} (15 bit inverse of {b} stored)"
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def __rmem(self, args_reqd):
        """Read Memory at address `b` and write it `a`"""
        a, b = self.__get_args(args_reqd)
        self.registers[a] = self.memory[b]
        info = f"[{self.pointer:05}: RME] reg[{a}] = {self.memory[b]}"
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def __wmem(self, args_reqd):
        """Write value from `b` into memory address at `a`"""
        a, b = self.__get_args(args_reqd)
        self.memory[a] = b
        info = f"[{self.pointer:05}: WME] Write to memory at a({a}) with value {b}"
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def __call(self, args_reqd):
        """Write the address of the next instruction
            to the stack and jump to `a`"""
        a = self.__get_args(args_reqd)
        info = f"[{self.pointer:05}: CAL] "
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def __ret(self, args_reqd):
        """Remove the top element from the stack and jump to it; empty stack = halt"""
        info = f"[{self.pointer:05}: RET] "
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def __out(self, args_reqd):
        """Write the character represented by ascii code `a` to the terminal"""
        a,  = self.__get_args(args_reqd)
        char_a = chr(a)
        self.output_terminal[-1] += char_a
        info = f"[{self.pointer:05}: OUT] {repr(char_a)} goes to output terminal"
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def __input(self, args_reqd):
        """Read a character from the terminal and write its ascii code to `a`"""
        a,  = self.__get_args(args_reqd)
        input_char = self.input_terminal.pop(0)
        input_ascii = ord(input_char)
        self.registers[a] = input_ascii
        info = f"[{self.pointer:05}: INP] reg[{a}] = {input_ascii} ({input_char} -> {input_ascii})"
        self.op_log.append(info)
        self.pointer += args_reqd + 1

    def __noop(self):
        """No Operation"""
        info = f"[{self.pointer:05}: NOP] No Operation Performed"
        self.op_log.append(info)
        self.pointer += 1

    def __terminate(self):
        """ Stop Execution and Terminate the program. """
        self.running = False
        info = f"[{self.pointer:05}: HALT] __PROGRAM TERMINATED__"
        self.op_log.append(info)

    def run_computer(self, input_commands = []):
        self.input_terminal = input_commands[:]

        while self.running and not self.paused:
            opcode = self.memory[self.pointer]

            if opcode not in self.opcode_map:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")

            self.opcode_map[opcode]()  # Execute the corresponding operation
            if self.debug:
                print(self.op_log[-1])
        print(self.output_terminal[-1])
        return