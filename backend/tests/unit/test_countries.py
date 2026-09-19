import pytest

from app.domain.countries import COUNTRIES, currency_for, to_usd


def test_currency_is_derived_from_country():
    assert currency_for("IN") == "INR"
    assert currency_for("DE") == "EUR"
    assert currency_for("US") == "USD"


def test_unknown_country_is_rejected():
    with pytest.raises(ValueError, match="Unsupported country"):
        currency_for("ZZ")


def test_usd_converts_to_itself():
    assert to_usd(100_000, "USD") == 100_000


def test_conversion_uses_static_rate_and_rounds_to_int():
    # 1 INR = 0.012 USD in the static table
    assert to_usd(1_000_000, "INR") == 12_000


def test_every_country_has_a_known_currency_rate():
    for code in COUNTRIES:
        assert to_usd(1, currency_for(code)) >= 0
