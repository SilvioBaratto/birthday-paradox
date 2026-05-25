"""Unit tests for BirthdayProbability."""

from __future__ import annotations

import pytest

from birthday.core.config import BirthdayConfig
from birthday.math.probability import BirthdayProbability


class TestKnownValues:
    """Exact probabilities against known analytical values."""

    def test_prob_23(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.prob_match_exact(23) == pytest.approx(0.507297, abs=1e-6)

    def test_prob_50(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.prob_match_exact(50) == pytest.approx(0.970374, abs=1e-6)

    def test_prob_70(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.prob_match_exact(70) == pytest.approx(0.999160, abs=1e-6)

    def test_expected_collisions_23(self) -> None:
        # C(23, 2) / 365 = 253 / 365
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.expected_collisions(23) == pytest.approx(253 / 365, abs=1e-6)


class TestMonotonicity:
    """P(match) is non-decreasing with group size."""

    def test_monotonic_1_to_100(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        for n in range(1, 100):
            p_n = prob.prob_match_exact(n)
            p_next = prob.prob_match_exact(n + 1)
            assert p_n <= p_next, f"P({n}) = {p_n:.10f} > P({n + 1}) = {p_next:.10f}"


class TestBoundaryConditions:
    """Edge cases for group sizes at D = 365."""

    def test_prob_match_exact_zero_is_zero(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.prob_match_exact(0) == 0.0

    def test_prob_match_exact_366_is_one(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.prob_match_exact(366) == 1.0

    def test_prob_no_match_exact_zero_is_one(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.prob_no_match_exact(0) == 1.0

    def test_prob_no_match_exact_366_is_zero(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.prob_no_match_exact(366) == 0.0


class TestApproximationQuality:
    """Taylor approximation stays close to exact values."""

    def test_approx_near_exact_for_small_n(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        exact = prob.prob_match_exact(23)
        approx = prob.prob_match_approx(23)
        assert abs(exact - approx) < 0.01

    def test_approx_equals_exact_at_n_1(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.prob_match_approx(1) == 0.0


class TestExpectedValues:
    """Expected-value formulas."""

    def test_expected_collisions_formula(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.expected_collisions(10) == 10 * 9 / (2 * 365)

    def test_expected_collisions_zero_for_n_lt_2(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.expected_collisions(0) == 0.0
        assert prob.expected_collisions(1) == 0.0

    def test_expected_unique_birthdays_between_1_and_n(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        for n in [1, 10, 23, 50]:
            val = prob.expected_unique_birthdays(n)
            assert val <= n
            assert val >= 0.99999999999999


class TestMedianGroupSize:
    """Median group size is the smallest n with P(match) ≥ 0.5."""

    def test_median_is_23_for_d365(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        assert prob.median_group_size() == 23

    def test_median_satisfies_half_threshold(self) -> None:
        prob = BirthdayProbability(BirthdayConfig())
        median = prob.median_group_size()
        assert prob.prob_match_exact(median) >= 0.5
        assert prob.prob_match_exact(median - 1) < 0.5

    def test_median_for_small_days(self) -> None:
        prob = BirthdayProbability(BirthdayConfig(days_per_year=5))
        median = prob.median_group_size()
        assert prob.prob_match_exact(median) >= 0.5
