"""Entry point for the synctotes CLI.

Wired in F6 of the MDCU lifecycle. For now, ``synctotes`` runs and reports
that the pipeline is not yet implemented, exiting with status 0 so the entry
point is verified end-to-end during project-setup.
"""

from __future__ import annotations

import sys

from synctotes import __version__


def main() -> int:
    """Run the synctotes CLI."""
    print(f"synctotes {__version__} — pipeline not yet implemented.")
    print("See ARCHITECTURE.md and _mdcu.md (F6 plan) for the build path.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
