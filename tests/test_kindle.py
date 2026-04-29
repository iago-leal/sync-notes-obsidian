"""Tests for :mod:`synctotes.kindle` parser of My Clippings.txt."""

from __future__ import annotations

from datetime import datetime

from synctotes.kindle import (
    ClippingType,
    parse_clippings,
)


def test_parse_clippings_pt_br_count(sample_clippings_pt_br: str) -> None:
    clippings = parse_clippings(sample_clippings_pt_br)
    assert len(clippings) == 4


def test_parse_clippings_extracts_book_with_author(sample_clippings_pt_br: str) -> None:
    clippings = parse_clippings(sample_clippings_pt_br)
    first = clippings[0]
    assert first.book.title == "Dom Casmurro"
    assert first.book.author == "Machado de Assis"


def test_parse_clippings_extracts_book_without_author(sample_clippings_pt_br: str) -> None:
    clippings = parse_clippings(sample_clippings_pt_br)
    no_author = next(c for c in clippings if c.book.author is None)
    assert no_author.book.title == "Livro Sem Autor"


def test_parse_clippings_handles_location_range(sample_clippings_pt_br: str) -> None:
    clippings = parse_clippings(sample_clippings_pt_br)
    first = clippings[0]
    assert first.location_start == 1234
    assert first.location_end == 1235


def test_parse_clippings_handles_single_location(sample_clippings_pt_br: str) -> None:
    clippings = parse_clippings(sample_clippings_pt_br)
    second = clippings[1]
    assert second.location_start == 1300
    assert second.location_end is None


def test_parse_clippings_handles_page(sample_clippings_pt_br: str) -> None:
    clippings = parse_clippings(sample_clippings_pt_br)
    paged = next(c for c in clippings if c.page is not None)
    assert paged.page == 42


def test_parse_clippings_distinguishes_types(sample_clippings_pt_br: str) -> None:
    clippings = parse_clippings(sample_clippings_pt_br)
    types = {c.kind for c in clippings}
    assert types == {ClippingType.HIGHLIGHT, ClippingType.NOTE, ClippingType.BOOKMARK}


def test_parse_clippings_extracts_text(sample_clippings_pt_br: str) -> None:
    clippings = parse_clippings(sample_clippings_pt_br)
    assert "Capitu olhou-me em silêncio" in clippings[0].text


def test_parse_clippings_bookmark_has_empty_text(sample_clippings_pt_br: str) -> None:
    clippings = parse_clippings(sample_clippings_pt_br)
    bookmark = next(c for c in clippings if c.kind == ClippingType.BOOKMARK)
    assert bookmark.text == ""


def test_parse_clippings_strips_bom(sample_clippings_pt_br: str) -> None:
    clippings = parse_clippings(sample_clippings_pt_br)
    assert clippings[0].book.title == "Dom Casmurro"


def test_parse_clippings_parses_pt_br_date(sample_clippings_pt_br: str) -> None:
    clippings = parse_clippings(sample_clippings_pt_br)
    first = clippings[0]
    assert first.added_at == datetime(2018, 6, 1, 14, 30, 25)


def test_parse_clippings_supports_english(sample_clippings_en: str) -> None:
    clippings = parse_clippings(sample_clippings_en)
    assert len(clippings) == 1
    item = clippings[0]
    assert item.book.title == "Pride and Prejudice"
    assert item.book.author == "Jane Austen"
    assert item.kind == ClippingType.HIGHLIGHT
    assert item.location_start == 100
    assert item.location_end == 105


def test_parse_clippings_parses_en_date_with_am_pm(sample_clippings_en: str) -> None:
    clippings = parse_clippings(sample_clippings_en)
    assert clippings[0].added_at == datetime(2018, 6, 3, 9, 15, 0)


def test_parse_clippings_handles_crlf_line_endings() -> None:
    content = (
        "Livro\r\n- Seu destaque na posição 1 | Adicionado: hoje\r\n\r\ntexto\r\n==========\r\n"
    )
    clippings = parse_clippings(content)
    assert len(clippings) == 1
    assert clippings[0].location_start == 1
    assert clippings[0].text == "texto"


def test_parse_clippings_skips_malformed_blocks() -> None:
    content = (
        "Livro Bom (Autor)\n"
        "- Seu destaque na posição 1 | Adicionado: hoje\n"
        "\n"
        "ok\n"
        "==========\n"
        "linha solta sem metadata\n"
        "==========\n"
        "Outro Livro (Autor)\n"
        "- Seu destaque na posição 2 | Adicionado: hoje\n"
        "\n"
        "tambem ok\n"
        "==========\n"
    )
    clippings = parse_clippings(content)
    assert len(clippings) == 2
