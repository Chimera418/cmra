"""
fire.py — Fire Dragon Interpreter (alias-based syntax)
Original: cmra.py

Exposed API:
    FireInterpreter().run(file_path)
    FireInterpreter().run_source(source)
    run(file_path)          # convenience wrapper
"""

import re

PRECEDENCE = {"<": 0, ">": 0, "<=": 0, ">=": 0, "==": 0, "+": 1, "-": 1, "*": 2, "/": 2}


class FireInterpreter:
    """Stateful Fire Dragon interpreter instance.

    Each instance has isolated VARIABLES and DIRECTION so multiple
    runs or REPL sessions don't bleed state into each other.
    """

    def __init__(self):
        self.variables: dict = {}
        self.direction: int = 1

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, file_path: str) -> None:
        """Execute a .cmra file."""
        with open(file_path, encoding="utf-8") as f:
            source = f.read()
        self.run_source(source)

    def run_source(self, source: str) -> None:
        """Execute CMRA source code given as a string."""
        lines = [self._tokenize(line) for line in source.splitlines()]
        line_index = 0
        while 0 <= line_index < len(lines):
            line = lines[line_index]
            new_index = self._run_line(line, lines, line_index)
            if new_index is not None:
                line_index = new_index + self.direction
            else:
                line_index += self.direction

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _tokenize(self, line: str) -> list:
        parts = re.findall(r'".*?"|\'.*?\'|\S+', line)
        tokens = []
        for item in parts:
            # comment
            if item == "murmur":
                break
            if (item.startswith('"') and item.endswith('"')) or \
               (item.startswith("'") and item.endswith("'")):
                tokens.append(("__str__", item[1:-1]))
                continue
            try:
                tokens.append(float(item))
            except ValueError:
                tokens.append(item)
        return tokens

    def _evaluate(self, token_list: list):
        values = []
        operators = []

        def apply_op(v1, op, v2):
            if op == "+" and (isinstance(v1, str) or isinstance(v2, str)):
                return str(v1) + str(v2)
            return eval(f"{repr(v1)} {op} {repr(v2)}")

        for token in token_list:
            if type(token) == float:
                values.append(token)
            elif isinstance(token, tuple) and token[0] == "__str__":
                values.append(token[1])
            elif token in PRECEDENCE:
                if not operators:
                    operators.append(token)
                    continue
                prev = operators[-1]
                if PRECEDENCE[prev] >= PRECEDENCE[token]:
                    op = operators.pop()
                    v2 = values.pop()
                    v1 = values.pop()
                    values.append(apply_op(v1, op, v2))
                operators.append(token)
            else:
                values.append(self.variables[token])

        while operators:
            op = operators.pop()
            v2 = values.pop()
            v1 = values.pop()
            values.append(apply_op(v1, op, v2))

        return values[0]

    def _run_line(self, line: list, lines: list, line_index: int):
        if not line:
            return None
        if line[0] == "murmur":
            return None

        # roar <expr>  →  print
        if line[0] == "roar":
            print(self._evaluate(line[1:]))
            return None

        # <var> bind <expr>  →  assignment
        if len(line) >= 2 and line[1] == "bind":
            self.variables[line[0]] = self._evaluate(line[2:])
            return None

        # sniff <condition> [: <action>]  →  conditional
        if line[0] == "sniff":
            return self._handle_sniff(line, lines, line_index)

        # dive / soar  →  direction control
        if line[0] == "dive":
            self.direction = 1
            return None
        if line[0] == "soar":
            self.direction = -1
            return None

        return None

    def _handle_sniff(self, line: list, lines: list, line_index: int):
        if ":" in line:
            colon_index = line.index(":")
            condition = line[1:colon_index]
        else:
            condition = line[1:]

        # Inline: sniff <cond> : <action>
        if ":" in line and colon_index < len(line) - 1:
            action = line[colon_index + 1:]
            if self._evaluate(condition):
                self._execute_inline(action)
            return None

        # Block: sniff <cond>\n{\n  ...\n}
        block_start = line_index + 1
        while block_start < len(lines) and "{" not in lines[block_start]:
            block_start += 1

        block_end = block_start + 1
        brace_count = 1
        while block_end < len(lines) and brace_count > 0:
            if "{" in lines[block_end]:
                brace_count += 1
            elif "}" in lines[block_end]:
                brace_count -= 1
            block_end += 1

        if self._evaluate(condition):
            first = block_start + 1
            last = block_end - 2
            return first if self.direction >= 0 else last

        return block_end - 1

    def _execute_inline(self, tokens: list) -> None:
        if not tokens:
            return
        if tokens[0] == "sniff":
            if ":" in tokens:
                ci = tokens.index(":")
                cond = tokens[1:ci]
                nested = tokens[ci + 1:]
                if self._evaluate(cond):
                    self._execute_inline(nested)
            return
        if len(tokens) == 1 and tokens[0] == "dive":
            self.direction = 1
        elif len(tokens) == 1 and tokens[0] == "soar":
            self.direction = -1
        elif len(tokens) >= 2 and tokens[1] == "bind":
            self.variables[tokens[0]] = self._evaluate(tokens[2:])
        elif tokens[0] == "roar":
            print(self._evaluate(tokens[1:]))


# ------------------------------------------------------------------
# Convenience module-level function
# ------------------------------------------------------------------

def run(file_path: str) -> None:
    """Run a .cmra file with a fresh Fire interpreter."""
    FireInterpreter().run(file_path)
