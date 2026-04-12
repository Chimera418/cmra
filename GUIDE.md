# 🐉 CMRA User Guide

> The complete guide to writing, running, and understanding Chimera programs.

---

## Table of Contents

1. [Installation](#installation)
2. [Running Programs](#running-programs)
3. [Language Basics](#language-basics)
   - [Fire Dragon syntax](#fire-dragon-syntax-cmra-files)
   - [Shadow Dragon syntax](#shadow-dragon-syntax)
4. [Expressions & Types](#expressions--types)
5. [Control Flow & Direction](#control-flow--direction)
6. [Block Conditionals](#block-conditionals)
7. [Writing Loops](#writing-loops)
8. [Common Pitfalls](#common-pitfalls)
9. [Example Programs](#example-programs)
10. [Extending the Language](#extending-the-language)

---

## Installation

### Option A — pip (recommended, gives you the `cmra` command globally in your venv)

```powershell
# From the project root, with your venv activated:
pip install -e .

# Then anywhere inside the venv:
cmra myprogram.cmra
```

### Option B — PowerShell wrapper (no install needed)

```powershell
# From the project root:
.\cmra.ps1 "test cases\test.cmra"

# Add the project root to PATH for this session so you can use `cmra` anywhere:
$env:PATH = "C:\path\to\CMRA;$env:PATH"
cmra test.cmra
```

### Option C — Run directly with Python

```powershell
python -m cmra.cli myprogram.cmra
# or, if you just want the legacy single-file interpreters:
python cmra.py myprogram.cmra
python cmra_simplified.py myprogram.cmrasim
```

---

## Running Programs

```powershell
# Basic usage
cmra <filename>

# Examples
cmra "test cases\test.cmra"
cmra projects\calculator.cmra
cmra projects\fizzbuzz.cmra
```

> **File extensions**  
> `.cmra` → Fire Dragon (expressive aliases)  
> `.cmrasim` / `.rev` → Shadow Dragon (minimal syntax)  
> Both extensions work with all interpreters; the extension is just a convention.

---

## Language Basics

CMRA has two "dialects" with identical semantics. Pick whichever resonates.

### Fire Dragon syntax (`.cmra` files)

| Keyword | Role | Example |
|---------|------|---------|
| `bind` | Assign a variable | `x bind 5` |
| `roar` | Print a value | `roar "hello"` / `roar x + 1` |
| `sniff` | Conditional | `sniff x < 10 : roar x` |
| `dive` | Set direction → forward | `dive` |
| `soar` | Set direction → reverse | `soar` |
| `murmur` | Comment (rest of line ignored) | `murmur this is a note` |

**Variables** use `bind`:
```
x bind 3
name bind "Chimera"
roar name
```

### Shadow Dragon syntax

| Keyword | Role | Example |
|---------|------|---------|
| `=` | Assign a variable | `x = 5` |
| `print` | Print a value | `print x + 1` |
| `check` | Conditional | `check x < 10 : print x` |
| `reverse` | Toggle direction | `reverse` |
| `;` | Comment | `; this is a note` |

```
x = 3
name = "Chimera"
print name
```

---

## Expressions & Types

- **Numbers** are always floats: `2` → `2.0`, `3.14` → `3.14`
- **Strings** use single or double quotes: `"hello"` `'world'`
- **Arithmetic** follows standard precedence:
  - `*` `/` bind tighter than `+` `-`
  - Comparisons (`<` `>` `<=` `>=` `==`) have lowest precedence
- **String + anything** → string concatenation:
  - `"fire" + 2` → `"fire2"`
  - `"count: " + x` → `"count: 5.0"` (if x is 5)
- **Variables** are global and persist throughout execution

```
x bind 4
roar x * 3 + 1    murmur → 13.0
roar "val: " + x  murmur → "val: 4.0"
```

---

## Control Flow & Direction

CMRA's defining feature is a **global direction** that controls how the interpreter steps through lines.

| Direction | Value | Moves |
|-----------|-------|-------|
| Forward (default) | `1` | Line 1 → 2 → 3 … |
| Reverse | `-1` | Line N → N-1 → N-2 … |

**Fire Dragon:**
- `dive` → sets `DIRECTION = 1` (forward)
- `soar` → sets `DIRECTION = -1` (reverse)

**Shadow Dragon:**
- `reverse` → toggles direction (forward ↔ reverse)

The program terminates when the instruction pointer goes past the first or last line.

---

## Block Conditionals

Blocks group multiple lines under a single condition:

```
sniff x < 5 :
{
  roar "x is small"
  roar x
}
```

**Block entry rules:**

| Condition | Direction | Enters at |
|-----------|-----------|-----------|
| True | Forward | **First** line of block |
| True | Reverse | **Last** line of block |
| False | Either | Skip entire block |

This means a `soar` inside a block takes effect immediately — very useful for building loops.

---

## Writing Loops

CMRA has no native loop keyword. Instead, you use **direction reversal + flag guards**.

### Pattern 1 — Inline flagged loop

Best for simple counters:

```
murmur ── setup ──────────────────────────────────
i bind 0
flag bind 1

murmur ── loop boundary (top) ────────────────────
sniff i < 10 : sniff flag == 0 : dive

murmur ── flag guard: skip body on reverse pass ──
flag bind 0

murmur ── body (only runs on forward pass) ───────
sniff flag == 0 : roar i
sniff flag == 0 : i bind i + 1

murmur ── restore flag ────────────────────────────
flag bind 1

murmur ── loop boundary (bottom) ────────────────
sniff i < 10 : sniff flag == 1 : soar
```

**How it works:**
1. Program reaches bottom `sniff` → condition true → `soar` → reverses direction
2. On reverse pass, `flag bind 0` line re-executes, setting flag=0... but then `flag bind 1` restores it before the top boundary, so the top `dive` re-fires
3. Body lines are guarded by `sniff flag == 0`, so they only run when flag=0 (the forward pass)

### Pattern 2 — Block loop

Better for complex bodies:

```
flag bind 0
sniff i < 10 :
{
  sniff flag == 1 : dive
  sniff i < 10 : flag bind 1
  sniff flag == 1 : roar i
  sniff flag == 1 : i bind i + 1
  sniff i < 10 : flag bind 0
  sniff flag == 0 : soar
}
```

> **Key rule:** Always guard loop bodies with a flag variable so reverse traversals don't re-execute them.

---

## Common Pitfalls

### 🔥 Forgetting flag guards

```
murmur BAD — prints twice per iteration!
roar i
i bind i + 1
```

```
murmur GOOD — only runs on forward pass
sniff flag == 0 : roar i
sniff flag == 0 : i bind i + 1
```

### 🔥 String growth in loops

```
murmur BAD — s doubles in length each reverse pass
s bind ""
sniff flag == 0 : s bind s + "x"
```

Build strings outside loops, or ensure the assignment is guarded.

### 🔥 Numbers print as floats

`roar 5` prints `5.0`, not `5`. This is by design — all numeric literals are floats.

### 🔥 Nested loops need nested flags

```
murmur outer flag: flag_outer
murmur inner flag: flag_inner
murmur Each inner body line must be guarded with flag_inner == 0
```

### 🔥 `soar` vs `reverse`

- `soar` **sets** direction to reverse (idempotent — calling it twice is fine)
- `reverse` **toggles** — calling it twice cancels out!
- Use `soar`/`dive` (Fire Dragon) in loops for safety

---

## Example Programs

### Hello World

```
roar "Hello, Chimera!"
```

### Count 0 to 5

```
i bind 0
flag bind 1
sniff i <= 5 : sniff flag == 0 : dive
flag bind 0
sniff flag == 0 : roar i
sniff flag == 0 : i bind i + 1
flag bind 1
sniff i <= 5 : sniff flag == 1 : soar
```

### FizzBuzz (simplified — see `projects/fizzbuzz.cmra` for full version)

```
murmur Uses counter-based modulo (no % operator)
murmur See projects/fizzbuzz.cmra for the complete implementation
```

### Run the bundled projects

```powershell
cmra projects\calculator.cmra       # factorial, series, power
cmra projects\countdown.cmra        # reversible countdown
cmra projects\fizzbuzz.cmra         # fizzbuzz 1–15
cmra projects\story_adventure.cmra  # interactive text adventure
```

---

## Extending the Language

To add a new command to the Fire Dragon interpreter (`src/cmra/fire.py`):

1. **Top-level dispatch** — add a branch in `execute_line()` alongside `roar`, `bind`, `sniff`
2. **Inline action support** — add it to `execute_inline_action()` so it can appear after `:` in `sniff` chains
3. **Test it** — add a `.cmra` file to `test cases/`

Look at how `roar`, `bind`, `dive`, and `soar` are implemented — they follow the same two-step pattern.

---

*May your code burn bright and your loops reverse true!* 🐉🔥
