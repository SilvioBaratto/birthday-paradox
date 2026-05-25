"""Tests for the AnimationWriter abstraction."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import matplotlib.animation as animation

from birthday.core.config import BirthdayConfig
from birthday.visualization.matplotlib_viz import MatplotlibVisualizer
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

    def test_default_mp4_fps_and_bitrate(self) -> None:
        writer = AnimationWriter()
        assert writer.mp4_fps == 30
        assert writer.bitrate == 4_000_000

    def test_custom_mp4_fps_and_bitrate(self) -> None:
        writer = AnimationWriter(mp4_fps=60, bitrate=8_000_000)
        assert writer.mp4_fps == 60
        assert writer.bitrate == 8_000_000


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
        writer = AnimationWriter(fps=15, dpi=200, mp4_fps=30, bitrate=4_000_000)
        mock_writer = MagicMock()
        with patch.object(
            animation, "FFMpegWriter", return_value=mock_writer
        ) as mock_ffmpeg, patch.object(
            animation.FFMpegWriter, "isAvailable", return_value=True
        ), patch.object(
            AnimationWriter, "_discover_ffmpeg", return_value="/fake/ffmpeg"
        ):
            result = writer.get_writer(Path("test.mp4"))
            assert result is not None
            mock_ffmpeg.assert_called_once_with(
                fps=30,
                codec="libx264",
                bitrate=4_000_000,
                extra_args=["-pix_fmt", "yuv420p"],
                metadata={
                    "title": "Birthday Paradox Animation",
                    "artist": "birthday-paradox",
                },
            )

    def test_returns_none_for_mp4_when_ffmpeg_missing(self, caplog: Any) -> None:
        writer = AnimationWriter()
        with patch.object(
            AnimationWriter, "_discover_ffmpeg", return_value=None
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


class TestDiscoverFfmpeg:
    def test_uses_imageio_ffmpeg_first(self) -> None:
        writer = AnimationWriter()
        with patch(
            "birthday.visualization.writers.imageio_ffmpeg.get_ffmpeg_exe",
            return_value="/bundled/ffmpeg",
        ):
            result = writer._discover_ffmpeg()
        assert result == "/bundled/ffmpeg"

    def test_falls_back_to_shutil_when_imageio_ffmpeg_not_found(self) -> None:
        writer = AnimationWriter()
        with patch(
            "birthday.visualization.writers.imageio_ffmpeg.get_ffmpeg_exe",
            side_effect=RuntimeError("not found"),
        ), patch(
            "shutil.which", return_value="/usr/bin/ffmpeg"
        ) as mock_which:
            result = writer._discover_ffmpeg()
        assert result == "/usr/bin/ffmpeg"
        mock_which.assert_called_once_with("ffmpeg")

    def test_returns_none_when_no_ffmpeg_found(self) -> None:
        writer = AnimationWriter()
        with patch(
            "birthday.visualization.writers.imageio_ffmpeg.get_ffmpeg_exe",
            side_effect=RuntimeError("not found"),
        ), patch("shutil.which", return_value=None):
            result = writer._discover_ffmpeg()
        assert result is None

    def test_falls_back_when_imageio_ffmpeg_module_none(self) -> None:
        import birthday.visualization.writers as writers_mod

        writer = AnimationWriter()
        with patch.object(
            writers_mod, "imageio_ffmpeg", None
        ), patch(
            "shutil.which", return_value="/usr/bin/ffmpeg"
        ) as mock_which:
            result = writer._discover_ffmpeg()
        assert result == "/usr/bin/ffmpeg"
        mock_which.assert_called_once_with("ffmpeg")


class TestTryFfmpeg:
    def test_returns_writer_when_ffmpeg_available(self) -> None:
        writer = AnimationWriter(mp4_fps=30, bitrate=4_000_000)
        mock_ffmpeg_writer = MagicMock()
        with patch.object(
            animation.FFMpegWriter, "isAvailable", return_value=True
        ), patch.object(
            animation, "FFMpegWriter", return_value=mock_ffmpeg_writer
        ) as mock_cls, patch.object(
            AnimationWriter, "_discover_ffmpeg", return_value="/fake/ffmpeg"
        ):
            result = writer._try_ffmpeg(fps=30)
        assert result is mock_ffmpeg_writer
        mock_cls.assert_called_once_with(
            fps=30,
            codec="libx264",
            bitrate=4_000_000,
            extra_args=["-pix_fmt", "yuv420p"],
            metadata={
                "title": "Birthday Paradox Animation",
                "artist": "birthday-paradox",
            },
        )

    def test_returns_none_when_ffmpeg_not_available(self) -> None:
        writer = AnimationWriter()
        with patch.object(
            AnimationWriter, "_discover_ffmpeg", return_value=None
        ):
            result = writer._try_ffmpeg(fps=30)
        assert result is None

    def test_returns_none_when_isavailable_false(self) -> None:
        writer = AnimationWriter()
        with patch.object(
            animation.FFMpegWriter, "isAvailable", return_value=False
        ), patch.object(
            AnimationWriter, "_discover_ffmpeg", return_value="/broken/ffmpeg"
        ):
            result = writer._try_ffmpeg(fps=30)
        assert result is None


class TestIntegrationWithMatplotlibVisualizer:
    """Verify MatplotlibVisualizer can use AnimationWriter without inline writer= strings."""

    def test_visualizer_imports_and_uses_writer(self) -> None:
        config = BirthdayConfig(days_per_year=365, max_people=50)
        viz = MatplotlibVisualizer(config, output_dir="/tmp/test_output")

        # Verify the visualizer has an _animation_writer attribute
        assert hasattr(viz, "_animation_writer")
        assert isinstance(viz._animation_writer, AnimationWriter)

    def test_visualizer_has_mp4_defaults(self) -> None:
        config = BirthdayConfig(days_per_year=365, max_people=50)
        viz = MatplotlibVisualizer(config, output_dir="/tmp/test_output")
        writer = viz._animation_writer
        assert writer.mp4_fps == 30
        assert writer.bitrate == 4_000_000
