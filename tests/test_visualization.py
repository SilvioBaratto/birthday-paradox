"""Integration tests for MatplotlibVisualizer.create_all batch output."""

from __future__ import annotations

from pathlib import Path

import pytest

from birthday.core.config import BirthdayConfig
from birthday.visualization.matplotlib_viz import MatplotlibVisualizer


@pytest.fixture
def config() -> BirthdayConfig:
    return BirthdayConfig(days_per_year=365, max_people=10)


@pytest.fixture
def viz(config: BirthdayConfig, tmp_path: Path) -> MatplotlibVisualizer:
    return MatplotlibVisualizer(config, output_dir=tmp_path, seed=42)


class TestCreateAllBatch:
    """create_all produces all expected PNG and GIF files with non-zero size."""

    _EXPECTED_FILES: frozenset[str] = frozenset({
        "probability_curve.png",
        "simulation_vs_theory.png",
        "expected_collisions.png",
        "first_collision_distribution.png",
        "k_collision_curves.png",
        "approximation_error.png",
        "probability_buildup.gif",
        "room_filling.gif",
        "convergence.gif",
        "k_collision_animation.gif",
    })

    def test_all_expected_files_exist(self, viz: MatplotlibVisualizer) -> None:
        viz.create_all(n_trials=100, no_mp4=True)
        for name in self._EXPECTED_FILES:
            path = viz.output_dir / name
            assert path.exists(), f"missing file: {name}"

    def test_all_expected_files_are_non_empty(self, viz: MatplotlibVisualizer) -> None:
        viz.create_all(n_trials=100, no_mp4=True)
        for name in self._EXPECTED_FILES:
            path = viz.output_dir / name
            assert path.stat().st_size > 0, f"empty file: {name}"

    def test_returns_ten_files(self, viz: MatplotlibVisualizer) -> None:
        result = viz.create_all(n_trials=100, no_mp4=True)
        assert len(result) == 10
        names = {p.name for p in result}
        assert names == self._EXPECTED_FILES
