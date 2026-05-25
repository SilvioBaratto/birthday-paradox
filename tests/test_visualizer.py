"""Tests for dual-format animation output in MatplotlibVisualizer."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from birthday.core.config import BirthdayConfig
from birthday.visualization.matplotlib_viz import MatplotlibVisualizer
from birthday.visualization.writers import AnimationWriter


@pytest.fixture
def config() -> BirthdayConfig:
    return BirthdayConfig(days_per_year=365, max_people=10)


@pytest.fixture
def viz(config: BirthdayConfig, tmp_path: Path) -> MatplotlibVisualizer:
    return MatplotlibVisualizer(config, output_dir=tmp_path, seed=42)


class TestDualFormatAnimationOutput:
    """Each animation method should produce both .gif and .mp4."""

    def test_probability_buildup_both_formats(self, viz: MatplotlibVisualizer) -> None:
        with patch.object(MatplotlibVisualizer, "_save_animation") as mock_save:
            gif_path = viz.output_dir / "probability_buildup.gif"
            mp4_path = viz.output_dir / "probability_buildup.mp4"
            mock_save.side_effect = [gif_path, mp4_path]
            result = viz.animate_probability_buildup(save=True, fps=2)
        assert len(result) == 2
        assert result[0] == gif_path
        assert result[1] == mp4_path
        assert mock_save.call_count == 2
        assert mock_save.call_args_list[0][0][1] == gif_path
        assert mock_save.call_args_list[1][0][1] == mp4_path

    def test_animate_room_filling_produces_both_formats(self, viz: MatplotlibVisualizer) -> None:
        with patch.object(MatplotlibVisualizer, "_save_animation") as mock_save:
            gif_path = viz.output_dir / "room_filling.gif"
            mp4_path = viz.output_dir / "room_filling.mp4"
            mock_save.side_effect = [gif_path, mp4_path]
            result = viz.animate_room_filling(save=True, fps=2, group_size=5)
        assert len(result) == 2
        assert result[0] == gif_path
        assert result[1] == mp4_path

    def test_simulation_convergence_both_formats(self, viz: MatplotlibVisualizer) -> None:
        with patch.object(MatplotlibVisualizer, "_save_animation") as mock_save:
            gif_path = viz.output_dir / "convergence.gif"
            mp4_path = viz.output_dir / "convergence.mp4"
            mock_save.side_effect = [gif_path, mp4_path]
            result = viz.animate_simulation_convergence(save=True, fps=2, max_trials=10)
        assert len(result) == 2
        assert result[0] == gif_path
        assert result[1] == mp4_path

    def test_animate_k_collision_produces_both_formats(self, viz: MatplotlibVisualizer) -> None:
        with patch.object(MatplotlibVisualizer, "_save_animation") as mock_save:
            gif_path = viz.output_dir / "k_collision_animation.gif"
            mp4_path = viz.output_dir / "k_collision_animation.mp4"
            mock_save.side_effect = [gif_path, mp4_path]
            result = viz.animate_k_collision(save=True, n_trials=100, fps=2)
        assert len(result) == 2
        assert result[0] == gif_path
        assert result[1] == mp4_path


class TestNoMp4Flag:
    """no_mp4=True should skip MP4 generation."""

    def test_animate_skips_mp4_when_no_mp4_true(self, viz: MatplotlibVisualizer) -> None:
        with patch.object(MatplotlibVisualizer, "_save_animation") as mock_save:
            gif_path = viz.output_dir / "probability_buildup.gif"
            mock_save.return_value = gif_path
            result = viz.animate_probability_buildup(save=True, fps=2, no_mp4=True)
        assert len(result) == 1
        assert result[0] == gif_path
        assert mock_save.call_count == 1

    def test_create_all_with_no_mp4_returns_ten_files(self, viz: MatplotlibVisualizer) -> None:
        result = viz.create_all(n_trials=100, no_mp4=True)
        assert len(result) == 10
        names = {p.name for p in result}
        assert "probability_buildup.gif" in names
        assert "room_filling.gif" in names
        assert "convergence.gif" in names
        assert "k_collision_animation.gif" in names
        assert not any(p.suffix == ".mp4" for p in result)

    def test_create_all_returns_fourteen_files(self, viz: MatplotlibVisualizer) -> None:
        with patch.object(AnimationWriter, "_discover_ffmpeg", return_value="/fake/ffmpeg"), \
             patch.object(MatplotlibVisualizer, "_save_animation") as mock_save:
            # Simulate GIF + MP4 for each animation, PNG for each static plot
            mock_save.side_effect = [
                viz.output_dir / "probability_buildup.gif",
                viz.output_dir / "probability_buildup.mp4",
                viz.output_dir / "room_filling.gif",
                viz.output_dir / "room_filling.mp4",
                viz.output_dir / "convergence.gif",
                viz.output_dir / "convergence.mp4",
                viz.output_dir / "k_collision_animation.gif",
                viz.output_dir / "k_collision_animation.mp4",
            ]
            result = viz.create_all(n_trials=100)
        assert len(result) == 14


class TestGracefulFfmpegFallback:
    """When ffmpeg is unavailable, GIF is still produced."""

    def test_returns_only_gif_when_ffmpeg_unavailable(self, viz: MatplotlibVisualizer) -> None:
        with patch.object(MatplotlibVisualizer, "_save_animation") as mock_save:
            gif_path = viz.output_dir / "probability_buildup.gif"
            mock_save.side_effect = [gif_path, None]
            result = viz.animate_probability_buildup(save=True, fps=2)
        assert len(result) == 1
        assert result[0] == gif_path

    def test_returns_empty_list_when_save_false(self, viz: MatplotlibVisualizer) -> None:
        result = viz.animate_probability_buildup(save=False, fps=2)
        assert result == []


class TestIntegrationDualFormat:
    """Real file creation tests for dual format."""

    def test_animate_k_collision_creates_real_gif_and_mp4(self, viz: MatplotlibVisualizer) -> None:
        result = viz.animate_k_collision(save=True, n_trials=100, fps=2)
        assert len(result) >= 1
        assert any(p.name == "k_collision_animation.gif" for p in result)
        # MP4 only if ffmpeg is available
        writer = AnimationWriter()
        if writer._discover_ffmpeg() is not None:
            assert any(p.name == "k_collision_animation.mp4" for p in result)
