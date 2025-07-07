import copy

class VirtualMachine:
    MODULUS = 32768

    def __init__(self, program_bytes: bytes, debug: bool = False):
        """Initialize the Virtual Machine."""
        # Create an initial copy of the bytes program
        self.program_bytes = program_bytes

        # Flags for execution state
        self.paused: bool = False    # Indicates if the program is paused (e.g., waiting for input)
        self.running: bool = True    # Indicates if the program is still running (not halted)

        # Debugging mode flag
        self.debug: bool = debug     # If True, additional debug information can be printed/logged

        self.pointer: int = 0        # Pointer

        # Convert binary program to list of integers
        self.program: list[int] = [
            (high << 8) | low
            for low, high in zip(program_bytes[::2], program_bytes[1::2])
        ]

        # Registers
        self.registers: dict = {reg_no: 0 for reg_no in range(8)}

        # Unbounded stack
        self.output_stack: list = []

        # Memory: 15-bit address space 32K words of 16-bit values
        self.memory: list = [0] * self.MODULUS
        self.memory[:len(self.program)] = self.program

        # Log of all operations performed by the computer
        self.op_log = []

        self.input_terminal  = []
        self.output_terminal = [""]

        self.opcode_map = {
            0:  (self.__terminate, 0),
            1:  (self.__set,  2),
            2:  (self.__push, 1),
            3:  (self.__pop,  1),
            4:  (self.__equal_to, 3),
            5:  (self.__greater,  3),
            6:  (self.__jump,     1),
            7:  (self.__jump_to,  2),
            8:  (self.__jump_if,  2),
            9:  (self.__arithmetic, (3, "add")),
            10: (self.__arithmetic, (3, "mul")),
            11: (self.__arithmetic, (3, "mod")),
            12: (self.__and_or,     (3, "and")),
            13: (self.__and_or,     (3, " or")),
            14: (self.__not,   2),
            15: (self.__rmem,  2),
            16: (self.__wmem,  2),
            17: (self.__call,  1),
            18: (self.__ret,   0),
            19: (self.__out,   1),
            20: (self.__input, 1),
            21: (self.__noop,  0)
        }

    def resolve(self, val):
        if 0 <= val <= 32767:
            return val
        elif 32768 <= val <= 32775:
            return self.registers[val - self.MODULUS]
        else:
            raise ValueError(f"Invalid operand: {val}")

    def get_raw(self, val):
        if 32768 <= val <= 32775:
            return val - self.MODULUS
        raise ValueError(f"Expected register (32768-32775), got {val}")

    def __get_args(self, total_args: int):
        """Retrieve a list of arguments from memory starting from the current pointer position."""
        return self.memory[self.pointer + 1 : self.pointer + 1 + total_args]

    def set_registers(self, addr, val):
        """Set register[`addr`] to desired `value`"""
        self.registers[addr] = val

    def __set(self, args_count):
        """Set register `a` to the value of `b`."""
        a_raw, b_raw = self.__get_args(args_count)
        a, b = self.get_raw(a_raw), self.resolve(b_raw)
        self.set_registers(a, b)
        self.op_log.append(f"[{self.pointer:05}: SET] reg[{a}] = {b}")
        return args_count

    def __push(self, args_count):
        """Push `a` onto the stack."""
        a_raw, = self.__get_args(args_count)
        a = self.resolve(a_raw)
        self.output_stack.append(a)
        self.op_log.append(f"[{self.pointer:05}: PSH] Pushed Value({a}) onto stack {a_raw} {a}")
        return args_count

    def __pop(self, args_count):
        """Pop from the stack into register `a`. Raises error if empty."""
        if not self.output_stack:
            raise RuntimeError("Stack is empty")
        a_raw, = self.__get_args(args_count)
        a = self.get_raw(a_raw)
        pop_val = self.output_stack.pop()
        self.set_registers(a, pop_val)
        self.op_log.append(f"[{self.pointer:05}: POP] Pop {pop_val} from stack onto reg[{a}]")
        return args_count

    def __equal_to(self, args_count):
        """Set `a` to 1 if `b == c`, else 0."""
        a_raw, b_raw, c_raw = self.__get_args(args_count)
        a = self.get_raw(a_raw)
        b, c = [self.resolve(i) for i in (b_raw, c_raw)]
        val = int(b == c)
        condition = "==" if val else "!="
        self.set_registers(a, val)
        self.op_log.append(f"[{self.pointer:05}: EQL] reg[{a}] = {val} (cond: {b} {condition} {c})")
        return args_count

    def __greater(self, args_count):
        """Set `a` to 1 if `b > c`, else 0."""
        a_raw, b_raw, c_raw = self.__get_args(args_count)
        a = self.get_raw(a_raw)
        b, c = [self.resolve(i) for i in (b_raw, c_raw)]
        value = int(b > c)
        self.registers[a] = value
        condition = ">" if value else "<="
        self.op_log.append(f"[{self.pointer:05}: GRT] reg[{a}] = {value} (cond: {b} {condition} {c})")
        return args_count

    def __jump(self, args_count):
        """Jump to address `a`."""
        a_raw, = self.__get_args(args_count)
        a = self.resolve(a_raw)
        self.op_log.append(f"[{self.pointer:05}: JMP] Jump pointer to {a:05}")
        self.pointer = a
        return -1

    def __jump_to(self, args_count):
        """Jump to `b` if `a` != 0, else proceed."""
        raw_args = self.__get_args(args_count)
        a, b = [self.resolve(raw) for raw in raw_args]

        jump = b if (a != 0) else (self.pointer + args_count +1)
        condition = "!=" if a != 0 else "=="
        self.op_log.append(f"[{self.pointer:05}: JNZ] Jump pointer to {jump:05} (cond: {a} {condition} 0)")
        self.pointer = jump
        return -1

    def __jump_if(self, args_count):
        """Jump to `b` if `a` == 0, else proceed."""
        raw_args = self.__get_args(args_count)
        a, b = [self.resolve(raw) for raw in raw_args]

        jump = b if (a == 0) else (self.pointer + args_count +1)
        condition = "==" if (a == 0) else "!="
        self.op_log.append(f"[{self.pointer:05}: JFZ] Jump pointer to {jump:05} (cond: {a} {condition} 0)")
        self.pointer = jump
        return -1

    def __arithmetic(self, func_args):
        """Aritmethic Operation: `add`, `mul`, and `mod`"""
        args_count, op_type = func_args
        op_sign = {'add':'+', 'mul':'x', 'mod':'%'}[op_type]
        a_raw, b_raw, c_raw = self.__get_args(args_count)
        a = self.get_raw(a_raw)
        b, c = [self.resolve(i) for i in (b_raw, c_raw)]
        if op_type == "add":
            value = (b + c) % self.MODULUS
        elif op_type == "mul":
            value = (b * c) % self.MODULUS
        elif op_type == "mod":
            value = (b % c)
        self.set_registers(a, value)
        info = f"[{self.pointer:05}: {op_type.upper()}] reg[{a}] = {value} (eq: {b} {op_sign} {c})"
        self.op_log.append(info)
        return args_count

    def __and_or(self, func_args):
        """Bitwise `and`|`or` operations for values `b` and `c`"""
        args_count, op_type = func_args
        op_sign = {'and':'&', ' or':'|'}[op_type]
        a_raw, b_raw, c_raw = self.__get_args(args_count)
        a = self.get_raw(a_raw)
        b, c = [self.resolve(i) for i in (b_raw, c_raw)]
        if op_type == "and":
            value = b & c
        elif op_type == " or":
            value = b | c
        self.set_registers(a, value)
        self.op_log.append(f"[{self.pointer:05}: {op_type.upper()}] reg[{a}] = {value} (bit_op: {b} {op_sign} {c})")
        return args_count

    def __not(self, args_count):
        """Stores 15-bit bitwise inverse of `b` in `a`"""
        a_raw, b_raw = self.__get_args(args_count)
        a, b = self.get_raw(a_raw), self.resolve(b_raw)
        inv_bits = (~b) & (self.MODULUS - 1)       # Invert and mask to 15 bits
        self.set_registers(a, inv_bits)
        self.op_log.append("[{self.pointer:05}: NOT] reg[{a}] = {inv_bits} (15 bit inverse of {b} stored)")
        return args_count

    def __rmem(self, args_count):
        """Read Memory at address `b` and write it `a`"""
        a_raw, b_raw = self.__get_args(args_count)
        a, b = self.get_raw(a_raw), self.resolve(b_raw)
        value = self.memory[b]
        self.set_registers(a, value)
        self.op_log.append(f"[{self.pointer:05}: RDM] reg[{a}] = {self.memory[b]}")
        return args_count

    def __wmem(self, args_count):
        """Write value from `b` into memory address at `a`"""
        raw_args = self.__get_args(args_count)
        a, b = [self.resolve(raw) for raw in raw_args]

        self.memory[a] = b
        self.op_log.append(f"[{self.pointer:05}: WRM] Write to memory at a({a}) with value {b}")
        return args_count

    def __call(self, args_count):
        """Write the address of the next instruction
            to the stack and jump to `a`"""
        a_raw, = self.__get_args(args_count)
        a = self.resolve(a_raw)
        stack_val = self.pointer + args_count + 1
        self.output_stack.append(stack_val)
        self.op_log.append(f"[{self.pointer:05}: CAL] Call to {a}, return to {stack_val}")
        self.pointer = a
        return -1

    def __ret(self, _):
        """Remove the top element from the stack and jump to it; empty stack = halt"""
        if not self.output_stack:
            self.__terminate()
        ret_addr = self.output_stack.pop()
        self.op_log.append(f"[{self.pointer:05}: RET] Return to {ret_addr}")
        self.pointer = ret_addr
        return -1

    def __out(self, args_count):
        """Write the character represented by ascii code `a` to the terminal"""
        a_raw,  = self.__get_args(args_count)
        a = self.resolve(a_raw)
        char_a = chr(a)
        self.output_terminal[-1] += char_a
        self.op_log.append(f"[{self.pointer:05}: OUT] {a} -> {repr(char_a)} to terminal")
        return args_count

    def __input(self, args_count):
        """Read a character from the terminal and write its ascii code to `a`"""
        if not self.input_terminal:
            self.paused = True
            self.op_log.append(f"[{self.pointer:05}: INP] Empty Input | Pause Computer)")
            return 0
        a_raw,  = self.__get_args(args_count)
        a = self.get_raw(a_raw)
        input_char = self.input_terminal.pop(0)
        input_ascii = ord(input_char)
        self.set_registers(a, input_ascii)
        self.op_log.append(f"[{self.pointer:05}: INP] reg[{a}] = {input_ascii} ({input_char} -> {input_ascii})")
        return args_count

    def __noop(self, _):
        """No Operation"""
        self.op_log.append(f"[{self.pointer:05}: NOP] No Operation Performed")
        return 0

    def __terminate(self, _):
        """ Stop Execution and Terminate the program. """
        self.op_log.append(f"[{self.pointer:05}: HALT] __PROGRAM TERMINATED__")
        self.running = False
        return 0

    def run_computer(self, input_commands = []):

        while self.running and not self.paused:
            opcode = self.memory[self.pointer]

            if opcode not in self.opcode_map:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")

            op_fn, func_args = self.opcode_map[opcode]
            move_ip = op_fn(func_args)
            self.pointer += move_ip + 1

            if self.debug:
                print(self.op_log[-1])
        return self.output_terminal

    def save_log(self, file_name = "vm_log"):
        """Save log to a .txt file"""
        with open(f"{file_name}.txt", "w") as f:
            for item in self.op_log:
                f.write(f"{item}\n")
