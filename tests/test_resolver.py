"""Tests for :mod:`synctotes.resolver` against the Quincas Borba fixture.

These tests validate the deterministic snippet → PD-page resolver against
**real material** (Biblioteca Nacional PD edition + Amazon export with the
user's actual highlights) — exactly the scenario the project exists to
support.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from synctotes.amazon_export import parse_export_pdf
from synctotes.pdf import extract_pages
from synctotes.resolver import resolve_to_pd_page


@pytest.fixture
def quincas_borba_pd_pages(quincas_borba_pd_pdf: Path) -> dict[int, str]:
    """Extracted text per page of the PD Quincas Borba PDF."""
    return extract_pages(quincas_borba_pd_pdf)


def test_resolve_first_amazon_highlight_finds_page_in_pd(
    quincas_borba_pd_pages: dict[int, str],
    quincas_borba_amazon_export_pdf: Path,
) -> None:
    """The first highlight in the Amazon export must resolve in the PD edition.

    Snippet: 'tudo entra na mesma sensação de propriedade.' (commercial p.22).
    In the BN PD edition this phrase appears at the very start of Capítulo I,
    around page 1. The resolver should find it with high confidence.
    """
    notebook = parse_export_pdf(quincas_borba_amazon_export_pdf)
    first = notebook.annotations[0]

    result = resolve_to_pd_page(first.text, quincas_borba_pd_pages)

    assert result.status == "found"
    assert result.page is not None
    assert result.confidence is not None
    assert result.confidence >= 80.0
    assert result.page <= 5  # opening of the book


def test_resolve_returns_no_match_for_garbage_snippet(
    quincas_borba_pd_pages: dict[int, str],
) -> None:
    result = resolve_to_pd_page(
        "Lorem ipsum xyz nonexistent phrase qwerty 123",
        quincas_borba_pd_pages,
    )
    assert result.status == "no_match"
    assert result.page is None


def test_resolve_returns_no_match_for_empty_snippet(
    quincas_borba_pd_pages: dict[int, str],
) -> None:
    result = resolve_to_pd_page("", quincas_borba_pd_pages)
    assert result.status == "no_match"


def test_resolve_returns_no_match_for_empty_pages() -> None:
    result = resolve_to_pd_page("any text", {})
    assert result.status == "no_match"


def test_resolve_normalizes_smart_quotes(
    quincas_borba_pd_pages: dict[int, str],
) -> None:
    """Snippets with curly quotes still match against straight-quote PD text."""
    snippet_with_smart = "“tudo entra na mesma sensação de propriedade.”"
    result = resolve_to_pd_page(snippet_with_smart, quincas_borba_pd_pages)
    assert result.status == "found"


def test_resolve_returns_top_k_candidates_even_on_no_match(
    quincas_borba_pd_pages: dict[int, str],
) -> None:
    """Diagnostic candidates are useful even when status is no_match."""
    result = resolve_to_pd_page("xyz abc 123 unrelated string", quincas_borba_pd_pages)
    assert result.status == "no_match"
    assert len(result.candidates) > 0


def test_resolve_finds_known_continuation_segment(
    quincas_borba_pd_pages: dict[int, str],
) -> None:
    """A multi-line passage about 'campo de batatas' resolves cleanly."""
    snippet = (
        "Supõe tu um campo de batatas e duas tribos famintas. "
        "As batatas apenas chegam para alimentar uma das tribos"
    )
    result = resolve_to_pd_page(snippet, quincas_borba_pd_pages)
    assert result.status in {"found", "ambiguous"}
    assert result.page is not None


def test_quincas_borba_overall_match_rate_above_threshold(
    quincas_borba_pd_pages: dict[int, str],
    quincas_borba_amazon_export_pdf: Path,
) -> None:
    """Sanity check: most Amazon highlights resolve against PD edition.

    This is a soft form of the v0.1.0 milestone criterion (issue #5 will
    enforce ≥85% strictly). Here we accept ≥70% as a smoke threshold so
    a single threshold tuning regression doesn't flake the suite.
    """
    notebook = parse_export_pdf(quincas_borba_amazon_export_pdf)
    highlights = [
        a
        for a in notebook.annotations
        if a.kind.value == "highlight" and not a.is_continuation and a.text
    ]
    found = 0
    for ann in highlights:
        result = resolve_to_pd_page(ann.text, quincas_borba_pd_pages)
        if result.status == "found":
            found += 1

    assert highlights, "expected highlights in the export fixture"
    rate = found / len(highlights)
    assert rate >= 0.70, f"only {rate:.0%} of highlights resolved as 'found'"
