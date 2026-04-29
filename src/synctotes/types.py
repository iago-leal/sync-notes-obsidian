"""Shared types for the synctotes pipeline.

The :class:`MatchResult` and :class:`Candidate` dataclasses below are the public
interface of the loc->page resolver — see ARCHITECTURE.md guardrail #1.

LLM-fallback support will be added in v2 via decorator pattern over this same
interface (see ADR-002). Refactoring this contract later is expensive because
it touches every caller of the resolver, so it is established up front.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class Candidate:
    """A potential match for a snippet within a PDF, with location and score."""

    page: int
    score: float
    excerpt: str


MatchStatus = Literal["found", "ambiguous", "no_match"]


@dataclass(frozen=True)
class MatchResult:
    """Result of resolving a snippet to a page in a PDF.

    - ``found``: single high-confidence match; ``page`` and ``confidence`` set.
    - ``ambiguous``: multiple competing matches; ``candidates`` lists them.
    - ``no_match``: no candidate met the minimum score threshold.
    """

    status: MatchStatus
    page: int | None = None
    confidence: float | None = None
    candidates: tuple[Candidate, ...] = field(default_factory=tuple)
