"""Pure statistics helpers. No I/O, no framework imports: trivially unit-testable."""

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class SalaryStats:
    count: int
    total: int
    min: int
    max: int
    avg: float
    median: float


@dataclass(frozen=True)
class Bucket:
    start: int
    end: int
    count: int


def median(values: Sequence[int]) -> float:
    if not values:
        raise ValueError("median() of empty sequence")
    ordered = sorted(values)
    mid, odd = divmod(len(ordered), 2)
    return float(ordered[mid]) if odd else (ordered[mid - 1] + ordered[mid]) / 2


def summarize(values: Sequence[int]) -> SalaryStats:
    if not values:
        return SalaryStats(count=0, total=0, min=0, max=0, avg=0, median=0)
    total = sum(values)
    return SalaryStats(
        count=len(values),
        total=total,
        min=min(values),
        max=max(values),
        avg=round(total / len(values), 2),
        median=median(values),
    )


def histogram(values: Sequence[int], bucket_count: int) -> list[Bucket]:
    """Equal-width buckets over [min, max]; the top edge belongs to the last bucket."""
    if not values:
        return []
    lo, hi = min(values), max(values)
    if lo == hi:
        return [Bucket(lo, hi, len(values))]
    width = (hi - lo) / bucket_count
    counts = [0] * bucket_count
    for v in values:
        counts[min(int((v - lo) / width), bucket_count - 1)] += 1
    return [
        Bucket(round(lo + i * width), round(lo + (i + 1) * width), c) for i, c in enumerate(counts)
    ]
