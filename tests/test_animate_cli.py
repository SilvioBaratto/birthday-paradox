"""Tests for the birthday animate CLI subcommand."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from birthday.cli import cli


class TestAnimateSubcommand:
    """birthday animate <name> renders a single animation."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        return CliRunner()

    def test_animate_probability_buildup(self, runner: CliRunner, tmp_path: Path) -> None:
        result = runner.invoke(
            cli,
            [
                "animate", "probability_buildup",
                "--max-people", "10",
                "-o", str(tmp_path),
                "--fps", "2",
            ],
        )
        assert result.exit_code == 0, result.output
        assert (tmp_path / "probability_buildup.gif").exists()
        assert (tmp_path / "probability_buildup.mp4").exists()

    def test_animate_room_filling(self, runner: CliRunner, tmp_path: Path) -> None:
        result = runner.invoke(
            cli,
            [
                "animate", "room_filling",
                "--max-people", "10",
                "-o", str(tmp_path),
                "--fps", "2",
            ],
        )
        assert result.exit_code == 0, result.output
        assert (tmp_path / "room_filling.gif").exists()

    def test_animate_convergence(self, runner: CliRunner, tmp_path: Path) -> None:
        result = runner.invoke(
            cli,
            [
                "animate", "convergence",
                "--max-people", "10",
                "-o", str(tmp_path),
                "--fps", "2",
            ],
        )
        assert result.exit_code == 0, result.output
        assert (tmp_path / "convergence.gif").exists()

    def test_animate_k_collision(self, runner: CliRunner, tmp_path: Path) -> None:
        result = runner.invoke(
            cli,
            [
                "animate", "k_collision",
                "--max-people", "10",
                "-o", str(tmp_path),
                "--fps", "2",
            ],
        )
        assert result.exit_code == 0, result.output
        assert (tmp_path / "k_collision_animation.gif").exists()

    def test_animate_invalid_name_shows_error(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["animate", "not_a_name"])
        assert result.exit_code == 2
        assert "Invalid value" in result.output or "not_a_name" in result.output

    def test_animate_no_mp4_suppresses_mp4(self, runner: CliRunner, tmp_path: Path) -> None:
        result = runner.invoke(
            cli,
            [
                "animate", "probability_buildup",
                "--max-people", "10",
                "-o", str(tmp_path),
                "--fps", "2",
                "--no-mp4",
            ],
        )
        assert result.exit_code == 0, result.output
        assert (tmp_path / "probability_buildup.gif").exists()
        assert not (tmp_path / "probability_buildup.mp4").exists()

    def test_animate_respects_days_option(self, runner: CliRunner, tmp_path: Path) -> None:
        result = runner.invoke(
            cli,
            [
                "animate", "probability_buildup",
                "--days", "10",
                "--max-people", "10",
                "-o", str(tmp_path),
                "--fps", "2",
            ],
        )
        assert result.exit_code == 0, result.output

    def test_animate_respects_seed_option(self, runner: CliRunner, tmp_path: Path) -> None:
        result = runner.invoke(
            cli,
            [
                "animate", "room_filling",
                "--max-people", "10",
                "-o", str(tmp_path),
                "--seed", "42",
                "--fps", "2",
            ],
        )
        assert result.exit_code == 0, result.output
