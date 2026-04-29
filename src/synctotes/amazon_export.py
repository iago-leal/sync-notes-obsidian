"""Parser for Amazon Kindle 'Caderno de anotações' export PDFs.

When the user runs 'Send notes to email' (or equivalent) in the Kindle
companion app or web reader, Amazon emails a formatted PDF containing all
highlights, bookmarks and notes for the book. This parser extracts those
entries into structured :class:`AmazonAnnotation` objects.

Each annotation may use either page-based or position-based coordinates;
the same book may have only positions if its commercial edition does not
expose page numbers (Amazon-side decision, varies per title and edition).
The :class:`AmazonAnnotation` records which coordinate system is in use so
the resolver can dispatch accordingly.

Locale: Portuguese (Brazil). English support pending real fixture.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Final, Literal

import pdfplumber

from synctotes.kindle import ClippingType

CoordinateKind = Literal["page", "position"]


@dataclass(frozen=True)
class AmazonBook:
    """Identifies the commercial Kindle edition of a book."""

    title: str
    author: str | None
    asin: str | None


@dataclass(frozen=True)
class AmazonAnnotation:
    """A single annotation parsed from an Amazon export PDF."""

    kind: ClippingType
    color: str | None
    coordinate_kind: CoordinateKind
    coordinate_value: int
    is_continuation: bool
    text: str
    note: str | None
    date_added: date | None


@dataclass(frozen=True)
class ExportedNotebook:
    """Full content of a single Amazon export PDF."""

    book: AmazonBook
    annotations: tuple[AmazonAnnotation, ...]
    summary_total: int


_ASIN_RE: Final = re.compile(r"asin=([A-Z0-9]{10})")
_TOTAL_RE: Final = re.compile(r"Anota[çc][õo]es\s*\((\d+)\)")
_METADATA_RE: Final = re.compile(
    r"^(P[áa]gina|Posi[çc][ãa]o)\s+(\d+)\s*\|\s*(.+)$",
    re.IGNORECASE,
)
_TYPE_COLOR_RE: Final = re.compile(
    r"^(Destaque|Marcador|Nota|Continua[çc][ãa]o\s+do\s+destaque)\s*(?:\(([^)]+)\))?\s*$",
    re.IGNORECASE,
)
_DATE_RE: Final = re.compile(
    r"^\s*(\d{1,2})\s+de\s+([\w]+?)\.?\s+de\s+(\d{4})\s*$",
    re.IGNORECASE | re.UNICODE,
)
_NOTE_RE: Final = re.compile(r"^Nota:\s*(.+)$")
_ROMAN_RE: Final = re.compile(r"^[IVXLCDM]+$")
_BARE_DIGIT_RE: Final = re.compile(r"^\d+$")

_MONTHS_PT: Final[dict[str, int]] = {
    "jan": 1,
    "fev": 2,
    "mar": 3,
    "abr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "set": 9,
    "out": 10,
    "nov": 11,
    "dez": 12,
    "janeiro": 1,
    "fevereiro": 2,
    "março": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,
}


def parse_export_pdf(path: Path | str) -> ExportedNotebook:
    """Parse a 'Caderno de anotações' PDF exported by Amazon Kindle."""
    pdf_path = Path(path)
    text = _extract_full_text(pdf_path)
    lines = text.split("\n")

    book, total, annotations_start = _parse_header(lines)
    annotations = _parse_annotations(lines[annotations_start:])

    return ExportedNotebook(
        book=book,
        annotations=tuple(annotations),
        summary_total=total,
    )


def _extract_full_text(path: Path) -> str:
    parts: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n".join(parts)


def _parse_header(lines: list[str]) -> tuple[AmazonBook, int, int]:
    title: str | None = None
    author: str | None = None
    asin: str | None = None
    total = 0

    for index, raw in enumerate(lines):
        line = raw.strip()
        if not line:
            continue

        if title is None:
            title = line
            continue

        if author is None and line.lower().startswith("por "):
            author = line[4:].strip()
            continue

        if asin is None:
            asin_match = _ASIN_RE.search(line)
            if asin_match:
                asin = asin_match.group(1)
                continue

        total_match = _TOTAL_RE.search(line)
        if total_match:
            total = int(total_match.group(1))
            for j in range(index + 1, len(lines)):
                if _METADATA_RE.match(lines[j].strip()):
                    return AmazonBook(title or "", author, asin), total, j
            return AmazonBook(title or "", author, asin), total, index + 1

    return AmazonBook(title or "", author, asin), total, len(lines)


def _parse_annotations(lines: list[str]) -> list[AmazonAnnotation]:
    """State-machine parser over the annotation section of the export."""
    out: list[AmazonAnnotation] = []

    cur_kind: ClippingType | None = None
    cur_color: str | None = None
    cur_coord_kind: CoordinateKind | None = None
    cur_coord_value: int | None = None
    cur_is_continuation = False
    text_lines: list[str] = []
    note_text: str | None = None
    date_added: date | None = None
    in_note_block = False

    def flush() -> None:
        nonlocal cur_kind, cur_color, cur_coord_kind, cur_coord_value
        nonlocal cur_is_continuation, text_lines, note_text, date_added, in_note_block
        if cur_kind is not None and cur_coord_kind is not None and cur_coord_value is not None:
            out.append(
                AmazonAnnotation(
                    kind=cur_kind,
                    color=cur_color,
                    coordinate_kind=cur_coord_kind,
                    coordinate_value=cur_coord_value,
                    is_continuation=cur_is_continuation,
                    text="\n".join(text_lines).strip(),
                    note=note_text,
                    date_added=date_added,
                )
            )
        cur_kind = None
        cur_color = None
        cur_coord_kind = None
        cur_coord_value = None
        cur_is_continuation = False
        text_lines = []
        note_text = None
        date_added = None
        in_note_block = False

    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            continue

        if _BARE_DIGIT_RE.match(stripped):
            continue
        if _ROMAN_RE.match(stripped):
            continue

        meta = _METADATA_RE.match(stripped)
        if meta:
            flush()
            coord_word, coord_value, type_part = meta.groups()
            type_match = _TYPE_COLOR_RE.match(type_part.strip())
            if not type_match:
                continue
            type_word, color = type_match.groups()
            type_lower = type_word.lower()

            if "continua" in type_lower:
                kind = ClippingType.HIGHLIGHT
                is_cont = True
            elif "destaque" in type_lower:
                kind = ClippingType.HIGHLIGHT
                is_cont = False
            elif "marcador" in type_lower:
                kind = ClippingType.BOOKMARK
                is_cont = False
            elif "nota" in type_lower:
                kind = ClippingType.NOTE
                is_cont = False
            else:
                continue

            coord_lower = coord_word.lower()
            ck: CoordinateKind = (
                "page" if "agina" in coord_lower or "ágina" in coord_lower else "position"
            )

            cur_kind = kind
            cur_color = color
            cur_coord_kind = ck
            cur_coord_value = int(coord_value)
            cur_is_continuation = is_cont
            in_note_block = False
            continue

        if cur_kind is None:
            continue

        note_match = _NOTE_RE.match(stripped)
        if note_match:
            note_text = note_match.group(1).strip()
            in_note_block = True
            continue

        date_match = _DATE_RE.match(stripped)
        if date_match:
            day, month_word, year = date_match.groups()
            month = _MONTHS_PT.get(month_word.lower().rstrip("."))
            if month is not None:
                parsed = date(int(year), month, int(day))
                if not in_note_block and date_added is None:
                    date_added = parsed
            continue

        if in_note_block:
            note_text = (note_text or "") + "\n" + stripped
        else:
            text_lines.append(stripped)

    flush()
    return out
