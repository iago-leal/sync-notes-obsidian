"""Parser for Kindle ``My Clippings.txt`` files (PT-BR and EN locales).

Format documented by Amazon and stable across firmware versions: each
clipping is a 4-line block separated by ``==========``::

    Book Title (Author Name)
    - <type> | <location> | <date>

    <highlight text>
    ==========

The deterministic ``loc->page`` resolver also lives in this module — to be
implemented in a later commit. See ARCHITECTURE.md guardrail #1 and ADR-002
for the public interface contract (returns
:class:`synctotes.types.MatchResult`).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Final


class ClippingType(StrEnum):
    """Type of Kindle clipping."""

    HIGHLIGHT = "highlight"
    NOTE = "note"
    BOOKMARK = "bookmark"


@dataclass(frozen=True)
class KindleBook:
    """Identifies a book referenced in My Clippings.txt."""

    title: str
    author: str | None


@dataclass(frozen=True)
class KindleClipping:
    """A single highlight, note, or bookmark from a Kindle device."""

    book: KindleBook
    kind: ClippingType
    location_start: int | None
    location_end: int | None
    page: int | None
    added_at: datetime | None
    text: str


_SEPARATOR: Final[str] = "=========="

_TYPE_KEYWORDS: Final[dict[str, ClippingType]] = {
    "destaque": ClippingType.HIGHLIGHT,
    "highlight": ClippingType.HIGHLIGHT,
    "nota": ClippingType.NOTE,
    "note": ClippingType.NOTE,
    "marcador": ClippingType.BOOKMARK,
    "bookmark": ClippingType.BOOKMARK,
}

_PT_BR_MONTHS: Final[dict[str, int]] = {
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

_EN_MONTHS: Final[dict[str, int]] = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def parse_clippings(content: str) -> list[KindleClipping]:
    """Parse the full content of a My Clippings.txt file.

    Robust to UTF-8 BOM, mixed line endings (LF/CRLF), and PT-BR + EN
    locales. Malformed blocks are skipped silently — caller can compare the
    returned count to the raw block count if defect detection matters.
    """
    if content.startswith("﻿"):
        content = content[1:]
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    blocks = [block.strip() for block in content.split(_SEPARATOR)]
    clippings: list[KindleClipping] = []
    for block in blocks:
        if not block:
            continue
        parsed = _parse_block(block)
        if parsed is not None:
            clippings.append(parsed)
    return clippings


def _parse_block(block: str) -> KindleClipping | None:
    lines = block.split("\n")
    if len(lines) < 2:
        return None

    book = _parse_book_line(lines[0])
    if book is None:
        return None

    meta = _parse_metadata_line(lines[1])
    if meta is None:
        return None

    kind, loc_start, loc_end, page, added_at = meta

    text_lines = lines[2:]
    while text_lines and not text_lines[0].strip():
        text_lines.pop(0)
    text = "\n".join(text_lines).strip()

    return KindleClipping(
        book=book,
        kind=kind,
        location_start=loc_start,
        location_end=loc_end,
        page=page,
        added_at=added_at,
        text=text,
    )


def _parse_book_line(line: str) -> KindleBook | None:
    stripped = line.strip()
    if not stripped:
        return None
    match = re.match(r"^(.*?)\s*\((.+)\)\s*$", stripped)
    if match:
        return KindleBook(title=match.group(1).strip(), author=match.group(2).strip())
    return KindleBook(title=stripped, author=None)


def _parse_metadata_line(
    line: str,
) -> tuple[ClippingType, int | None, int | None, int | None, datetime | None] | None:
    """Parse the metadata line of a clipping block.

    Modern Kindle format combines type + location into a single ``|``-separated
    part (PT-BR ``"Seu destaque na posição 1234-1235"``; EN ``"Your Highlight
    on Location 100-105"``); older formats split them. We tolerate both by
    scanning every part for location/page and date independently.
    """
    stripped = line.strip()
    if not stripped.startswith("- "):
        return None
    parts = [part.strip() for part in stripped[2:].split("|")]
    if not parts:
        return None

    kind = _detect_type(parts[0])
    if kind is None:
        return None

    loc_start: int | None = None
    loc_end: int | None = None
    page: int | None = None
    added_at: datetime | None = None
    for part in parts:
        if loc_start is None and page is None:
            ls, le, p = _parse_position(part)
            if ls is not None or p is not None:
                loc_start, loc_end, page = ls, le, p
        if added_at is None:
            added_at = _parse_date(part)

    return kind, loc_start, loc_end, page, added_at


def _detect_type(part: str) -> ClippingType | None:
    lower = part.lower()
    for keyword, kind in _TYPE_KEYWORDS.items():
        if keyword in lower:
            return kind
    return None


def _parse_position(part: str) -> tuple[int | None, int | None, int | None]:
    """Parse 'na página X' / 'on page X' or 'na posição X-Y' / 'on Location X-Y'."""
    lower = part.lower()
    page_match = re.search(r"(?:p[áa]gina|page)\s+(\d+)", lower)
    if page_match:
        return (None, None, int(page_match.group(1)))
    loc_match = re.search(r"(?:posi[çc][ãa]o|location)\s+(\d+)(?:-(\d+))?", lower)
    if loc_match:
        start = int(loc_match.group(1))
        end = int(loc_match.group(2)) if loc_match.group(2) else None
        return (start, end, None)
    return (None, None, None)


def _parse_date(part: str) -> datetime | None:
    """Best-effort date parser for PT-BR ('Adicionado:') and EN ('Added on:').

    Returns ``None`` if the date does not match a known locale pattern; this
    is non-fatal because the rest of the clipping is still useful.
    """
    cleaned = part
    for prefix in ("Adicionado:", "Added on", "Added:"):
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix) :].strip()
            break

    pt_match = re.search(
        r"(\d+)\s+de\s+(\w+)\s+de\s+(\d{4})\s+(\d{1,2}):(\d{2}):(\d{2})",
        cleaned,
    )
    if pt_match:
        day, month_name, year, hour, minute, second = pt_match.groups()
        month = _PT_BR_MONTHS.get(month_name.lower())
        if month is not None:
            return datetime(int(year), month, int(day), int(hour), int(minute), int(second))

    en_match = re.search(
        r"(\w+)\s+(\d+),\s+(\d{4})\s+(\d{1,2}):(\d{2}):(\d{2})\s*(AM|PM)?",
        cleaned,
        re.IGNORECASE,
    )
    if en_match:
        month_name, day, year, hour, minute, second, ampm = en_match.groups()
        month = _EN_MONTHS.get(month_name.lower())
        if month is not None:
            h = int(hour)
            if ampm and ampm.upper() == "PM" and h != 12:
                h += 12
            elif ampm and ampm.upper() == "AM" and h == 12:
                h = 0
            return datetime(int(year), month, int(day), h, int(minute), int(second))

    return None
