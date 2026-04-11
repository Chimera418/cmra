# 🐉 CMRA Language (Chimera)

> **"Where code breathes fire and flows like flame..."**

**CMRA** (Chimera) is an esoteric programming language that explores reversible execution and direction control through an expressive, dragon-inspired syntax. Like a chimera commanding the elements, CMRA lets you control program flow with fiery commands that can soar upwards or dive downwards through your code.

🔥 **GitHub Repository:** [https://github.com/TeapotChimera418/cmra](https://github.com/TeapotChimera418/cmra)  
🌐 **Live Playground:** [https://cmra-esolang.vercel.app/playground.html](https://cmra-esolang.vercel.app/playground.html)  
📚 **Documentation:** [https://cmra-esolang.vercel.app/index.html](https://cmra-esolang.vercel.app/index.html)

---

## 🙌 Intro

CMRA began as a workshop project I attended by
[Tushar Sadhwani](https://github.com/tusharsadhwani) during a college multifest. The
prototype we built is in `prototype.py`. For a non‑aliased baseline, see Tushar's
[esolangs](https://github.com/tusharsadhwani/esolangs) repository. You can also read his
blog at [tush.ar](https://tush.ar).

This is a tiny side project made for fun and learning. If you build something cool or want
to improve the interpreter, feel free to reach out on
[GitHub (@TeapotChimera418)](https://github.com/TeapotChimera418) or Discord `gamingchimera`.

## ✨ Try it Online!

**🔥 [Launch the Interactive Playground](https://cmra-esolang.vercel.app/index.html)**

Write and run CMRA code directly in your browser! Features:
- 🐲 Toggle between Fire Dragon and Shadow Dragon interpreters
- 📁 Load example test cases and projects
- 💾 Upload your own `.cmra` files
- ⚡ Instant execution powered by Pyodide (Python in WebAssembly)
- 🎨 Syntax highlighting with line numbers

No installation required — just code and go!

## 🔱 The Twin Dragons

Two interpreters guard the secrets of CMRA:

- **`cmra.py`** — The **Fire Dragon**: Commands that roar and soar with expressive aliases (`bind`, `roar`, `sniff`, `dive`, `soar`, `murmur`)
- **`cmra_simplified.py`** — The **Shadow Dragon**: Minimal, direct commands (`=`, `print`, `check`, `reverse`, `{ }`)
- **`prototype.py`** — The **Ancient Wyrm**: Original compact baseline

📜 **Quick Reference:** `keybind.txt` — Sacred scroll mapping Fire ↔ Shadow dragon tongues  
🌐 **Web Grimoire:** Open `index.html` for interactive documentation

---

## 🔥 Quick Ignition (Windows PowerShell)

Breathe fire into your programs:

```powershell
# Fire Dragon (CMRA alias syntax)
python .\cmra.py ".\test cases\test.cmra"

# Shadow Dragon (simplified syntax)
python .\cmra_simplified.py .\test.rev
```

You can also use `py` as your incantation:

```powershell
py cmra.py "test cases\test_strings.cmra"
py cmra_simplified.py test.rev
```

---

## 🐲 The Dragon's Tongue (Language Overview)

### Shadow Dragon Syntax (`cmra_simplified.py`)

The minimalist path — direct and powerful:

- **Variables:** `x = 3`
- **Print:** `print x + 5` (numbers or strings; strings use quotes)
- **Conditionals:**
  - Inline: `check x < 5 : print x`
  - Block: `check x < 5 : { ... }`
- **Reverse direction:** `reverse` flips the global execution flow
- **Nested checks:** `check x <= 10 : check flag == 1 : reverse`

⚡ **Note:** In the Fire Dragon syntax, `reverse` is split into `dive` (descend) and `soar` (ascend).

### Fire Dragon Syntax (`cmra.py`)

The expressive path — commands that speak of power:

| Command | Purpose | Example |
|---------|---------|---------|
| `bind` | Assignment | `x bind 3` |
| `roar` | Print/output | `roar "Dragon awakens!"` |
| `sniff` | Conditional | `sniff x < 5 : roar x` |
| `dive` | Descend (forward direction) | `dive` |
| `soar` | Ascend (reverse direction) | `soar` |
| `murmur` | Comment (whisper) | `murmur This is a note` |

**Equivalence with Shadow Dragon:**
- `soar` ≈ `reverse` (reverse direction / ascend through code)
- `dive` sets forward direction (no simplified equivalent; forward is default)

#### Fire Dragon Examples

**Inline conditional:**
```
sniff x <= 10 : roar x
```

**Block conditional:**
```
sniff x < 5 :
{
  roar "inside the flames"
}
```

**Strings:** Single or double quotes. `"fire" + 2` becomes `"fire2"`.

---

## 🔥 Expression Rules & Flame Types

- **Numbers** are floats by default: `2` becomes `2.0`
- **Operator precedence:** `*`, `/` > `+`, `-` > comparisons (`<`, `>`, `<=`, `>=`, `==`)
- **String concatenation:** Use `+`. If either side is a string, both are coerced to strings
- **Variables:** Live in a global `VARIABLES` cauldron

---

## ⚡ The Flow of Fire (Execution Model)

CMRA's power lies in **reversible execution**:

- A global `DIRECTION` controls traversal: `1` = forward (dive), `-1` = reverse (soar)
- **Fire Dragon:** `dive` sets `DIRECTION = 1`; `soar` sets `DIRECTION = -1`
- **Shadow Dragon:** `reverse` toggles direction
- **Block magic:** When a `sniff/check` condition is true, the interpreter jumps into the block (first line forward, last line reverse). The main loop continues stepping with `DIRECTION`, so a `soar/reverse` inside a block takes effect immediately.

### Block Entry Ritual

- If condition is **true** and `DIRECTION >= 0` → jump to **first** line inside block
- If condition is **true** and `DIRECTION < 0` → jump to **last** line inside block
- If condition is **false** → skip past the block entirely

---

## 🌀 Dragon Loop Patterns (Reusable Incantations)

### 🔥 Pattern 1: Flagged Loop (Inline Style)

Perfect for simple counters and iterations:

```
flag bind 1
sniff cond : sniff flag == 0 : dive
flag bind 0
sniff flag == 0 : ;;; body (do work here)
sniff flag == 0 : ;;; step (i bind i + 1)
flag bind 1
sniff cond : sniff flag == 1 : soar
```

### 🔥 Pattern 2: Block Loop (Brace Style)

Better for grouping complex logic:

```
flag bind 0
sniff cond :
{
  sniff flag == 1 : dive
  sniff cond : flag bind 1
  sniff flag == 1 : ;;; body (do work here)
  sniff flag == 1 : ;;; step (i bind i + 1)
  sniff cond : flag bind 0
  sniff flag == 0 : soar
}
```

### ⚠️ Dragon's Warning

- **Always guard** loop bodies with the `flag` variable so reverse passes don't re-execute
- **Nested loops:** Apply the same guarding pattern to inner loops
- Without guards, your code will breathe fire chaotically on reverse traversals!

---

## 🎮 Test the Dragon's Breath

### CMRA Test Cases (Fire Dragon)

All tests live in `test cases cmra/`:

- `test.cmra` — Hello world + loop 0→10 using `sniff`/`dive`/`soar`
- `test_strings.cmra` — String literals and concatenation
- `test_arith.cmra` — Arithmetic precedence (*/ before +−). Expected: `7`, `9`
- `test_cond.cmra` — Inline conditions. Expected: `ok`, then `3`
- `test_block.cmra` — Block-style `sniff`. Expected: `inside`, then `after`

### Shadow Dragon Test Cases

All tests live in `test cases cmra_simplified/`:

- `test.cmrasim` — Basic loops and nested blocks using `check`/`reverse`
- `test_strings.cmrasim` — String literals and concatenation
- `test_arith.cmrasim` — Arithmetic precedence. Expected: `7`, `9`
- `test_cond.cmrasim` — Inline conditions. Expected: `ok`, then `3`
- `test_block.cmrasim` — Block-style `check`. Expected: `inside`, then `after`

### 🔥 Epic Dragon Projects

Witness the power of CMRA in action:

- **`projects/story_adventure.cmra`** — 🏰 **Interactive text adventure!** A complete story with characters, battles, and narrative choices. The dragon tells tales!
- **`projects/calculator.cmra`** — 🧮 Math operations: addition, subtraction, factorial, series sum, power calculations (demonstrates both loop patterns)
- **`projects/countdown.cmra`** — 🚀 Rocket launch countdown and reversible counters (shows forward/reverse flow)
- **`projects/fizzbuzz.cmra`** — 🎲 Classic FizzBuzz using counter-based modulo logic

### 🔥 Run the Dragons

```powershell
# Fire Dragon test cases
python .\cmra.py ".\test cases cmra\test_block.cmra"
python .\cmra.py ".\test cases cmra\test_strings.cmra"
python .\cmra.py ".\test cases cmra\test_arith.cmra"

# Shadow Dragon test cases
python .\cmra_simplified.py ".\test cases cmra_simplified\test_block.cmrasim"
python .\cmra_simplified.py ".\test cases cmra_simplified\test_strings.cmrasim"

# Epic projects (Fire Dragon only)
python .\cmra.py .\projects\story_adventure.cmra
python .\cmra.py .\projects\calculator.cmra
python .\cmra.py .\projects\countdown.cmra
python .\cmra.py .\projects\fizzbuzz.cmra
```

### Shadow Dragon Test

- `test.rev` — Sample for `cmra_simplified.py`: nested blocks, inline actions, `reverse` direction flipping

```powershell
python .\cmra_simplified.py .\test.rev
```

**Or try everything online at:** [https://cmra-esolang.vercel.app/index.html](https://cmra-esolang.vercel.app/index.html)

---

## 📦 Dragon's Hoard (File Inventory)

- **`cmra.py`** — Fire Dragon interpreter (full features: alias keywords, inline + block `sniff`)
- **`cmra_simplified.py`** — Shadow Dragon interpreter (minimal: `check`, `print`, `reverse`, braces)
- **`prototype.py`** — Ancient Wyrm (compact baseline with inline `sniff` only)
- **`keybind.txt`** — Sacred scroll mapping Fire ↔ Shadow dragon tongues
- **`index.html`** — Interactive documentation site with dragon-themed design
- **`playground.html`** — Browser-based code playground with Pyodide integration
- **`styles.css`** — Dragon fire theme styling
- **`projects/`** — Showcase programs (calculator, countdown, fizzbuzz, story_adventure)
- **`test cases cmra/`** — Fire Dragon test cases (.cmra files)
- **`test cases cmra_simplified/`** — Shadow Dragon test cases (.cmrasim files)

---

## ⚠️ Dragon's Wisdom (Pitfalls & Tips)

### 🔥 Beware the Reverse Flame

- Direction reversals **re-traverse lines**. Without a guarding `flag`, assignments and prints will repeat
- **Use the loop patterns** above to tame the reverse fire

### 🔥 String Growth Inferno

- Concatenating inside unguarded loops = exponential string growth
- Build strings once per forward pass, guard with flags

### 🔥 Numbers are Floats

- All numbers parse as floats (`2` → `2.0`)
- Want integers? Adapt tokenization to parse ints before floats

### 🔥 Nested Dragons

- Nested loops work, but **every inner body needs flag guards**
- Without guards, inner loops re-execute on reverse passes

---

## 🛠️ Forging New Dragon Powers (Extending CMRA)

Want to add new commands? Follow the ancient pattern:

1. **Top-level dispatch** — Add your command alongside `roar`/`print`
2. **Inline action executor** — Enable it in nested `sniff`/`check` statements

Study how `roar`, `bind`, `dive`, and `soar` are implemented in both interpreters.

---

## 🐉 The Ancient Wyrm (Prototype)

`prototype.py` is the original compact CMRA interpreter:

- Supports: `murmur`, `roar`, `bind`, `sniff` (inline only), `soar`, `dive`
- Useful for understanding the core mechanics
- No block `sniff` — inline conditionals only

---

## 📜 License

CMRA is a learning and experimentation project. Use freely, learn deeply, code fiercely! 🔥

---

**May your code burn bright and your loops reverse true!** 🐉🔥
