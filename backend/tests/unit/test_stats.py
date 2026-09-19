import pytest

from app.domain.stats import SalaryStats, histogram, median, summarize


def test_median_of_odd_count():
    assert median([3, 1, 2]) == 2


def test_median_of_even_count_is_mean_of_middle_pair():
    assert median([1, 2, 3, 4]) == 2.5


def test_median_of_empty_raises():
    with pytest.raises(ValueError):
        median([])


def test_summarize_empty_returns_zeroed_stats():
    assert summarize([]) == SalaryStats(count=0, total=0, min=0, max=0, avg=0, median=0)


def test_summarize_computes_all_fields():
    stats = summarize([100, 200, 300, 400])
    assert stats == SalaryStats(count=4, total=1000, min=100, max=400, avg=250, median=250)


def test_histogram_buckets_values_and_includes_upper_edge():
    buckets = histogram([0, 5, 10, 15, 20], bucket_count=2)
    assert [(b.start, b.end, b.count) for b in buckets] == [(0, 10, 2), (10, 20, 3)]


def test_histogram_of_identical_values_is_single_bucket():
    buckets = histogram([7, 7, 7], bucket_count=5)
    assert len(buckets) == 1 and buckets[0].count == 3


def test_histogram_of_empty_is_empty():
    assert histogram([], bucket_count=5) == []


def test_histogram_counts_sum_to_input_size():
    values = list(range(1000))
    assert sum(b.count for b in histogram(values, bucket_count=7)) == 1000
