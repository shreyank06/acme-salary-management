"""Country catalogue and static FX table.

Design note: FX rates are a *static, versioned* table on purpose. Org-wide
figures must be reproducible and testable; live rates would make the same
report differ between two runs. Figures derived from it are approximate.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Country:
    code: str
    name: str
    currency: str


COUNTRIES: dict[str, Country] = {
    c.code: c
    for c in (
        Country("US", "United States", "USD"),
        Country("GB", "United Kingdom", "GBP"),
        Country("IN", "India", "INR"),
        Country("DE", "Germany", "EUR"),
        Country("FR", "France", "EUR"),
        Country("CA", "Canada", "CAD"),
        Country("AU", "Australia", "AUD"),
        Country("SG", "Singapore", "SGD"),
        Country("JP", "Japan", "JPY"),
        Country("BR", "Brazil", "BRL"),
    )
}

# 1 unit of currency -> USD (approximate, static).
USD_RATES: dict[str, float] = {
    "USD": 1.0,
    "GBP": 1.27,
    "INR": 0.012,
    "EUR": 1.08,
    "CAD": 0.74,
    "AUD": 0.66,
    "SGD": 0.74,
    "JPY": 0.0067,
    "BRL": 0.20,
}


def currency_for(country_code: str) -> str:
    try:
        return COUNTRIES[country_code].currency
    except KeyError:
        raise ValueError(f"Unsupported country: {country_code}") from None


def to_usd(amount: int, currency: str) -> int:
    return round(amount * USD_RATES[currency])
