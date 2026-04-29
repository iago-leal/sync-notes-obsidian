"""Smoke tests — validate that the package skeleton imports correctly.

These exist so the test suite collects something at project-setup time.
Real coverage lands in F6.a as each module is implemented.
"""

from __future__ import annotations

from typing import get_args

import synctotes
from synctotes import types


def test_package_has_version() -> None:
    assert synctotes.__version__


def test_match_result_contract_is_exposed() -> None:
    """The MatchResult type contract is the public resolver interface (guardrail #1)."""
    assert types.MatchResult is not None
    assert types.Candidate is not None
    statuses = set(get_args(types.MatchStatus))
    assert {"found", "ambiguous", "no_match"} <= statuses


def test_match_result_default_construction() -> None:
    result = types.MatchResult(status="no_match")
    assert result.page is None
    assert result.confidence is None
    assert result.candidates == ()
