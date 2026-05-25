"""Analytical probability formulas for the Birthday Paradox."""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray
from scipy.special import gammaln

from birthday.core.config import BirthdayConfig


class BirthdayProbability:
    """
    Closed-form probability calculations for the Birthday Paradox.

    Implements three views:
      1. Exact:           P(match) = 1 - D!/(D^n (D-n)!)
      2. Taylor approx:   P(match) ~= 1 - exp(-n(n-1)/(2D))
      3. Expected pairs:  E[matching pairs] = C(n,2)/D
    """

    __slots__ = ("_config",)

    def __init__(self, config: BirthdayConfig) -> None:
        self._config = config

    @property
    def config(self) -> BirthdayConfig:
        return self._config

    def prob_no_match_exact(self, n: int) -> float:
        """
        Exact P(all n birthdays distinct).

        Uses log-gamma for numerical stability:
            log P(no match) = lgamma(D+1) - lgamma(D-n+1) - n*log(D)
        """
        days = self._config.days_per_year
        if n <= 1:
            return 1.0
        if n > days:
            return 0.0
        log_p = gammaln(days + 1) - gammaln(days - n + 1) - n * math.log(days)
        return float(math.exp(log_p))

    def prob_match_exact(self, n: int) -> float:
        """Exact P(at least one shared birthday)."""
        return 1.0 - self.prob_no_match_exact(n)

    def prob_match_approx(self, n: int) -> float:
        """Taylor approximation P(match) ~= 1 - exp(-n(n-1)/(2D))."""
        days = self._config.days_per_year
        if n <= 1:
            return 0.0
        return 1.0 - math.exp(-n * (n - 1) / (2.0 * days))

    def expected_collisions(self, n: int) -> float:
        """Expected number of matching pairs = C(n,2) / D."""
        days = self._config.days_per_year
        if n < 2:
            return 0.0
        return n * (n - 1) / (2.0 * days)

    def expected_unique_birthdays(self, n: int) -> float:
        """
        E[# distinct birthdays] = D * (1 - (1 - 1/D)^n).

        Each day is "missed" with prob (1-1/D)^n.
        """
        days = self._config.days_per_year
        return days * (1.0 - (1.0 - 1.0 / days) ** n)

    def median_group_size(self) -> int:
        """
        Smallest n s.t. P(match) >= 0.5.

        Closed-form approximation: n ~= ceil( (1 + sqrt(1 + 8*D*ln 2)) / 2 ).
        We verify exactly afterwards.
        """
        days = self._config.days_per_year
        approx = math.ceil((1.0 + math.sqrt(1.0 + 8.0 * days * math.log(2.0))) / 2.0)
        # Adjust by walking around the estimate
        n = max(2, approx - 2)
        while self.prob_match_exact(n) < 0.5 and n <= days:
            n += 1
        return n

    def probability_curve(self, max_n: int | None = None) -> tuple[
        NDArray[np.int_], NDArray[np.float64], NDArray[np.float64]
    ]:
        """
        Compute exact + approx curves for n = 1..max_n.

        Returns (group_sizes, exact, approx).
        """
        days = self._config.days_per_year
        if max_n is None:
            max_n = min(self._config.max_people, days)
        ns = np.arange(1, max_n + 1, dtype=np.int_)
        exact = np.array([self.prob_match_exact(int(n)) for n in ns], dtype=np.float64)
        approx = np.array([self.prob_match_approx(int(n)) for n in ns], dtype=np.float64)
        return ns, exact, approx

    def prob_at_least_k_share(self, n: int, k: int, samples: int = 0) -> float:
        """
        P(at least k people share a single birthday).

        Closed-form is intractable for k >= 3; we fall back to MC if requested.
        For k == 2 we return the exact paradox probability.
        For k >= 3 with samples > 0 we run a quick MC; otherwise raise.
        """
        if k < 2:
            raise ValueError("k must be >= 2")
        if k == 2:
            return self.prob_match_exact(n)
        if samples <= 0:
            raise ValueError(f"k={k} requires samples > 0 for Monte Carlo estimation")
        if n < k:
            return 0.0

        rng = np.random.default_rng(0)
        days = self._config.days_per_year
        draws = rng.integers(0, days, size=(samples, n))
        sorted_draws = np.sort(draws, axis=1)
        has_k = np.zeros(samples, dtype=bool)
        for i in range(n - k + 1):
            has_k |= sorted_draws[:, i] == sorted_draws[:, i + k - 1]
        return float(has_k.mean())
