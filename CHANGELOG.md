# CHANGELOG

All notable changes to CMRA are documented here.

---

## [Unreleased] — 2026-04-12

### 🆕 New Ways to Run CMRA

The project grew beyond two standalone scripts. You can now run CMRA in four different ways:

#### 1. `pip install` + `cmra` CLI *(recommended)*
```powershell
pip install -e .          # inside your venv
cmra myprogram.cmra
cmra run script.cmra --debug
cmra repl --mode shadow
```
The `cmra` command is registered via `pyproject.toml → [project.scripts]`.

#### 2. PowerShell wrapper — `cmra.ps1`
No install required. Auto-selects venv Python or falls back to system Python:
```powershell
.\cmra.ps1 myprogram.cmra
# Add to PATH so bare `cmra` works:
$env:PATH = "C:\path\to\CMRA;$env:PATH"
cmra myprogram.cmra
```

#### 3. BAT wrapper — `cmra.bat`
Same auto-detect logic for CMD / legacy shells:
```bat
cmra.bat myprogram.cmra
```

#### 4. Python module directly
```powershell
python -m cmra.cli myprogram.cmra
```

#### Build a standalone `.exe`
```powershell
.\build.bat              # PyInstaller → dist\cmra.exe
dist\cmra.exe myprogram.cmra
```

---

### 📦 Package Restructure (`src/cmra/`)

| File | Description |
|------|-------------|
| `src/cmra/__init__.py` | Package init, version `0.1.0` |
| `src/cmra/fire.py` | Fire Dragon interpreter — class-based, replaces global state in `cmra.py` |
| `src/cmra/shadow.py` | Shadow Dragon interpreter — class-based, `.cmrash` extension |
| `src/cmra/runner.py` | Dispatches to correct interpreter by file extension |
| `src/cmra/repl.py` | Interactive REPL with persistent variable state |
| `src/cmra/cli.py` | Entry point: `cmra <file>`, `cmra run <file>`, `cmra repl` |
| `pyproject.toml` | Package metadata and `cmra` script entry point |
| `setup.py` | pip 21.x compatibility shim |
| `build.bat` | PyInstaller build helper → `dist\cmra.exe` |

> **Original `cmra.py` and `cmra_simplified.py` are untouched** — they still work as before.

---

### 📖 Documentation

| File | What changed |
|------|-------------|
| `guide.html` | **New** — standalone User Guide (dark theme): installation, syntax, direction model, loops, pitfalls, examples, extending |
| `GUIDE.md` | **New** — markdown version of the User Guide |
| `README.md` | Full rewrite — pip install as Option 1, wrappers as Option 2, links to guide |
| `index.html` | Updated Quick Start section with all 3 run options; added **📖 User Guide** nav link |
| `playground.html` | Added "run locally" note in header |
| `.gitignore` | Expanded — covers `__pycache__`, `*.egg-info`, `dist/`, `build/`, IDE files, OS noise |

---

### Key Design Decisions

- **Class-based interpreters** — each interpreter run is isolated (no global state leakage between files)
- **`.cmrash` extension** — new canonical extension for Shadow Dragon (`.cmrasim` still works)
- **Wrappers auto-detect venv** — `cmra.ps1` and `cmra.bat` check for `venv\Scripts\python.exe` first, so they work with or without activation
- **Original scripts untouched** — `cmra.py` and `cmra_simplified.py` remain for backwards compatibility
