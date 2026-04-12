# 🐉 CMRA Language (Chimera)

> **"Where code breathes fire and flows like flame..."**

**CMRA** (Chimera) is an esoteric programming language exploring reversible execution and direction control through a dragon-inspired syntax. Programs can soar *up* or dive *down* through code at runtime.

🔥 **GitHub:** [TeapotChimera418/cmra](https://github.com/TeapotChimera418/cmra)  
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
[GitHub (@TeapotChimera418)](https://github.com/TeapotChimera418) or Discord [`gamingchimera`](https://discord.com/users/736465046317563915).

## ✨ Try it Online

**🔥 [Launch the Interactive Playground](https://cmra-esolang.vercel.app/playground.html)**

Write and run CMRA code directly in your browser — no installation needed. Powered by Pyodide.

---

## ⚡ Installation & Quick Start

### pip install (recommended)

```powershell
# From the project root with your venv active:
pip install -e .

# Now use `cmra` from anywhere inside the venv:
cmra "test cases\test.cmra"
```

### No-install PowerShell wrapper

```powershell
.\cmra.ps1 "test cases\test.cmra"
```

### Run with Python directly

```powershell
python -m cmra.cli "test cases\test.cmra"
python cmra.py "test cases cmra\test.cmra"          # legacy single-file
python cmra_simplified.py "test cases cmra_simplified\test.cmrasim"
```

---

## 🔱 The Twin Dragons

| Dragon | Entry point | Keywords |
|--------|-------------|----------|
| 🐲 **Fire Dragon** | `cmra.py` / `src/cmra/fire.py` | `bind` `roar` `sniff` `dive` `soar` `murmur` |
| 🌑 **Shadow Dragon** | `cmra_simplified.py` / `src/cmra/shadow.py` | `=` `print` `check` `reverse` `;` |
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

**Test cases** live in `test cases/` (`.cmra`) and `test cases cmra_simplified/` (`.cmrasim`).  
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
| `cmra_simplified.py` | Legacy Shadow Dragon single-file |
| `prototype.py` | Original workshop prototype |
| `cmra.ps1` / `cmra.bat` | No-install launchers |
| `pyproject.toml` | Package metadata (pip install) |
| `index.html` + `styles.css` | Static docs site |
| `playground.html` | Browser REPL (Pyodide) |
| `GUIDE.md` | Full user guide |
| `keybind.txt` | Fire ↔ Shadow keyword cheatsheet |
| `projects/` | Showcase programs |
| `test cases/` | Regression tests (`.cmra`) |
| `test cases cmra_simplified/` | Regression tests (`.cmrasim`) |

---

## 📜 License

CMRA is a learning project. Use freely, learn deeply, code fiercely! 🔥

---

**May your code burn bright and your loops reverse true!** 🐉🔥
