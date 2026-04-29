"""Tests for :mod:`synctotes.amazon_export` against the real Quincas Borba export."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from synctotes.amazon_export import parse_export_pdf
from synctotes.kindle import ClippingType


def test_header_extracts_title_author_asin_total(
    quincas_borba_amazon_export_pdf: Path,
) -> None:
    notebook = parse_export_pdf(quincas_borba_amazon_export_pdf)
    assert notebook.book.title == "Quincas Borba"
    assert notebook.book.author == "Assis, Machado de"
    assert notebook.book.asin == "B09JWVC7X8"
    assert notebook.summary_total == 61


def test_total_annotations_match_summary(
    quincas_borba_amazon_export_pdf: Path,
) -> None:
    """Parsed items reconcile with the 'Anotações (N)' header.

    Amazon's summary counts each attached note (``Nota: ...`` line) as a
    separate item but a continuation of a highlight (``Continuação do
    destaque`` block) as part of the parent highlight (not separate). Our
    parser does the opposite: it folds attached notes into ``note`` field
    and keeps continuations as separate items. The reconciliation is:

        items_excluding_continuations + attached_notes == summary_total
    """
    notebook = parse_export_pdf(quincas_borba_amazon_export_pdf)
    items_excl_cont = sum(1 for a in notebook.annotations if not a.is_continuation)
    attached_notes = sum(1 for a in notebook.annotations if a.note is not None)
    assert items_excl_cont + attached_notes == notebook.summary_total


def test_first_annotation_matches_known_values(
    quincas_borba_amazon_export_pdf: Path,
) -> None:
    notebook = parse_export_pdf(quincas_borba_amazon_export_pdf)
    first = notebook.annotations[0]
    assert first.kind == ClippingType.HIGHLIGHT
    assert first.color == "Amarelo"
    assert first.coordinate_kind == "page"
    assert first.coordinate_value == 22
    assert first.is_continuation is False
    assert "tudo entra na mesma sensação de propriedade" in first.text
    assert first.date_added == date(2026, 4, 1)


def test_independent_note_annotation_is_captured(
    quincas_borba_amazon_export_pdf: Path,
) -> None:
    """Page 26 has a 'Página 26 | Nota' entry with text 'Viés de confirmação.'"""
    notebook = parse_export_pdf(quincas_borba_amazon_export_pdf)
    notes = [a for a in notebook.annotations if a.kind == ClippingType.NOTE]
    assert any("Viés de confirmação" in n.text for n in notes)


def test_attached_note_is_captured_under_highlight(
    quincas_borba_amazon_export_pdf: Path,
) -> None:
    """Page 29 highlight has an attached 'Nota: falsas esperanças causam...'"""
    notebook = parse_export_pdf(quincas_borba_amazon_export_pdf)
    target = next(
        a
        for a in notebook.annotations
        if a.coordinate_value == 29 and a.kind == ClippingType.HIGHLIGHT and not a.is_continuation
    )
    assert target.note is not None
    assert "falsas esperanças" in target.note


def test_continuation_is_flagged(quincas_borba_amazon_export_pdf: Path) -> None:
    """Page 37 has 'Continuação do destaque' from the previous chunk."""
    notebook = parse_export_pdf(quincas_borba_amazon_export_pdf)
    continuations = [a for a in notebook.annotations if a.is_continuation]
    assert len(continuations) >= 1
    cont = continuations[0]
    assert cont.kind == ClippingType.HIGHLIGHT
    assert cont.coordinate_kind == "page"
    assert cont.coordinate_value == 37


def test_bookmark_is_captured(quincas_borba_amazon_export_pdf: Path) -> None:
    """At least one 'Marcador (Azul)' annotation exists in the export."""
    notebook = parse_export_pdf(quincas_borba_amazon_export_pdf)
    bookmarks = [a for a in notebook.annotations if a.kind == ClippingType.BOOKMARK]
    assert len(bookmarks) >= 1
    assert bookmarks[0].color == "Azul"


def test_all_annotations_have_coordinate(
    quincas_borba_amazon_export_pdf: Path,
) -> None:
    notebook = parse_export_pdf(quincas_borba_amazon_export_pdf)
    for ann in notebook.annotations:
        assert ann.coordinate_kind in {"page", "position"}
        assert ann.coordinate_value > 0
