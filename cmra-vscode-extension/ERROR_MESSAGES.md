# CMRA Extension Error Message Catalog

This file documents the message families currently emitted by the VS Code extension diagnostics engine.

## Fire Dragon (.cmra)

### 1) Undefined Variable
- Line {line}: '{name}' is but a myth in this realm.
  Hint: Bind it before you attempt to command it. 🐉
- Line {line}: The dragon searched for '{name}'... but found only ashes.
  Hint: Use 'bind' to summon it into existence. 🔥
- Line {line}: '{name}' has not been bound to the dragon's will.
  Hint: Bind it before invoking its name. 🐲
- Line {line}: No sigil named '{name}' answers your call.
  Hint: Forge it first with 'bind'.

### 2) Missing Condition Colon
- Line {line}: The sniff incantation is incomplete.
  Hint: Add ':' after the condition.

### 3) Missing Print Expression
- Line {line}: A roar with no words shakes only silence.
  Hint: Add an expression after 'roar'.

### 4) Missing Assignment Value
- Line {line}: This binding ritual has no offering.
  Hint: Add a value after 'bind'.

### 5) Wrong Assignment Operator
- Line {line}: Fire Dragon rejects '=' in this chant.
  Hint: Use 'bind' for assignments in .cmra files.

### 6) Unknown Command
- Line {line}: The dragon does not recognize '{found}'.
  Hint: Use known runes like bind, roar, sniff, dive, or soar.

### 7) Unmatched Braces
- Line {line}: The flame-circle of braces is unbalanced.
  Hint: Check that every '{' has a matching '}'.

## Shadow Dragon (.cmrash)

### 1) Undefined Variable
- Line {line}: Undefined variable '{name}'.
  Hint: Initialize it with '=' before using it.
- Line {line}: '{name}' was referenced before assignment.
  Hint: Use '{name} = ...' first.
- Line {line}: Name '{name}' does not exist in scope.
  Hint: Define it using '='.

### 2) Missing Condition Colon
- Line {line}: Invalid check syntax.
  Hint: Add ':' after the condition.

### 3) Missing Print Expression
- Line {line}: 'print' requires an expression.
  Hint: Example: print x + 1

### 4) Missing Assignment Value
- Line {line}: Assignment is missing a value.
  Hint: Use: {name} = <expression>

### 5) Wrong Assignment Operator
- Line {line}: Unexpected 'bind' in .cmrash.
  Hint: Use '=' for assignments.

### 6) Unknown Command
- Line {line}: Unknown command '{found}'.
  Hint: Use '=', print, check, or reverse.

### 7) Unmatched Braces
- Line {line}: Unmatched braces detected.
  Hint: Ensure every '{' has a closing '}'.

## Notes

- The extension picks one random variant per diagnostic occurrence.
- Placeholders:
  - {line}: 1-based line number
  - {name}: variable name
  - {found}: unknown command token
