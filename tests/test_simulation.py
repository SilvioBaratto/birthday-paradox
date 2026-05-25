"""Unit tests for MonteCarloSimulator convergence."""

from __future__ import annotations

import math

import numpy as np
import pytest

from birthday.core.config import BirthdayConfig
from birthday.math.probability import BirthdayProbability
from birthday.simulation.monte_carlo import MonteCarloSimulator


class TestConvergence:
    """Empirical probability converges to exact within 4σ."""

    @pytest.fixture
    def config(self) -> BirthdayConfig:
        return BirthdayConfig(days_per_year=365)

    @pytest.mark.parametrize(
        "n", [23, 50, 70]
    )
    def test_empirical_within_4_sigma(self, config: BirthdayConfig, n: int) -> None:
        trials = 20_000
        seed = 42
        prob = BirthdayProbability(config)
        exact = prob.prob_match_exact(n)
        sigma = math.sqrt(exact * (1 - exact) / trials)

        sim = MonteCarloSimulator(config, seed=seed)
        result = sim.simulate_group(n, trials)
        empirical = result.empirical_probability

        assert abs(empirical - exact) <= 4 * sigma, (
            f"n={n}: |{empirical:.6f} - {exact:.6f}| = {abs(empirical - exact):.6f} "
            f"> 4σ = {4 * sigma:.6f}"
        )


class TestResultStructure:
    """simulate_group returns correct SimulationResult."""

    def test_result_has_correct_group_size_and_trials(self) -> None:
        config = BirthdayConfig()
        sim = MonteCarloSimulator(config, seed=42)
        result = sim.simulate_group(23, 1_000)
        assert result.group_size == 23
        assert result.n_trials == 1_000


class TestSimulateCurve:
    """simulate_curve returns empirical probabilities for each group size."""

    def test_returns_array_of_same_length(self) -> None:
        config = BirthdayConfig()
        sim = MonteCarloSimulator(config, seed=42)
        group_sizes = np.array([5, 10, 23])
        result = sim.simulate_curve(group_sizes, n_trials=1_000)
        assert len(result) == len(group_sizes)

    def test_values_between_zero_and_one(self) -> None:
        config = BirthdayConfig()
        sim = MonteCarloSimulator(config, seed=42)
        group_sizes = np.array([5, 10, 23])
        result = sim.simulate_curve(group_sizes, n_trials=1_000)
        for val in result:
            assert 0.0 <= val <= 1.0


class TestFirstCollisionDistribution:
    """simulate_first_collision_distribution returns array of length n_trials."""

    def test_returns_array_of_length_n_trials(self) -> None:
        config = BirthdayConfig()
        sim = MonteCarloSimulator(config, seed=42)
        result = sim.simulate_first_collision_distribution(max_people=30, n_trials=1_000)
        assert len(result) == 1_000

    def test_values_are_non_negative(self) -> None:
        config = BirthdayConfig()
        sim = MonteCarloSimulator(config, seed=42)
        result = sim.simulate_first_collision_distribution(max_people=30, n_trials=1_000)
        assert all(v >= 0 for v in result)


class TestInvalidInputs:
    """simulate_group raises ValueError on invalid arguments."""

    def test_group_size_less_than_one_raises(self) -> None:
        config = BirthdayConfig()
        sim = MonteCarloSimulator(config, seed=42)
        with pytest.raises(ValueError):
            sim.simulate_group(0, 1_000)

    def test_n_trials_less_than_one_raises(self) -> None:
        config = BirthdayConfig()
        sim = MonteCarloSimulator(config, seed=42)
        with pytest.raises(ValueError):
            sim.simulate_group(23, 0)

    def test_simulate_curve_n_trials_less_than_one_raises(self) -> None:
        config = BirthdayConfig()
        sim = MonteCarloSimulator(config, seed=42)
        with pytest.raises(ValueError):
            sim.simulate_curve(np.array([5, 10]), n_trials=0)
