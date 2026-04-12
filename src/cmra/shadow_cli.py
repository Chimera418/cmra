"""
shadow_cli.py — Entry point for the `cmrash` command.

`cmrash <file>` is a convenience alias that always uses the Shadow Dragon
interpreter, allowing users to omit the .cmrash extension check.

Usage:
    cmrash <file.cmrash>
    cmrash repl
"""

import sys
import os as _os

# Bootstrap: allow `python shadow_cli.py` invocation without install
if "cmra" not in sys.modules:
    _here = _os.path.dirname(_os.path.abspath(__file__))
    _src = _os.path.dirname(_here)
    if _src not in sys.path:
        sys.path.insert(0, _src)

import argparse
from cmra.shadow import ShadowInterpreter
from cmra.repl import start_repl


def main() -> None:
    # Allow bare: cmrash <file>
    if len(sys.argv) == 2 and not sys.argv[1].startswith("-") \
            and sys.argv[1] != "repl":
        path = sys.argv[1]
        try:
            interp = ShadowInterpreter()
            interp.run(path)
        except FileNotFoundError:
            print(f"Error: File not found: '{path}'", file=sys.stderr)
            sys.exit(1)
        return

    parser = argparse.ArgumentParser(
        prog="cmrash",
        description="CMRA Shadow Dragon — run .cmrash files",
    )
    subparsers = parser.add_subparsers(dest="command")

    run_p = subparsers.add_parser("run", help="Run a .cmrash source file")
    run_p.add_argument("file", help="Path to .cmrash source file")

    subparsers.add_parser("repl", help="Start Shadow Dragon REPL")

    args = parser.parse_args()

    if args.command == "run":
        try:
            interp = ShadowInterpreter()
            interp.run(args.file)
        except FileNotFoundError:
            print(f"Error: File not found: '{args.file}'", file=sys.stderr)
            sys.exit(1)
    elif args.command == "repl":
        start_repl(mode="shadow")
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
