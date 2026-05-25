"""Animation writer abstraction for Matplotlib visualizations."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

import matplotlib.animation as animation

logger = logging.getLogger(__name__)

try:
    import imageio_ffmpeg
except ImportError:  # pragma: no cover
    imageio_ffmpeg = None


class AnimationWriter:
    """Selects the correct Matplotlib animation writer based on file extension."""

    __slots__ = ("fps", "dpi", "mp4_fps", "bitrate")

    _SUPPORTED: frozenset[str] = frozenset({"gif", "mp4"})

    def __init__(
        self,
        fps: int = 8,
        dpi: int = 100,
        mp4_fps: int = 30,
        bitrate: int = 4_000_000,
    ) -> None:
        self.fps = fps
        self.dpi = dpi
        self.mp4_fps = mp4_fps
        self.bitrate = bitrate

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
            return self._try_ffmpeg(self.mp4_fps)

        logger.warning(f"Unsupported animation extension: '{ext}' for {path}")
        return None

    def _discover_ffmpeg(self) -> str | None:
        """Discover ffmpeg binary via imageio-ffmpeg first, then system PATH."""
        if imageio_ffmpeg is not None:
            try:
                return str(imageio_ffmpeg.get_ffmpeg_exe())
            except RuntimeError:
                pass

        return shutil.which("ffmpeg")

    def _try_ffmpeg(self, fps: int) -> animation.MovieWriter | None:
        """Attempt to create a production-configured FFMpegWriter; return None on failure."""
        ffmpeg_path = self._discover_ffmpeg()
        if ffmpeg_path is None:
            logger.warning("ffmpeg not found; skipping MP4 output")
            return None

        import matplotlib as mpl

        old_path = mpl.rcParams["animation.ffmpeg_path"]
        mpl.rcParams["animation.ffmpeg_path"] = ffmpeg_path
        try:
            if not animation.FFMpegWriter.isAvailable():
                logger.warning(
                    f"ffmpeg at {ffmpeg_path} not executable; skipping MP4 output"
                )
                return None
            return animation.FFMpegWriter(
                fps=fps,
                codec="libx264",
                bitrate=self.bitrate,
                extra_args=["-pix_fmt", "yuv420p"],
                metadata={
                    "title": "Birthday Paradox Animation",
                    "artist": "birthday-paradox",
                },
            )
        finally:
            mpl.rcParams["animation.ffmpeg_path"] = old_path
