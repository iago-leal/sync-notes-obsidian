"""Writer of Obsidian callouts into the destination vault.

Callouts always link to the canonical PDF (``[[livro.pdf#page=X]]``) — see
ARCHITECTURE.md guardrail #2. Idempotency is enforced via stable hash of
(book, normalized snippet) — see ARCHITECTURE.md guardrail #6.

Implementation lands in F6.a.
"""

from __future__ import annotations
