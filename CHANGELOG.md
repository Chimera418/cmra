# CHANGELOG

All notable changes to CMRA are documented here.

---

## [Unreleased]

## [1.1.1] — 2026-04-27

### Runtime (PyPI)

- Added package entrypoint [src/cmra/__main__.py](src/cmra/__main__.py) so `python -m cmra` works out of the box.
- Bumped Python package version to **0.1.2**.

### Windows CLI

- Fixed [cmra.bat](cmra.bat) launcher flow so it resolves and runs the package CLI reliably on Windows.

### Documentation

- Synced command guidance across [README.md](README.md), [GUIDE.md](GUIDE.md), [guide.html](guide.html), and [index.html](index.html) to consistently prefer `python -m cmra`.

### VS Code Extension

- Updated extension default command to `python -m cmra`.
- Bumped extension version to **1.1.1** for VS Code Marketplace and OpenVSX publishing.

## [1.1.0] — 2026-04-14

### 🛠️ Extension Updates

- **Run command reliability**: VS Code extension now defaults to `python -m cmra "<file>"`.
- **Config support**: Added/standardized `cmra.executablePath` with default `python -m cmra` for custom interpreter/command overrides.
- **Diagnostics improvements**:
	- Added randomized themed message variants for Fire Dragon (`.cmra`) diagnostics.
	- Added clear technical variants for Shadow Dragon (`.cmrash`) diagnostics using `=` guidance.
	- Fixed false positives so legal comparisons like `==` are not flagged as invalid assignment in `.cmra` conditions.
- **Docs sync**:
	- Extension README now includes inline diagnostics catalog for marketplace viewers.
	- Added `cmra-vscode-extension/ERROR_MESSAGES.md` as canonical message catalog.
	- Added `idk/update_checklist.md` to track required doc/release updates per change type.

### 🚀 VS Code Extension Released (v1.0.2)

The **CMRA Esoteric Language** extension is now officially live on the VS Code Marketplace and Open VSX Registry! 
- Provides accurate syntax highlighting for both Fire Dragon (`.cmra`) and Shadow Dragon (`.cmrash`) dialects.
- Seamlessly run your dragon code locally directly from the editor (requires `pip install cmra`).
- Includes fast snippets for bootstrapping loop and conditional patterns.

---

### 🆕 New Ways to Run CMRA

The project grew beyond two standalone scripts. You can now run CMRA in four different ways:

#### 1. `pip install` + `cmra` CLI *(recommended)*
```powershell
pip install cmra          # from PyPI

# development install (optional)
pip install -e .          # inside your venv
cmra myprogram.cmra
cmra run script.cmra --debug
cmra repl --mode shadow
cmrash myprogram.cmrash
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
python -m cmra myprogram.cmra
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

> **Standalone scripts remain available:** `cmra.py` (Fire) and `cmrash.py` (Shadow).

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
- **`.cmrash` extension** — canonical extension for Shadow Dragon
- **Wrappers auto-detect venv** — `cmra.ps1` and `cmra.bat` check for `venv\Scripts\python.exe` first, so they work with or without activation
- **Standalone scripts available** — `cmra.py` and `cmrash.py` remain for direct execution workflows
