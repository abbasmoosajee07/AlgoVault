class VirtualMachine:
    MODULUS = 32768

    def __init__(self, program_bytes: bytes, debug: bool = False):
        """Initialize the Virtual Machine."""
        # Core configuration
        self.pointer = 0                      # Instruction pointer
        self.debug = debug                    # Enables debug logging
        self.paused = False                   # Indicates if execution is paused (waiting for input)
        self.running = True                   # Indicates if the VM is running
        self.version_no = 0
        self.software_patches = None

        # State components
        self.memory = [0] * self.MODULUS      # Memory: 15-bit address space 32K words of 16-bit values
        self.registers    = [0] * 8           # 8 general-purpose registers
        self.output_stack = [ ]               # Unbounded stack for temporary values
        self.output_terminal = [""]           # Output buffer for character writes
        self.input_commands  = []             # Input buffer for keyboard simulation
        self.op_log = []                      # Log of executed operations (used for debugging/tracing)
        self.program_bytes = program_bytes    # Create an initial copy of the bytes program

        self.program = [                      # Convert binary program to list of integers
            (high << 8) | low
            for low, high in zip(program_bytes[::2], program_bytes[1::2])
        ]
        self.memory[:len(self.program)] = self.program

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
            13: (self.__and_or,     (3, "or")),
            14: (self.__not,   2),
            15: (self.__rmem,  2),
            16: (self.__wmem,  2),
            17: (self.__call,  1),
            18: (self.__ret,   0),
            19: (self.__out,   1),
            20: (self.__input, 1),
            21: (self.__noop,  0)
        }

    def __validate_val(self, val):
        if 0 <= val <= 32767:
            return val
        else:
            return self.registers[self.__get_reg_no(val)]

    def __get_reg_no(self, val):
        if 32768 <= val <= 32775:
            return val - self.MODULUS
        raise ValueError(f"Expected register (32768-32775), got {val}")

    def __get_args(self, total_args):
        """Retrieve a list of arguments from memory starting from the current pointer position."""
        return self.memory[self.pointer + 1 : self.pointer + 1 + total_args]

    def __set_registers(self, addr, val):
        """Set register[`addr`] to desired `value`"""
        self.registers[addr] = val

    def __terminate(self, args_count):
        """[00]: Stop Execution and Terminate the program. """
        self.debug_log(f"[{self.pointer:05}: HALT] __PROGRAM TERMINATED__")
        self.running = False
        return args_count

    def __set(self, args_count):
        """[01]: Set register `a` to the value of `b`."""
        a_raw, b_raw = self.__get_args(args_count)
        a, b = self.__get_reg_no(a_raw), self.__validate_val(b_raw)
        self.__set_registers(a, b)
        self.debug_log(f"[{self.pointer:05}: SET] reg[{a}] = {b}")
        return args_count

    def __push(self, args_count):
        """[02]: Push `a` onto the stack."""
        a_raw, = self.__get_args(args_count)
        a = self.__validate_val(a_raw)
        self.output_stack.append(a)
        self.debug_log(f"[{self.pointer:05}: PSH] Pushed Value({a}) onto stack {a_raw} {a}")
        return args_count

    def __pop(self, args_count):
        """[03]: Pop from the stack into register `a`. Raises error if empty."""
        if not self.output_stack:
            raise RuntimeError("Stack is empty")
        a_raw, = self.__get_args(args_count)
        a = self.__get_reg_no(a_raw)
        pop_val = self.output_stack.pop()
        self.__set_registers(a, pop_val)
        self.debug_log(f"[{self.pointer:05}: POP] Pop {pop_val} from stack onto reg[{a}]")
        return args_count

    def __equal_to(self, args_count):
        """[04]: Set `a` to 1 if `b == c`, else 0."""
        a_raw, b_raw, c_raw = self.__get_args(args_count)
        a = self.__get_reg_no(a_raw)
        b, c = [self.__validate_val(i) for i in (b_raw, c_raw)]
        val = int(b == c)
        condition = "==" if val else "!="
        self.__set_registers(a, val)
        self.debug_log(f"[{self.pointer:05}: EQL] reg[{a}] = {val} (cond: {b} {condition} {c})")
        return args_count

    def __greater(self, args_count):
        """[05]: Set `a` to 1 if `b > c`, else 0."""
        a_raw, b_raw, c_raw = self.__get_args(args_count)
        a = self.__get_reg_no(a_raw)
        b, c = [self.__validate_val(i) for i in (b_raw, c_raw)]
        val = int(b > c)
        self.__set_registers(a, val)
        condition = ">" if val else "<="
        self.debug_log(f"[{self.pointer:05}: GRT] reg[{a}] = {val} (cond: {b} {condition} {c})")
        return args_count

    def __jump(self, args_count):
        """[06]: Jump to address `a`."""
        a_raw, = self.__get_args(args_count)
        a = self.__validate_val(a_raw)
        self.debug_log(f"[{self.pointer:05}: JMP] Jump pointer to {a:05}")
        self.pointer = a

    def __jump_to(self, args_count):
        """[07]: Jump to `b` if `a` != 0, else proceed."""
        raw_args = self.__get_args(args_count)
        a, b = [self.__validate_val(raw) for raw in raw_args]
        jump = b if (a != 0) else (self.pointer + args_count +1)
        condition = "!=" if a != 0 else "=="
        self.debug_log(f"[{self.pointer:05}: JNZ] Jump pointer to {jump:05} (cond: {a} {condition} 0)")
        self.pointer = jump

    def __jump_if(self, args_count):
        """[08]: Jump to `b` if `a` == 0, else proceed."""
        raw_args = self.__get_args(args_count)
        a, b = [self.__validate_val(raw) for raw in raw_args]
        jump = b if (a == 0) else (self.pointer + args_count +1)
        condition = "==" if (a == 0) else "!="
        self.debug_log(f"[{self.pointer:05}: JFZ] Jump pointer to {jump:05} (cond: {a} {condition} 0)")
        self.pointer = jump

    def __arithmetic(self, func_args):
        """[09, 10, 11]: Aritmethic Operation `add`, `mul`, and `mod`"""
        args_count, op_type = func_args
        op_sign = {'add':'+', 'mul':'x', 'mod':'%'}[op_type]
        a_raw, b_raw, c_raw = self.__get_args(args_count)
        a = self.__get_reg_no(a_raw)
        b, c = [self.__validate_val(i) for i in (b_raw, c_raw)]
        if op_type == "add":
            val = (b + c) % self.MODULUS
        elif op_type == "mul":
            val = (b * c) % self.MODULUS
        elif op_type == "mod":
            val = (b % c)
        self.__set_registers(a, val)
        info = f"[{self.pointer:05}: {op_type.upper()}] reg[{a}] = {val} (eq: {b} {op_sign} {c})"
        self.debug_log(info)
        return args_count

    def __and_or(self, func_args):
        """[12, 13]: Bitwise `and`|`or` operations for values `b` and `c`"""
        args_count, op_type = func_args
        op_sign = {'and':'&', 'or':'|'}[op_type]
        a_raw, b_raw, c_raw = self.__get_args(args_count)
        a = self.__get_reg_no(a_raw)
        b, c = [self.__validate_val(i) for i in (b_raw, c_raw)]
        if op_type == "and":
            val = b & c
        elif op_type == "or":
            val = b | c
            op_type += " "
        self.__set_registers(a, val)
        self.debug_log(f"[{self.pointer:05}: {op_type.upper()}] reg[{a}] = {val} (bit_op: {b} {op_sign} {c})")
        return args_count

    def __not(self, args_count):
        """[14]: Stores 15-bit bitwise inverse of `b` in `a`"""
        a_raw, b_raw = self.__get_args(args_count)
        a, b = self.__get_reg_no(a_raw), self.__validate_val(b_raw)
        inv_bits = (~b) & (self.MODULUS - 1)       # Invert and mask to 15 bits
        self.__set_registers(a, inv_bits)
        self.debug_log(f"[{self.pointer:05}: NOT] reg[{a}] = {inv_bits} (15 bit inverse of {b} stored)")
        return args_count

    def __rmem(self, args_count):
        """[15]: Read Memory at address `b` and write it `a`"""
        a_raw, b_raw = self.__get_args(args_count)
        a, b = self.__get_reg_no(a_raw), self.__validate_val(b_raw)
        val = self.memory[b]
        self.__set_registers(a, val)
        self.debug_log(f"[{self.pointer:05}: RDM] reg[{a}] = {val}")
        return args_count

    def __wmem(self, args_count):
        """[16]: Write val from `b` into memory address at `a`"""
        raw_args = self.__get_args(args_count)
        a, b = [self.__validate_val(raw) for raw in raw_args]
        self.memory[a] = b
        self.debug_log(f"[{self.pointer:05}: WRM] Write to memory at a({a}) with value {b}")
        return args_count

    def __call(self, args_count):
        """[17]: Write the address of the next instruction to the stack and jump to `a`"""
        a_raw, = self.__get_args(args_count)
        a = self.__validate_val(a_raw)
        stack_val = self.pointer + args_count + 1
        self.output_stack.append(stack_val)
        self.debug_log(f"[{self.pointer:05}: CAL] Call to {a}, return to {stack_val}")
        self.pointer = a

    def __ret(self, args_count):
        """[18]: Remove the top element from the stack and jump to it; empty stack = halt"""
        if not self.output_stack:
            self.debug_log(f"[{self.pointer:05}: RET]  EMPTY OUTPUT STACK")
            self.__terminate(args_count)
        ret_addr = self.output_stack.pop()
        self.debug_log(f"[{self.pointer:05}: RET] Return to {ret_addr}")
        self.pointer = ret_addr

    def __out(self, args_count):
        """[19]: Write the character represented by ascii code `a` to the terminal"""
        a_raw,  = self.__get_args(args_count)
        a = self.__validate_val(a_raw)
        char_a = chr(a)
        self.output_terminal[-1] += char_a
        self.debug_log(f"[{self.pointer:05}: OUT]{repr(char_a)} to terminal (ASCII Code: {a})")
        return args_count

    def __input(self, args_count):
        """[20]: Read a character from the terminal and write its ascii code to `a`"""
        if not self.input_commands:
            self.paused = True
            self.debug_log(f"[{self.pointer:05}: INP] Empty Input | Pause Computer)")
            return None
        a_raw,  = self.__get_args(args_count)
        a = self.__get_reg_no(a_raw)
        input_char = self.input_commands.pop(0)
        input_ascii = ord(input_char)
        self.__set_registers(a, input_ascii)
        self.debug_log(f"[{self.pointer:05}: INP] reg[{a}] = {input_ascii} ({input_char} -> {input_ascii})")
        return args_count

    def __noop(self, args_count):
        """[21]: No Operation"""
        self.debug_log(f"[{self.pointer:05}: NOP] No Operation Performed")
        return args_count

    def replicate(self, copy_no = 1):
        """Create and return a copy of the current VirtualMachine instance, preserving its state."""
        # Create a new instance with the original program bytes
        new_vm = VirtualMachine(self.program_bytes, debug=self.debug)

        # Deep copy the current VM state
        new_vm.paused = self.paused
        new_vm.running = self.running
        new_vm.pointer = self.pointer
        new_vm.memory  = self.memory.copy()
        new_vm.registers = self.registers.copy()
        new_vm.output_stack = self.output_stack.copy()
        new_vm.input_commands = self.input_commands.copy()
        new_vm.output_terminal = self.output_terminal.copy()
        new_vm.software_patches = self.software_patches
        new_vm.version_no = copy_no

        # Copy operation log and add replication marker
        new_vm.op_log = self.op_log.copy()
        new_vm.debug_log(f"[{new_vm.version_no:05}_COPY] __REPLICATED VM AT CURRENT STATE__")

        return new_vm

    def add_input(self, input_commands):
        """Add input commands to the VM's input commands queue."""
        if isinstance(input_commands, list):
            input_commands = '\n'.join(input_commands)
        else:
            input_commands = [input_commands]

        self.input_commands.extend(input_commands)
        self.output_terminal.append("")
        self.paused = False
        self.debug_log(f"[ADD INPUTS] Add series of commands to input commands queue")

    def debug_log(self, message):
        """If debug is True, add op_message to an operation log"""
        if self.debug:
            self.op_log.append(message)

    def save_log(self, file_name = "vm_log", file_loc = ""):
        """Save log to a .txt file"""
        import os
        full_path = os.path.join(file_loc, f"{file_name}.txt")
        with open(full_path, "w") as f:
            f.write('\n'.join(self.op_log))

    def monkey_patching(self, patches):
        self.software_patches = patches
        self.debug_log(f"[{self.pointer:05}: UPD] Software Patched")

    def run_computer(self, input_commands = []):
        """Run Computer with an initial list of commands"""
        if input_commands:
            self.add_input(input_commands + [""])

        while self.running and not self.paused:
            opcode = self.memory[self.pointer]
            if opcode not in self.opcode_map:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")

            op_fn, (func_args) = self.opcode_map[opcode]
            move_ip = op_fn(func_args)

            if move_ip is not None:
                self.pointer += move_ip + 1

            # Call monkey patch if available
            if hasattr(self, "software_patches") and callable(self.software_patches):
                self.software_patches(self.pointer, self.registers, self.memory)

        return self.output_terminal