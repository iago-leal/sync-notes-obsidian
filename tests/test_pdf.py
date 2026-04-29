"""Tests for :mod:`synctotes.pdf`."""

from __future__ import annotations

from pathlib import Path

from synctotes.pdf import extract_pages


def test_extract_pages_returns_one_indexed_dict(sample_pdf_path: Path) -> None:
    pages = extract_pages(sample_pdf_path)
    assert min(pages) == 1
    assert max(pages) == 3
    assert len(pages) == 3


def test_extract_pages_returns_text_per_page(sample_pdf_path: Path) -> None:
    pages = extract_pages(sample_pdf_path)
    assert "Lorem ipsum" in pages[1]
    assert "tempor incididunt" in pages[2]
    assert "minim veniam" in pages[3]


def test_extract_pages_accepts_string_path(sample_pdf_path: Path) -> None:
    pages = extract_pages(str(sample_pdf_path))
    assert len(pages) == 3
