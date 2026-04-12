"""
repl.py — Interactive REPL for CMRA

Usage:
    cmra repl              (defaults to Fire Dragon)
    cmra repl --mode fire
    cmra repl --mode shadow
"""

from cmra.fire import FireInterpreter
from cmra.shadow import ShadowInterpreter

DRAGON_NAMES = {
    "fire":   "Fire Dragon   (.cmra syntax)",
    "shadow": "Shadow Dragon (.cmrash syntax)",
}

PROMPTS = {
    "fire":   "fire> ",
    "shadow": "shadow> ",
}


def start_repl(mode: str = "fire") -> None:
    """Start an interactive REPL session.

    The interpreter instance persists across lines, so variables
    set in one line are accessible in the next.
    """
    mode = mode.lower()
    if mode not in ("fire", "shadow"):
        raise ValueError(f"Unknown mode '{mode}'. Choose 'fire' or 'shadow'.")

    interpreter = FireInterpreter() if mode == "fire" else ShadowInterpreter()
    prompt = PROMPTS[mode]

    print(f"CMRA REPL — {DRAGON_NAMES[mode]}")
    print("Type 'exit' or 'quit' to leave, Ctrl-C to abort.\n")

    while True:
        try:
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        stripped = line.strip()
        if stripped in ("exit", "quit"):
            print("Bye!")
            break
        if not stripped:
            continue

        try:
            interpreter.run_source(stripped)
        except KeyError as e:
            print(f"  Error: undefined variable {e}")
        except Exception as e:
            print(f"  Error: {e}")
