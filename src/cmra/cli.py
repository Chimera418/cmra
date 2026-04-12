"""
cli.py — Command-line entry point for CMRA

Usage:
    cmra <file>                      # auto-dispatch by extension
    cmra run <file> [--debug]        # explicit run
    cmra repl [--mode fire|shadow]   # interactive REPL
"""

import argparse
import sys
import os as _os

# ── Bootstrap: make sure `cmra` package is importable when cli.py is run
# directly (e.g. `python path/to/cli.py`) rather than via `python -m cmra.cli`
if "cmra" not in sys.modules:
    _here = _os.path.dirname(_os.path.abspath(__file__))          # …/src/cmra
    _src  = _os.path.dirname(_here)                                # …/src
    if _src not in sys.path:
        sys.path.insert(0, _src)

from cmra.runner import dispatch
from cmra.repl import start_repl


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cmra",
        description="CMRA — Creative Minimal Recursive Automaton language runtime",
    )
    subparsers = parser.add_subparsers(dest="command")

    # -- cmra run <file> --------------------------------------------------
    run_parser = subparsers.add_parser("run", help="Run a CMRA source file")
    run_parser.add_argument("file", help="Path to .cmra or .cmrash source file")
    run_parser.add_argument(
        "--debug", action="store_true", help="Print interpreter debug info"
    )

    # -- cmra repl --------------------------------------------------------
    repl_parser = subparsers.add_parser("repl", help="Start interactive REPL")
    repl_parser.add_argument(
        "--mode",
        choices=["fire", "shadow"],
        default="fire",
        help="Interpreter mode (default: fire)",
    )

    return parser


def main() -> None:
    # Allow `cmra <file>` as shorthand (no subcommand)
    if len(sys.argv) == 2 and not sys.argv[1].startswith("-") \
            and sys.argv[1] not in ("run", "repl"):
        # Treat as: cmra run <file>
        try:
            dispatch(sys.argv[1])
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        try:
            dispatch(args.file, debug=args.debug)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "repl":
        start_repl(mode=args.mode)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
