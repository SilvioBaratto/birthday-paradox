"""Result containers for simulations and analyses."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True, slots=True)
class SimulationResult:
    """
    Outcome of a Monte Carlo run for a single group size.

    Attributes:
        group_size: Number of people in the room (n).
        n_trials: Number of Monte Carlo trials.
        n_collisions: Trials in which at least one shared birthday occurred.
        collision_indices: For each trial, index (1-based) of the person who
            first produced a collision, or 0 if none occurred.
    """

    group_size: int
    n_trials: int
    n_collisions: int
    collision_indices: NDArray[np.int_] = field(repr=False)

    @property
    def empirical_probability(self) -> float:
        """Empirical P(at least one shared birthday)."""
        return self.n_collisions / self.n_trials if self.n_trials else 0.0


@dataclass(frozen=True, slots=True)
class CollisionCurve:
    """
    Probability curve across group sizes.

    Attributes:
        group_sizes: Array of n values.
        theoretical: Exact P(match) for each n.
        approximation: Taylor approximation 1 - exp(-n(n-1)/(2D)) for each n.
        empirical: Monte Carlo P(match) for each n (may be empty).
    """

    group_sizes: NDArray[np.int_]
    theoretical: NDArray[np.float64]
    approximation: NDArray[np.float64]
    empirical: NDArray[np.float64] = field(default_factory=lambda: np.array([]))
