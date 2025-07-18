import re, operator

class EquationParser:
    OP_DICT = {
        '+': operator.add, '-': operator.sub,  '*': operator.mul, '**': operator.pow
    }

    def __init__(self, equation_str):
        lhs, rhs = equation_str.split("=")
        self.rhs = int(rhs.strip())
        self.parts = re.split(r'(_)', lhs.strip())
        self.indices = [i for i, x in enumerate(self.parts) if x == '_']
        self.has_placeholders = bool(self.indices)

    def evaluate(self, values=None):
        """Evaluate the equation.
        If values are provided, fill them into placeholders. If not, assume equation is fully concrete.
        """
        expr = self.parts[:]
        if self.has_placeholders:
            assert values is not None and len(values) == len(self.indices)
            for i, idx in enumerate(self.indices):
                expr[idx] = str(values[i])

        expr_str = ''.join(expr).replace("^", "**")
        tokens = re.findall(r'\d+|[\+\-\*]{1,2}', expr_str)
        result = self._evaluate_tokens(tokens)
        return result == self.rhs

    def _evaluate_tokens(self, tokens):
        for prec in (["**"], ["*"], ["+", "-"]):
            tokens = self._apply(tokens, prec)
        return int(tokens[0])

    def _apply(self, tokens, precedence):
        stack = []
        i = 0
        while i < len(tokens):
            if tokens[i] in precedence:
                a = int(stack.pop())
                b = int(tokens[i + 1])
                op = self.OP_DICT[tokens[i]]
                stack.append(str(op(a, b)))
                i += 2
            else:
                stack.append(tokens[i])
                i += 1
        return stack

    def to_callable(self):
        """Return a function taking a tuple of values to test the equation."""
        assert self.has_placeholders
        return lambda p: self.evaluate(p)
