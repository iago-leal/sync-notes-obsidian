"""PDF text extraction via pdfplumber.

Used by :mod:`synctotes.kindle` to perform fuzzy text search of highlight
snippets against extracted PDF text. Page numbers are 1-indexed (matching
human convention and the link format ``[[livro.pdf#page=X]]``).
"""

from __future__ import annotations

from pathlib import Path

import pdfplumber


def extract_pages(path: Path | str) -> dict[int, str]:
    """Extract text from each page of a PDF.

    Returns a mapping of 1-indexed page number to its text content. Empty
    pages map to the empty string. The mapping is dense (every page from 1
    to N is present).
    """
    pdf_path = Path(path)
    pages: dict[int, str] = {}
    with pdfplumber.open(pdf_path) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            pages[index] = page.extract_text() or ""
    return pages
