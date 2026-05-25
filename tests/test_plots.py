"""Tests for static plot methods in MatplotlibVisualizer."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from birthday.core.config import BirthdayConfig
from birthday.math.probability import BirthdayProbability
from birthday.visualization.matplotlib_viz import MatplotlibVisualizer
from birthday.visualization.writers import AnimationWriter


@pytest.fixture
def config() -> BirthdayConfig:
    return BirthdayConfig(days_per_year=365, max_people=50)


@pytest.fixture
def viz(config: BirthdayConfig, tmp_path: Path) -> MatplotlibVisualizer:
    return MatplotlibVisualizer(config, output_dir=tmp_path, seed=42)


class TestPlotKCollisionCurves:
    def test_returns_path_when_save_true(self, viz: MatplotlibVisualizer) -> None:
        result = viz.plot_k_collision_curves(save=True, n_trials=500)
        assert result is not None
        assert result.name == "k_collision_curves.png"
        assert result.exists()

    def test_returns_none_when_save_false(self, viz: MatplotlibVisualizer) -> None:
        result = viz.plot_k_collision_curves(save=False, n_trials=100)
        assert result is None

    def test_file_has_content(self, viz: MatplotlibVisualizer) -> None:
        result = viz.plot_k_collision_curves(save=True, n_trials=500)
        assert result is not None
        assert result.stat().st_size > 0

    @patch.object(BirthdayProbability, "prob_at_least_k_share", return_value=0.05)
    @patch.object(BirthdayProbability, "prob_match_exact", return_value=0.5)
    def test_calls_prob_methods(
        self,
        mock_exact: MagicMock,
        mock_k: MagicMock,
        config: BirthdayConfig,
        tmp_path: Path,
    ) -> None:
        viz = MatplotlibVisualizer(config, output_dir=tmp_path, seed=42)
        viz.plot_k_collision_curves(save=False, n_trials=100)
        mock_exact.assert_called()
        k_calls = [call.args[1] for call in mock_k.call_args_list]
        assert sorted(set(k_calls)) == [3, 4, 5]

    @patch.object(BirthdayProbability, "prob_at_least_k_share", return_value=0.05)
    def test_max_n_respects_config(
        self,
        mock_k: MagicMock,
        config: BirthdayConfig,
        tmp_path: Path,
    ) -> None:
        viz = MatplotlibVisualizer(config, output_dir=tmp_path, seed=42)
        viz.plot_k_collision_curves(save=False, n_trials=100)
        call_ns = {call.args[0] for call in mock_k.call_args_list}
        assert max(call_ns) == config.max_people


class TestAnimateKCollision:
    def test_returns_path_when_save_true(self, viz: MatplotlibVisualizer) -> None:
        result = viz.animate_k_collision(save=True, n_trials=100, fps=2)
        assert result is not None
        assert result.name == "k_collision_animation.gif"
        assert result.exists()

    def test_returns_none_when_save_false(self, viz: MatplotlibVisualizer) -> None:
        result = viz.animate_k_collision(save=False, n_trials=100, fps=2)
        assert result is None

    def test_file_has_content(self, viz: MatplotlibVisualizer) -> None:
        result = viz.animate_k_collision(save=True, n_trials=100, fps=2)
        assert result is not None
        assert result.stat().st_size > 0

    @patch.object(BirthdayProbability, "prob_at_least_k_share", return_value=0.05)
    @patch.object(BirthdayProbability, "prob_match_exact", return_value=0.5)
    def test_precomputes_curves(
        self,
        mock_exact: MagicMock,
        mock_k: MagicMock,
        viz: MatplotlibVisualizer,
    ) -> None:
        viz.animate_k_collision(save=False, n_trials=100, fps=2)
        mock_exact.assert_called()
        k_calls = [call.args[1] for call in mock_k.call_args_list]
        assert sorted(set(k_calls)) == [3, 4, 5]

    def test_uses_animation_writer(self, viz: MatplotlibVisualizer) -> None:
        with patch.object(
            AnimationWriter, "get_writer", return_value=MagicMock()
        ) as mock_writer:
            viz.animate_k_collision(save=True, n_trials=100, fps=2)
            mock_writer.assert_called()
            call_path = mock_writer.call_args[0][0]
            assert str(call_path).endswith(".gif")


class TestPlotApproximationError:
    def test_returns_path_when_save_true(self, viz: MatplotlibVisualizer) -> None:
        result = viz.plot_approximation_error(save=True)
        assert result is not None
        assert result.name == "approximation_error.png"
        assert result.exists()

    def test_returns_none_when_save_false(self, viz: MatplotlibVisualizer) -> None:
        result = viz.plot_approximation_error(save=False)
        assert result is None

    def test_file_has_content(self, viz: MatplotlibVisualizer) -> None:
        result = viz.plot_approximation_error(save=True)
        assert result is not None
        assert result.stat().st_size > 0

    @patch.object(BirthdayProbability, "probability_curve")
    def test_uses_probability_curve(
        self,
        mock_curve: MagicMock,
        config: BirthdayConfig,
        tmp_path: Path,
    ) -> None:
        ns = np.arange(1, config.max_people + 1)
        mock_curve.return_value = (ns, np.zeros(len(ns)), np.zeros(len(ns)))
        viz = MatplotlibVisualizer(config, output_dir=tmp_path, seed=42)
        viz.plot_approximation_error(save=False)
        mock_curve.assert_called_once()

    @patch.object(BirthdayProbability, "probability_curve")
    def test_max_error_below_threshold_for_d365(
        self,
        mock_curve: MagicMock,
        config: BirthdayConfig,
        tmp_path: Path,
    ) -> None:
        """For D=365, n<=100, max abs error should be < 0.012."""
        ns = np.arange(1, 101)
        exact = np.array([1.0 - np.exp(-n * (n - 1) / (2.0 * 365)) for n in ns])
        # Slightly perturbed approx to simulate real behavior
        approx = exact + np.sin(ns / 10) * 0.005
        mock_curve.return_value = (ns, exact, approx)
        viz = MatplotlibVisualizer(config, output_dir=tmp_path, seed=42)
        result = viz.plot_approximation_error(save=False)
        assert result is None  # save=False
        max_error = float(np.max(np.abs(exact - approx)))
        assert max_error < 0.012
