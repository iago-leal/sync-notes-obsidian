"""Parser for Kindle ``My Clippings.txt`` and the deterministic loc->page resolver.

Implementation lands in F6.a. The public API will return
:class:`synctotes.types.MatchResult` from the resolver — see ARCHITECTURE.md
guardrail #1.
"""

from __future__ import annotations
