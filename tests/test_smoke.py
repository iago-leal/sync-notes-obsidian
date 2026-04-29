"""Smoke tests — validate that the package skeleton imports correctly.

These exist so the test suite collects something at project-setup time.
Real coverage lands in F6.a as each module is implemented.
"""

from __future__ import annotations

import synctotes
from synctotes import types


def test_package_has_version() -> None:
    assert synctotes.__version__


def test_match_result_contract_is_exposed() -> None:
    """The MatchResult type contract is the public resolver interface (guardrail #1)."""
    assert types.MatchResult is not None
    assert types.Candidate is not None
    assert "found" in types.MatchStatus.__args__
    assert "ambiguous" in types.MatchStatus.__args__
    assert "no_match" in types.MatchStatus.__args__


def test_match_result_default_construction() -> None:
    result = types.MatchResult(status="no_match")
    assert result.page is None
    assert result.confidence is None
    assert result.candidates == ()
