"""
runner.py — File-type dispatcher for CMRA

Detects interpreter based on file extension:
  .cmra   → Fire Dragon
  .cmrash → Shadow Dragon
"""

from pathlib import Path
from cmra.fire import FireInterpreter
from cmra.shadow import ShadowInterpreter

EXTENSION_MAP = {
    ".cmra":   FireInterpreter,
    ".cmrash": ShadowInterpreter,
}


def dispatch(file_path: str, debug: bool = False) -> None:
    """Run a CMRA source file, choosing the interpreter by extension."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: '{file_path}'")

    ext = path.suffix.lower()
    interpreter_cls = EXTENSION_MAP.get(ext)

    if interpreter_cls is None:
        supported = ", ".join(EXTENSION_MAP.keys())
        raise ValueError(
            f"Unknown file type '{ext}'. Expected one of: {supported}"
        )

    if debug:
        name = "Fire Dragon" if ext == ".cmra" else "Shadow Dragon"
        print(f"[debug] Running with {name} interpreter: {path}")

    interpreter = interpreter_cls()
    interpreter.run(str(path))
