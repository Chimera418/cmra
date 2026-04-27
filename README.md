# 🐉 CMRA Language (Chimera)

> **"Where code breathes fire and flows like flame..."**

**CMRA** (Chimera) is an esoteric programming language exploring reversible execution and direction control through a dragon-inspired syntax. Programs can soar *up* or dive *down* through code at runtime.

🔥 **GitHub:** [Chimera418/cmra](https://github.com/Chimera418/cmra)  
🌐 **Playground:** [cmra-esolang.vercel.app/playground.html](https://cmra-esolang.vercel.app/playground.html)  
📚 **Docs:** [cmra-esolang.vercel.app](https://cmra-esolang.vercel.app/index.html)  
📖 **User Guide:** [GUIDE.md](GUIDE.md)

---

## 🙌 Origin

CMRA began as a workshop project I attended by
[Tushar Sadhwani](https://github.com/tusharsadhwani) during a college multifest. The
prototype we built is in `prototype.py`. For a non‑aliased baseline, see Tushar's
[esolangs](https://github.com/tusharsadhwani/esolangs) repository. You can also read his
blog at [tush.ar](https://tush.ar).

This is a tiny side project made for fun and learning. If you build something cool or want
to improve the interpreter, feel free to reach out on
[GitHub (@Chimera418)](https://github.com/Chimera418) or Discord [`gamingchimera`](https://discord.com/users/736465046317563915).

## ✨ Try it Online

**🔥 [Launch the Interactive Playground](https://cmra-esolang.vercel.app/playground.html)**

Write and run CMRA code directly in your browser — no installation needed. Powered by Pyodide.

---

## ⚡ Installation & Quick Start

### CMRA Esoteric Language Extension (VS Code / Cursor)

For the best developer experience, install the official IDE extension:
- **Marketplace**: Install directly from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=Chimera418.cmra-esolang) or [Open VSX Registry](https://open-vsx.org/vscode/item?itemName=Chimera418.cmra-esolang). Works on both VS Code and Cursor!
- **Manual Install**: Download the `.vsix` from [GitHub Releases](https://github.com/Chimera418/cmra/releases).
- **Reliable Run command**: Extension run uses `python -m cmra "<file>"` by default.
- **Config override**: Set `cmra.executablePath` if you need a custom interpreter/command.
- **Diagnostics**: Randomized dragon-themed diagnostics for `.cmra`, concise `=`-style diagnostics for `.cmrash`.

#### Diagnostic message examples (extension)

**Fire Dragon (`.cmra`)**
- `Line 4: 'x' is but a myth in this realm.`
	`Hint: Bind it before you attempt to command it. 🐉`
- `Line 5: Fire Dragon rejects '=' in this chant.`
	`Hint: Use 'bind' for assignments in .cmra files.`

**Shadow Dragon (`.cmrash`)**
- `Line 4: Undefined variable 'x'.`
	`Hint: Initialize it with '=' before using it.`
- `Line 5: Unexpected 'bind' in .cmrash.`
	`Hint: Use '=' for assignments.`

Full catalog: [cmra-vscode-extension/ERROR_MESSAGES.md](cmra-vscode-extension/ERROR_MESSAGES.md)

### Standalone Windows Executable

Don't have Python installed? No problem! 
Download the standalone `cmra.exe` from the latest [GitHub Releases](https://github.com/Chimera418/cmra/releases) and add it to your PATH to run CMRA programs natively.

### pip install (recommended)

```powershell
# Install from PyPI:
pip install cmra

# Or install from source (development):
pip install -e .

# Now use `cmra` and `cmrash` from anywhere inside the venv:
cmra "test cases\test.cmra"
cmrash "test cases\test.cmrash"
```

### No-install PowerShell wrapper

```powershell
.\cmra.ps1 "test cases\test.cmra"
```

If you are already inside a subfolder such as `test cases`, use the parent-folder wrapper instead:

```powershell
..\cmra.ps1 "test.cmra"
```

If you install CMRA into your environment and add it to PATH, you can also run:

```powershell
cmra "test cases\test.cmra"
```

### Run with Python directly

```powershell
# Legacy single-file interpreters:
python cmra.py "test cases cmra\test.cmra"
python cmrash.py "test cases cmrash\test.cmrash"
```

---

## 🔱 The Twin Dragons

| Dragon | Entry point | Keywords |
|--------|-------------|----------|
| 🐲 **Fire Dragon** | `cmra.py` / `src/cmra/fire.py` | `bind` `roar` `sniff` `dive` `soar` `murmur` |
| 🌑 **Shadow Dragon** | `cmrash.py` / `src/cmra/shadow.py` | `=` `print` `check` `reverse` `;` |
| 🐉 **Ancient Wyrm** | `prototype.py` | Compact baseline, inline `sniff` only |

---

## 🐲 Language at a Glance

```
murmur Fire Dragon — count 0 to 5
i bind 0
flag bind 1
sniff i <= 5 : sniff flag == 0 : dive
flag bind 0
sniff flag == 0 : roar i
sniff flag == 0 : i bind i + 1
flag bind 1
sniff i <= 5 : sniff flag == 1 : soar
```

- `bind` — assign variable  
- `roar` — print  
- `sniff … : action` — conditional (inline or block)  
- `dive` / `soar` — set execution direction forward / reverse  
- No loop keyword — direction reversal + flag guards make loops

**→ See [GUIDE.md](GUIDE.md) for the full walkthrough.**

---

## ⚡ Execution Model

A global `DIRECTION` (`1` or `-1`) steps through lines. `soar` reverses it; `dive` restores forward. When direction goes past the first or last line, the program ends. Block `sniff/check` enters at the first (forward) or last (reverse) line of the block.

---

## 🎮 Test Cases & Projects

```powershell
# Test cases (pip-installed cmra)
cmra "test cases\test.cmra"
cmra "test cases\test_strings.cmra"
cmra "test cases\test_arith.cmra"

# Projects
cmra projects\calculator.cmra
cmra projects\countdown.cmra
cmra projects\fizzbuzz.cmra
cmra projects\story_adventure.cmra
```

**Test cases** live in `test cases/` (`.cmra`) and `test cases cmrash/` (`.cmrash`).  
**Projects** live in `projects/`: calculator, countdown, fizzbuzz, story_adventure.

---

## 📦 File Inventory

| Path | Purpose |
|------|---------|
| `src/cmra/` | Installable Python package |
| `src/cmra/cli.py` | Entry point for the `cmra` command |
| `src/cmra/fire.py` | Fire Dragon interpreter |
| `src/cmra/shadow.py` | Shadow Dragon interpreter |
| `src/cmra/runner.py` | Shared dispatch logic |
| `cmra.py` | Legacy Fire Dragon single-file |
| `cmrash.py` | Legacy Shadow Dragon single-file |
| `prototype.py` | Original workshop prototype |
| `cmra.ps1` / `cmra.bat` | No-install launchers |
| `pyproject.toml` | Package metadata (pip install) |
| `index.html` + `styles.css` | Static docs site |
| `playground.html` | Browser REPL (Pyodide) |
| `GUIDE.md` | Full user guide |
| `keybind.txt` | Fire ↔ Shadow keyword cheatsheet |
| `projects/` | Showcase programs |
| `test cases/` | Regression tests (`.cmra`) |
| `test cases cmrash/` | Regression tests (`.cmrash`) |

---

## 📜 License

CMRA is a learning project. Use freely, learn deeply, code fiercely! 🔥

---

**May your code burn bright and your loops reverse true!** 🐉🔥
