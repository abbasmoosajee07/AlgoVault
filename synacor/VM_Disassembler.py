class VM_Disassembler:
    def __init__(self, virtual_machine):
        self.vm = virtual_machine
        self.M = self.vm.MODULUS
        self.program = self.vm.program
        self.opcode_metadata = self.__opcode_metadata(self.vm.opcode_map)

    def __opcode_metadata(self, opcode_map):
        """
        Build a dictionary of {opcode: (name, argcount)} from the VM's opcode map.
        Special handling for grouped operations (e.g., arithmetic).
        """
        metadata = {}
        for opcode, (func, argspec) in opcode_map.items():
            name = func.__name__.lstrip('_')
            argcount = argspec
            if name in {"arithmetic", "and_or"}:
                argcount, name = argspec
            metadata[opcode] = (name, argcount)
        return metadata

    def format_instruction(self, address, instruction):
        """Format a single disassembled instruction as a string."""
        opcode = instruction[0]
        opname, _ = self.opcode_metadata.get(opcode, ("???", 0))

        def format_arg(arg):
            if opcode == 19:  # 'out'
                return repr(chr(arg))
            return str(arg) if arg < self.M else f"R[{arg - self.M}]"

        args = " ".join(format_arg(arg) for arg in instruction[1:])
        return f"{address:5}: {opname:7} {args}".rstrip()

    def disassemble(self, start, count):
        """
        Disassemble `count` instructions starting from `start` address.
        Prints disassembled output directly.
        """
        i = start
        printed = 0
        r7_call_point = None
        program = self.program
        disassembled_prog = [f"\nDisassembly from address {start} for {count} instructions:\n"]

        while printed < count and i < len(program):
            opcode = program[i]
            if opcode not in self.opcode_metadata:
                print(f"{i:5}: ???     Invalid opcode {opcode}")
                break
            _, argcount = self.opcode_metadata[opcode]
            instr = program[i:i + 1 + argcount]
            if opcode == 17:
                r7_call_point = i
            disassembled_prog.append(self.format_instruction(i, instr))
            i += 1 + argcount
            printed += 1
        return r7_call_point, disassembled_prog

    @staticmethod
    def ackermann_func(m, n, k, M):
        """
        A stack-based variation of the Ackermann function with parameters:
        - m, n: initial input values
        - k: custom constant controlling growth
        - M: modulus applied to all results

        The behavior is defined by:
        - A(0, n) = (n + 1) % M
        - A(1, n) = (n + k + 1) % M
        - A(2, n) = ((n + 2) * k + n + 1) % M
        - A(m, 0) = A(m - 1, k)
        - A(m, n) = A(m - 1, A(m, n - 1))
        """
        stack = [m, n]

        while len(stack) > 1:
            n = stack.pop()
            m = stack.pop()

            if m == 0:
                stack.append((n + 1) % M)
            elif m == 1:
                stack.append((n + k + 1) % M)
            elif m == 2:
                stack.append(((n + 2) * k + n + 1) % M)
            elif n == 0:
                stack.extend([m - 1, k])
            else:
                stack.extend([m - 1, m, n - 1])

        return stack[0]
