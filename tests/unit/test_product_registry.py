"""Tests for `util.product_registry`. Loads the real products.yaml so this
file doubles as a smoke test that the YAML is shaped as expected."""
from __future__ import annotations

import pytest

from util import product_registry


@pytest.fixture(autouse=True)
def _reset_registry():
    product_registry._REGISTRY = None  # type: ignore[attr-defined]
    yield
    product_registry._REGISTRY = None  # type: ignore[attr-defined]


class TestGetProduct:
    def test_returns_record_for_known_id(self) -> None:
        rec = product_registry.get_product("reptwin")
        assert rec is not None
        assert rec["id"] == "reptwin"
        assert rec["name"] == "RepTwin"

    def test_returns_none_for_unknown_id(self) -> None:
        assert product_registry.get_product("not_a_product") is None


class TestGetName:
    def test_known(self) -> None:
        assert product_registry.get_name("reptwin") == "RepTwin"
        assert product_registry.get_name("pod") == "Point-of-Dispense (POD)"

    def test_unknown(self) -> None:
        assert product_registry.get_name("not_a_product") is None


class TestGetOneLine:
    def test_known(self) -> None:
        line = product_registry.get_one_line("reptwin")
        assert isinstance(line, str)
        assert len(line) > 20  # actual one-liner, not empty


class TestGetConfirmedClaims:
    def test_known(self) -> None:
        claims = product_registry.get_confirmed_claims("reptwin")
        assert isinstance(claims, list)
        assert len(claims) > 0  # RepTwin has confirmed claims in the YAML
        assert all(isinstance(c, str) for c in claims)

    def test_unknown_returns_empty(self) -> None:
        assert product_registry.get_confirmed_claims("not_a_product") == []


class TestAllProductIds:
    def test_returns_known_ids(self) -> None:
        ids = product_registry.all_product_ids()
        assert "reptwin" in ids
        assert "marketplace" in ids
        # Sprint 8: 14 active products (16 master PRD entries minus AQS and CIS,
        # which Sherry pulled from the active set).
        assert len(ids) == 14
        # The two removed products MUST NOT come back without an explicit decision.
        assert "aqs" not in ids
        assert "cis" not in ids
