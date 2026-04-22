"""
Tests for JMeter results analysis and metrics calculation.
"""
import pytest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath("."))
from scripts.results_analyzer import (
    generate_sample_results,
    calculate_metrics,
)


@pytest.fixture(scope="module")
def sample_results():
    return generate_sample_results(100)


@pytest.fixture(scope="module")
def metrics(sample_results):
    return calculate_metrics(sample_results)


class TestResultsGeneration:

    def test_generates_correct_row_count(self, sample_results):
        assert len(sample_results) == 100

    def test_has_required_columns(self, sample_results):
        required = ["elapsed", "label", "responseCode",
                    "success", "bytes"]
        for col in required:
            assert col in sample_results.columns

    def test_elapsed_is_positive(self, sample_results):
        assert (sample_results["elapsed"] > 0).all()

    def test_success_is_boolean(self, sample_results):
        assert sample_results["success"].dtype == bool

    def test_error_rate_reasonable(self, sample_results):
        error_rate = (~sample_results["success"]).mean()
        assert 0 <= error_rate <= 0.10

    def test_response_codes_valid(self, sample_results):
        valid = {"200", "500", "404", "301", "302"}
        assert set(sample_results["responseCode"].unique()).issubset(valid)


class TestMetricsCalculation:

    def test_total_requests_correct(self, metrics):
        assert metrics["total_requests"] == 100

    def test_error_rate_within_range(self, metrics):
        assert 0 <= metrics["error_rate"] <= 100

    def test_avg_response_positive(self, metrics):
        assert metrics["avg_response_ms"] > 0

    def test_min_less_than_max(self, metrics):
        assert metrics["min_response_ms"] <= metrics["max_response_ms"]

    def test_p90_less_than_p95(self, metrics):
        assert metrics["p90_response_ms"] <= metrics["p95_response_ms"]

    def test_p95_less_than_max(self, metrics):
        assert metrics["p95_response_ms"] <= metrics["max_response_ms"]

    def test_throughput_positive(self, metrics):
        assert metrics["throughput_rps"] > 0

    def test_passed_plus_failed_equals_total(self, metrics):
        assert metrics["passed"] + metrics["failed"] == metrics["total_requests"]

    def test_avg_response_within_sla(self, metrics):
        assert metrics["avg_response_ms"] < 2000, \
            f"Average response {metrics['avg_response_ms']}ms exceeds 2000ms SLA"

    def test_error_rate_within_threshold(self, metrics):
        assert metrics["error_rate"] < 5.0, \
            f"Error rate {metrics['error_rate']}% exceeds 5% threshold"
