"""Tests for README v1.1 content."""

from pathlib import Path

import pytest

README = Path("README.md")


class TestReadmeExists:
    """README file must exist."""

    def test_file_exists(self) -> None:
        assert README.exists(), f"{README} must exist"


class TestReadmeV11:
    """Validate v1.1 additions per issue #18 acceptance criteria."""

    @pytest.fixture
    def text(self) -> str:
        if not README.exists():
            pytest.skip(f"{README} not present yet")
        return README.read_text()

    @pytest.fixture
    def lines(self, text: str) -> set[str]:
        return {line.strip() for line in text.splitlines()}

    def test_version_bump_referenced(self, text: str) -> None:
        assert "v1.1" in text, "README must reference v1.1"

    def test_imageio_ffmpeg_documented(self, text: str) -> None:
        assert "imageio-ffmpeg" in text, "README must document imageio-ffmpeg"

    def test_birthday_animate_usage(self, text: str) -> None:
        assert "birthday animate" in text, "README must include birthday animate usage"

    def test_animate_names_probability_buildup(self, text: str) -> None:
        assert "probability_buildup" in text, "README must document probability_buildup animation"

    def test_animate_names_room_filling(self, text: str) -> None:
        assert "room_filling" in text, "README must document room_filling animation"

    def test_animate_names_convergence(self, text: str) -> None:
        assert "convergence" in text, "README must document convergence animation"

    def test_animate_names_k_collision(self, text: str) -> None:
        assert "k_collision" in text, "README must document k_collision animation"

    def test_no_mp4_flag_documented(self, text: str) -> None:
        assert "--no-mp4" in text, "README must document --no-mp4 flag"

    def test_mp4_links_for_all_animations(self, text: str) -> None:
        for name in [
            "probability_buildup",
            "room_filling",
            "convergence",
            "k_collision_animation",
        ]:
            assert f"{name}.mp4" in text, f"README must link to MP4: {name}.mp4"

    def test_report_feature_documented(self, text: str) -> None:
        assert "birthday report" in text, "README must document birthday report"

    def test_project_layout_includes_reporting(self, text: str) -> None:
        assert "reporting" in text.lower(), "Project Layout must mention reporting/"

    def test_project_layout_includes_di(self, text: str) -> None:
        assert "di/" in text.lower(), "Project Layout must mention di/"

    def test_project_layout_includes_writers(self, text: str) -> None:
        assert "writers" in text.lower(), "Project Layout must mention writers.py"
