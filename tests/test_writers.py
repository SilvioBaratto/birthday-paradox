"""Tests for the AnimationWriter abstraction."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import matplotlib.animation as animation

from birthday.visualization.writers import AnimationWriter


class TestAnimationWriterInit:
    def test_default_fps_and_dpi(self) -> None:
        writer = AnimationWriter()
        assert writer.fps == 8
        assert writer.dpi == 100

    def test_custom_fps_and_dpi(self) -> None:
        writer = AnimationWriter(fps=12, dpi=150)
        assert writer.fps == 12
        assert writer.dpi == 150


class TestSupports:
    def test_supports_gif(self) -> None:
        assert AnimationWriter.supports("gif") is True
        assert AnimationWriter.supports(".gif") is True

    def test_supports_mp4(self) -> None:
        assert AnimationWriter.supports("mp4") is True
        assert AnimationWriter.supports(".mp4") is True

    def test_does_not_support_unknown(self) -> None:
        assert AnimationWriter.supports("png") is False
        assert AnimationWriter.supports("avi") is False
        assert AnimationWriter.supports("") is False


class TestGetWriter:
    def test_returns_pillow_writer_for_gif(self) -> None:
        writer = AnimationWriter(fps=10, dpi=120)
        result = writer.get_writer(Path("test.gif"))
        assert isinstance(result, animation.PillowWriter)
        assert result.fps == 10

    def test_returns_ffmpeg_writer_for_mp4_when_available(self) -> None:
        writer = AnimationWriter(fps=15, dpi=200)
        with patch.object(
            animation, "FFMpegWriter", return_value=MagicMock()
        ) as mock_ffmpeg:
            result = writer.get_writer(Path("test.mp4"))
            assert result is not None
            mock_ffmpeg.assert_called_once_with(fps=15)

    def test_returns_none_for_mp4_when_ffmpeg_missing(self, caplog: Any) -> None:
        writer = AnimationWriter()
        with patch.object(
            animation, "FFMpegWriter", side_effect=RuntimeError("ffmpeg not found")
        ), caplog.at_level(logging.WARNING):
            result = writer.get_writer(Path("test.mp4"))
        assert result is None
        assert "ffmpeg" in caplog.text.lower()

    def test_returns_none_for_unsupported_extension(self, caplog: Any) -> None:
        writer = AnimationWriter()
        with caplog.at_level(logging.WARNING):
            result = writer.get_writer(Path("test.png"))
        assert result is None
        assert "unsupported" in caplog.text.lower()

    def test_extension_case_insensitive(self) -> None:
        writer = AnimationWriter()
        result = writer.get_writer(Path("test.GIF"))
        assert isinstance(result, animation.PillowWriter)


class TestIntegrationWithMatplotlibVisualizer:
    """Verify MatplotlibVisualizer can use AnimationWriter without inline writer= strings."""

    def test_visualizer_imports_and_uses_writer(self) -> None:
        from birthday.core.config import BirthdayConfig
        from birthday.visualization.matplotlib_viz import MatplotlibVisualizer

        config = BirthdayConfig(days_per_year=365, max_people=50)
        viz = MatplotlibVisualizer(config, output_dir="/tmp/test_output")

        # Verify the visualizer has an _animation_writer attribute
        assert hasattr(viz, "_animation_writer")
        assert isinstance(viz._animation_writer, AnimationWriter)
