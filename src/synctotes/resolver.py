"""Deterministic snippet → PD-page resolver.

Given a highlight snippet (any source) and the extracted text of the
canonical PD edition (a mapping ``{page: text}``), the resolver returns a
:class:`synctotes.types.MatchResult` capturing whether the snippet maps to a
single page, multiple candidates, or none.

Algorithm: :func:`rapidfuzz.fuzz.partial_ratio` (best substring alignment)
applied page-by-page after light text normalization (NFKC, smart quotes →
straight, dash unification, whitespace collapse). The page with highest
score is the candidate; status depends on absolute score and the gap to the
runner-up.

LLM-fallback (ADR-002) attaches as a decorator over this same interface
without touching call sites — the ``status='ambiguous'`` and
``status='no_match'`` branches are the explicit extension hooks.
"""

from __future__ import annotations

import re
import unicodedata
from functools import lru_cache
from typing import Final

from rapidfuzz import fuzz

from synctotes.types import Candidate, MatchResult

# Provisional thresholds. Empirical recalibration tracked in issue #5
# (≥85% rigorous match-rate target for Quincas Borba fixture).
DEFAULT_MIN_SCORE: Final[float] = 80.0
DEFAULT_AMBIGUITY_MARGIN: Final[float] = 5.0
_TOP_K_CANDIDATES: Final[int] = 3
_EXCERPT_LENGTH: Final[int] = 120
_NORMALIZE_CACHE_SIZE: Final[int] = 512

# Typographical normalization map: codepoints that vary between Kindle/Amazon
# exports and PDF text-extraction, but are semantically equivalent.
_REPLACEMENTS: Final[dict[str, str]] = {
    "“": '"',  # LEFT DOUBLE QUOTATION MARK
    "”": '"',  # RIGHT DOUBLE QUOTATION MARK
    "‘": "'",  # LEFT SINGLE QUOTATION MARK  # noqa: RUF001
    "’": "'",  # RIGHT SINGLE QUOTATION MARK  # noqa: RUF001
    "—": "-",  # EM DASH
    "–": "-",  # EN DASH  # noqa: RUF001
    "…": "...",  # HORIZONTAL ELLIPSIS
    " ": " ",  # NO-BREAK SPACE  # noqa: RUF001
}


def resolve_to_pd_page(
    snippet: str,
    pd_pages: dict[int, str],
    *,
    min_score: float = DEFAULT_MIN_SCORE,
    ambiguity_margin: float = DEFAULT_AMBIGUITY_MARGIN,
) -> MatchResult:
    """Resolve a highlight snippet to a page in the canonical PD edition.

    Returns:
        ``status='found'`` — top-1 score ≥ ``min_score`` AND gap to top-2
        is ≥ ``ambiguity_margin``.

        ``status='ambiguous'`` — top-1 score ≥ ``min_score`` but gap to
        top-2 is < ``ambiguity_margin``. ``candidates`` lists the top-3.

        ``status='no_match'`` — top-1 score < ``min_score``. ``candidates``
        still lists the top-3 for diagnostic logging.
    """
    normalized_snippet = _normalize(snippet)
    if not normalized_snippet or not pd_pages:
        return MatchResult(status="no_match")

    scored = _score_pages(normalized_snippet, pd_pages)
    if not scored:
        return MatchResult(status="no_match")

    scored.sort(key=lambda c: c.score, reverse=True)
    top = scored[0]
    candidates = tuple(scored[:_TOP_K_CANDIDATES])

    if top.score < min_score:
        return MatchResult(status="no_match", candidates=candidates)

    second_score = scored[1].score if len(scored) > 1 else 0.0
    if (top.score - second_score) < ambiguity_margin:
        return MatchResult(
            status="ambiguous",
            page=top.page,
            confidence=top.score,
            candidates=candidates,
        )

    return MatchResult(
        status="found",
        page=top.page,
        confidence=top.score,
        candidates=candidates,
    )


def _score_pages(normalized_snippet: str, pd_pages: dict[int, str]) -> list[Candidate]:
    """Compute a Candidate per non-empty page, sorted later by caller."""
    out: list[Candidate] = []
    for page, raw_text in pd_pages.items():
        normalized = _normalize(raw_text)
        if not normalized:
            continue
        score = fuzz.partial_ratio(normalized_snippet, normalized)
        out.append(
            Candidate(
                page=page,
                score=float(score),
                excerpt=_excerpt(normalized),
            )
        )
    return out


@lru_cache(maxsize=_NORMALIZE_CACHE_SIZE)
def _normalize(text: str) -> str:
    """NFKC + smart-quote/dash unification + whitespace collapse.

    Cached because the same page text is re-normalized once per highlight
    when a caller resolves many snippets against the same `pd_pages` dict.
    """
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKC", text)
    for src, dst in _REPLACEMENTS.items():
        normalized = normalized.replace(src, dst)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _excerpt(normalized_text: str, length: int = _EXCERPT_LENGTH) -> str:
    """Short prefix of an already-normalized page for diagnostic display."""
    if len(normalized_text) <= length:
        return normalized_text
    return normalized_text[:length].rstrip() + "…"
