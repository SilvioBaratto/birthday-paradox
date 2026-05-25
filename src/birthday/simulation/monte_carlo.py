"""Monte Carlo simulation of the Birthday Paradox."""

from __future__ import annotations

import logging

import numpy as np
from numpy.typing import NDArray

from birthday.core.config import BirthdayConfig
from birthday.core.models import SimulationResult

logger = logging.getLogger(__name__)


class MonteCarloSimulator:
    """
    Vectorized Monte Carlo simulator for the Birthday Paradox.

    For each trial we draw `group_size` uniform integers in [0, D) and check
    whether any value repeats. We also record the index of the first colliding
    person so we can visualise how collisions accumulate as the room fills.
    """

    __slots__ = ("_config", "_seed", "_rng")

    def __init__(self, config: BirthdayConfig, seed: int | None = None) -> None:
        self._config = config
        self._seed = seed
        self._rng = np.random.default_rng(seed)

    @property
    def config(self) -> BirthdayConfig:
        return self._config

    @property
    def seed(self) -> int | None:
        return self._seed

    def reset_seed(self, seed: int | None = None) -> None:
        self._seed = seed
        self._rng = np.random.default_rng(seed)

    def simulate_group(self, group_size: int, n_trials: int) -> SimulationResult:
        """
        Run `n_trials` independent rooms of `group_size` people.

        Returns a SimulationResult with collision counts and per-trial index
        of first collision (0 if no collision occurred).
        """
        if group_size < 1:
            raise ValueError("group_size must be >= 1")
        if n_trials < 1:
            raise ValueError("n_trials must be >= 1")

        days = self._config.days_per_year
        draws = self._rng.integers(0, days, size=(n_trials, group_size))

        # For each trial: find earliest index whose value has appeared before.
        collision_idx = np.zeros(n_trials, dtype=np.int_)
        n_collisions = 0
        for t in range(n_trials):
            seen: dict[int, int] = {}
            for i, val in enumerate(draws[t], start=1):
                v = int(val)
                if v in seen:
                    collision_idx[t] = i
                    n_collisions += 1
                    break
                seen[v] = i

        return SimulationResult(
            group_size=group_size,
            n_trials=n_trials,
            n_collisions=n_collisions,
            collision_indices=collision_idx,
        )

    def simulate_curve(
        self, group_sizes: NDArray[np.int_], n_trials: int
    ) -> NDArray[np.float64]:
        """
        Empirical P(match) for each group size.

        Optimised via a single big batch of size `max(group_sizes)` reused
        across all sizes — we just check the prefix for collisions.
        """
        if n_trials < 1:
            raise ValueError("n_trials must be >= 1")

        days = self._config.days_per_year
        max_n = int(group_sizes.max())
        draws = self._rng.integers(0, days, size=(n_trials, max_n))

        empirical = np.zeros(len(group_sizes), dtype=np.float64)
        for i, n in enumerate(group_sizes):
            n_int = int(n)
            if n_int < 2:
                empirical[i] = 0.0
                continue
            # Vectorised: per-row, count uniques in first n columns
            prefix = draws[:, :n_int]
            # Sort each row, check adjacent equality
            srt = np.sort(prefix, axis=1)
            has_dup = (np.diff(srt, axis=1) == 0).any(axis=1)
            empirical[i] = float(has_dup.mean())
            logger.debug(f"n={n_int}: empirical P={empirical[i]:.4f}")
        return empirical

    def simulate_first_collision_distribution(
        self, max_people: int, n_trials: int
    ) -> NDArray[np.int_]:
        """
        Distribution of the index at which the first collision appears.

        Returns array of length `n_trials`; 0 means "no collision within
        max_people" (rare for max_people >> sqrt(D)).
        """
        days = self._config.days_per_year
        draws = self._rng.integers(0, days, size=(n_trials, max_people))
        first_idx = np.zeros(n_trials, dtype=np.int_)
        for t in range(n_trials):
            seen = np.zeros(days, dtype=bool)
            for i in range(max_people):
                v = int(draws[t, i])
                if seen[v]:
                    first_idx[t] = i + 1
                    break
                seen[v] = True
        return first_idx
