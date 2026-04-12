import sys
import re

PRECEDENCE = {"<": 0, ">": 0, "<=": 0, ">=": 0, "==": 0, "+": 1, "-": 1, "*": 2, "/": 2}

VARIABLES = {}

DIRECTION = 1

def evaluate(line):
    values = []
    operators = []

    for token in line:
        # numeric literal
        if type(token) == float:
            values.append(token)
        # string literal created by tokenize is stored as a tuple
        elif isinstance(token, tuple) and token[0] == '__str__':
            values.append(token[1])
        elif token in PRECEDENCE:
            if len(operators) == 0:
                operators.append(token)
                continue

            current_operator = token
            # IF previous operator has HIGHER precedence
            prev_operator = operators[-1]
            if PRECEDENCE[prev_operator] >= PRECEDENCE[current_operator]:
                op = operators.pop()
                value_2 = values.pop()
                value_1 = values.pop()
                # use repr to ensure string operands are quoted for eval
                result = eval(f"{repr(value_1)} {op} {repr(value_2)}")
                values.append(result)

            operators.append(token)
        else:
            # variable, take value out
            value = VARIABLES[token]
            values.append(value)

    while len(operators) > 0:
        op = operators.pop()
        value_2 = values.pop()
        value_1 = values.pop()
        result = eval(f"{repr(value_1)} {op} {repr(value_2)}")
        values.append(result)

    return values[0]

def run(line,lines,line_index):
    global DIRECTION
    if len(line) == 0:
        pass
    elif line[0] == "print":
        value = line[1:]
        print(evaluate(value))
    elif len(line) >= 2 and line[1] == "=":
        # assignment
        variable = line[0]
        value = evaluate(line[2:])
        VARIABLES[variable] = value
    elif line[0] == "check":
        # Find the condition tokens before ':'
        if ":" in line:
            colon_index = line.index(":")
            condition = line[1:colon_index]
        else:
            # e.g. check x < 5 :
            condition = line[1:]

        # If there are tokens after ':' on the same line, treat this as an
        # inline check (single-line action) rather than a block check.
        if ":" in line and colon_index < len(line) - 1:
            action = line[colon_index + 1:]

            def execute_action(tokens):
                """Execute a single inline action list. Supports nested
                `check` actions recursively, `reverse`, assignments and
                `print`.
                """
                if len(tokens) == 0:
                    return

                if tokens[0] == "check":
                    # find colon in nested tokens
                    if ":" in tokens:
                        ci = tokens.index(":")
                        cond = tokens[1:ci]
                        nested = tokens[ci+1:]
                        if evaluate(cond):
                            execute_action(nested)
                    else:
                        # simple check without action (no-op)
                        if evaluate(tokens[1:]):
                            return
                    return

                # non-check actions
                if len(tokens) == 1 and tokens[0] == "reverse":
                    globals()["DIRECTION"] = globals()["DIRECTION"] * -1
                elif len(tokens) >= 2 and tokens[1] == "=":
                    var = tokens[0]
                    val = evaluate(tokens[2:])
                    VARIABLES[var] = val
                elif tokens[0] == "print":
                    print(evaluate(tokens[1:]))
                else:
                    # unsupported action (ignore)
                    return

            if evaluate(condition):
                execute_action(action)

            # inline check doesn't have a block: nothing more to skip
            return None

        # Find where block starts (the '{' line)
        block_start = line_index + 1
        while block_start < len(lines) and "{" not in lines[block_start]:
            block_start += 1

        # Find where block ends (matching '}')
        block_end = block_start + 1
        brace_count = 1
        while block_end < len(lines) and brace_count > 0:
            if "{" in lines[block_end]:
                brace_count += 1
            elif "}" in lines[block_end]:
                brace_count -= 1
            block_end += 1
            

        # Execute the block if condition is true
        if evaluate(condition):
            # Instead of iterating the block here, return the index of the
            # first executable line inside the block (respecting current DIRECTION).
            # The main loop will then continue stepping with
            # DIRECTION, so a `reverse` encountered while inside the block
            # immediately affects traversal direction.
            first = block_start + 1
            last = block_end - 2

            if DIRECTION >= 0:
                # jump into the block at its first line
                return first
            else:
                # if direction is reversed, start at the last executable
                # line inside the block so stepping upwards will work
                return last

        # if condition false: skip the block entirely
        return block_end - 1

    

            

        
    elif line[0] == "reverse":
        DIRECTION = DIRECTION * -1

def main():
    filepath = sys.argv[1]

    with open(filepath) as file:
        lines = file.readlines() 
        lines = [tokenize(line) for line in lines]
    
    line_index = 0
    # Debug: print tokenized lines (commented out for normal use)
    # print(lines)
    while line_index >= 0 and line_index < len(lines):
        line = lines[line_index]
        new_index = run(line, lines, line_index)
        if new_index is not None:
            line_index = new_index + DIRECTION
        else:
            line_index += DIRECTION

    

def tokenize(line):
    # split into quoted strings or non-whitespace tokens
    parts = re.findall(r'".*?"|\'.*?\'|\S+', line)
    tokens = []
    for item in parts:
        # string literal
        if (item.startswith('"') and item.endswith('"')) or (item.startswith("'") and item.endswith("'")):
            # store as a tuple to distinguish from variable names
            tokens.append(('__str__', item[1:-1]))
            continue

        # try numeric
        try:
            token = float(item)
        except:
            token = item

        tokens.append(token)

    return tokens

main()