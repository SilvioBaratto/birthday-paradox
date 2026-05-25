"""Animation writer abstraction for Matplotlib visualizations."""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.animation as animation

logger = logging.getLogger(__name__)


class AnimationWriter:
    """Selects the correct Matplotlib animation writer based on file extension."""

    __slots__ = ("fps", "dpi")

    _SUPPORTED: frozenset[str] = frozenset({"gif", "mp4"})

    def __init__(self, fps: int = 8, dpi: int = 100) -> None:
        self.fps = fps
        self.dpi = dpi

    @classmethod
    def supports(cls, extension: str) -> bool:
        """Return True if the given file extension is supported."""
        ext = extension.lstrip(".").lower()
        return ext in cls._SUPPORTED

    def get_writer(
        self, path: Path, fps: int | None = None, dpi: int | None = None,
    ) -> animation.MovieWriter | None:
        """Return a Matplotlib writer instance for the given path, or None if unsupported."""
        ext = path.suffix.lstrip(".").lower()
        actual_fps = fps if fps is not None else self.fps

        if ext == "gif":
            return animation.PillowWriter(fps=actual_fps)  # type: ignore[return-value]

        if ext == "mp4":
            return self._try_ffmpeg(actual_fps)

        logger.warning(f"Unsupported animation extension: '{ext}' for {path}")
        return None

    def _try_ffmpeg(self, fps: int) -> animation.MovieWriter | None:
        """Attempt to create an FFMpegWriter; log and return None on failure."""
        try:
            return animation.FFMpegWriter(fps=fps)
        except (RuntimeError, ImportError) as exc:
            logger.warning(f"FFMpegWriter unavailable ({exc}); skipping MP4 output")
            return None
