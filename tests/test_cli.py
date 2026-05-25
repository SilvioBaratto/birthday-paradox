"""Tests for CLI wiring of new visualizations."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from birthday.cli import cli
from birthday.core.config import BirthdayConfig
from birthday.visualization.matplotlib_viz import MatplotlibVisualizer


class TestCreateAllProducesTenFiles:
    def test_returns_ten_files_with_no_mp4(self, tmp_path: Path) -> None:
        config = BirthdayConfig(days_per_year=365, max_people=10)
        viz = MatplotlibVisualizer(config, output_dir=tmp_path, seed=42)
        result = viz.create_all(n_trials=100, no_mp4=True)
        assert len(result) == 10
        names = {p.name for p in result}
        assert "k_collision_curves.png" in names
        assert "approximation_error.png" in names
        assert "k_collision_animation.gif" in names
        assert not any(p.suffix == ".mp4" for p in result)

    def test_returns_fourteen_files_with_mp4(self, tmp_path: Path) -> None:
        config = BirthdayConfig(days_per_year=365, max_people=10)
        viz = MatplotlibVisualizer(config, output_dir=tmp_path, seed=42)
        result = viz.create_all(n_trials=100)
        names = {p.name for p in result}
        assert "k_collision_curves.png" in names
        assert "approximation_error.png" in names
        assert "k_collision_animation.gif" in names
        assert "k_collision_animation.mp4" in names

    def test_k_collision_curves_uses_min_50k_trials(self, tmp_path: Path) -> None:
        with patch.object(
            MatplotlibVisualizer, "plot_k_collision_curves", return_value=tmp_path / "k.png"
        ) as mock_plot:
            config = BirthdayConfig(days_per_year=365, max_people=10)
            viz = MatplotlibVisualizer(config, output_dir=tmp_path, seed=42)
            viz.create_all(n_trials=100)
            mock_plot.assert_called_once()
            assert mock_plot.call_args.kwargs["n_trials"] >= 50000


class TestCliPlotCommand:
    def test_plot_skips_mp4_with_flag(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "plot",
                "--max-people", "10",
                "-o", str(tmp_path),
                "-t", "100",
                "--no-mp4",
            ],
        )
        assert result.exit_code == 0, result.output
        names = {p.name for p in tmp_path.iterdir()}
        assert "probability_buildup.gif" in names
        assert "k_collision_animation.gif" in names
        assert not any(n.endswith(".mp4") for n in names)

    def test_plot_generates_mp4_without_flag(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "plot",
                "--max-people", "10",
                "-o", str(tmp_path),
                "-t", "100",
            ],
        )
        assert result.exit_code == 0, result.output
        names = {p.name for p in tmp_path.iterdir()}
        assert "probability_buildup.gif" in names
        assert any(n.endswith(".mp4") for n in names)

    def test_plot_generates_new_static_plots(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "plot",
                "--max-people", "10",
                "-o", str(tmp_path),
                "-t", "100",
                "--no-animations",
            ],
        )
        assert result.exit_code == 0, result.output
        names = {p.name for p in tmp_path.iterdir()}
        assert "k_collision_curves.png" in names
        assert "approximation_error.png" in names
        assert "probability_curve.png" in names

    def test_plot_generates_new_animation(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "plot",
                "--max-people", "10",
                "-o", str(tmp_path),
                "-t", "100",
            ],
        )
        assert result.exit_code == 0, result.output
        names = {p.name for p in tmp_path.iterdir()}
        assert "k_collision_animation.gif" in names
        assert "probability_buildup.gif" in names

    def test_plot_skips_animations_with_flag(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "plot",
                "--max-people", "10",
                "-o", str(tmp_path),
                "-t", "100",
                "--no-animations",
            ],
        )
        assert result.exit_code == 0, result.output
        names = {p.name for p in tmp_path.iterdir()}
        assert "k_collision_animation.gif" not in names
        assert "probability_buildup.gif" not in names

    def test_plot_k_collision_uses_min_50k_trials(self, tmp_path: Path) -> None:
        with patch.object(
            MatplotlibVisualizer, "plot_k_collision_curves", return_value=tmp_path / "k.png"
        ) as mock_plot:
            runner = CliRunner()
            runner.invoke(
                cli,
                [
                    "plot",
                    "--max-people", "10",
                    "-o", str(tmp_path),
                    "-t", "100",
                    "--no-animations",
                ],
            )
            mock_plot.assert_called_once()
            assert mock_plot.call_args.kwargs["n_trials"] >= 50000


class TestCliAllCommand:
    def test_all_generates_ten_files(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "all",
                "--max-people", "10",
                "-o", str(tmp_path),
                "-t", "100",
            ],
        )
        assert result.exit_code == 0, result.output
        names = {p.name for p in tmp_path.iterdir()}
        assert "k_collision_curves.png" in names
        assert "approximation_error.png" in names
        assert "k_collision_animation.gif" in names
        assert any(n.endswith(".mp4") for n in names)

    def test_all_skips_mp4_with_flag(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "all",
                "--max-people", "10",
                "-o", str(tmp_path),
                "-t", "100",
                "--no-mp4",
            ],
        )
        assert result.exit_code == 0, result.output
        names = {p.name for p in tmp_path.iterdir()}
        assert "k_collision_curves.png" in names
        assert "k_collision_animation.gif" in names
        assert not any(n.endswith(".mp4") for n in names)
