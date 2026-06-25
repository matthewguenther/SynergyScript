"""Enable ``python -m synergyscript ...`` as an alias for the ``synergy`` CLI."""

from synergyscript.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
