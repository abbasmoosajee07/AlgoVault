import copy

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

        # {21: 0, 19: 1, 6: 1, 7: 2, 8: 2, 1: 2, 9: 3, 4: 3, 2: 1, 3: 1, 5: 3, 12: 3, 13: 3, 14: 2, 17: 1, 10: 3, 11: 3, 15: 2, 16: 2, 18: 0, 20: 1}
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
            21: self.__noop
        }

    def __name(self, args_reqd):
        """Func"""
        a = self.__get_args(args_reqd)
        info = f"[{self.pointer:05}: NAME] "
        self.op_log.append(info)
        self.pointer += args_reqd + 1
        def get(n):
            return n if n < self.MODULUS else self.registers[n-self.MODULUS]
        def set_register(register, value):
            self.registers[register-self.MODULUS] = value
        def set_memory(address, value):
            self.memory[address] = value
        def set_ip(value, push_return_address=False):
            if push_return_address:
                self.stack.append(self.ip+2)
            self.ip = value

    def get_num(self, val):
        """Validate number"""
        if 0 <= val <= 32767:
            sel_val = val
        elif 32768 <= val <= 32775:
            sel_val = self.registers[self.__mod_math(val)]
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
        for arg_no in range(1, total_args + 1):
            args = self.memory.get(self.pointer + arg_no, 0)
            args = self.pointer + arg_no
            sel_args = self.get_num(args)
            args_list.append(sel_args)
        return args_list

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
        inv_bits = (~b) & 0x7FFF       # Invert and mask to 15 bits
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


        while self.running and not self.paused:
            opcode = self.memory[self.pointer]
            opcode = self.get_num(opcode)

            if opcode not in self.opcode_map:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")

            self.opcode_map[opcode]()  # Execute the corresponding operation
            if self.debug:
                print(self.op_log[-1])
        # print(self.registers)
        return