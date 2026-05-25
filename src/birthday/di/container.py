"""Dependency injection container for the Birthday Paradox."""

from __future__ import annotations

from pathlib import Path

from birthday.core.config import BirthdayConfig
from birthday.math.probability import BirthdayProbability
from birthday.simulation.monte_carlo import MonteCarloSimulator
from birthday.visualization.matplotlib_viz import MatplotlibVisualizer


class Container:
    """Wire and resolve Birthday Paradox services."""

    __slots__ = ("_config", "_output_dir", "_seed")

    def __init__(
        self,
        *,
        days: int = 365,
        max_people: int = 100,
        output_dir: Path | str = "output",
        seed: int | None = 42,
        config: BirthdayConfig | None = None,
    ) -> None:
        self._config = config or BirthdayConfig(days_per_year=days, max_people=max_people)
        self._output_dir = Path(output_dir)
        self._seed = seed

    def config(self) -> BirthdayConfig:
        return self._config

    def probability(self) -> BirthdayProbability:
        return BirthdayProbability(self._config)

    def simulator(self, seed: int | None = None) -> MonteCarloSimulator:
        actual_seed = seed if seed is not None else self._seed
        return MonteCarloSimulator(self._config, seed=actual_seed)

    def visualizer(
        self,
        output_dir: Path | str | None = None,
        seed: int | None = None,
    ) -> MatplotlibVisualizer:
        actual_output = output_dir if output_dir is not None else self._output_dir
        actual_seed = seed if seed is not None else self._seed
        return MatplotlibVisualizer(
            self._config,
            output_dir=actual_output,
            seed=actual_seed,
        )
