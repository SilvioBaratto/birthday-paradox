"""Tests for .gitignore rules."""

from pathlib import Path

import pytest

GITIGNORE = Path(".gitignore")


class TestGitignore:
    """Verify repository hygiene rules in .gitignore."""

    @pytest.fixture
    def gitignore_lines(self) -> set[str]:
        assert GITIGNORE.exists(), ".gitignore must exist"
        return set(GITIGNORE.read_text().splitlines())

    def test_output_mp4_ignored(self, gitignore_lines: set[str]) -> None:
        when = "output/*.mp4 is present"
        then = "large MP4 binaries are excluded from version control"
        assert "output/*.mp4" in gitignore_lines, f"{when} → {then}"

    def test_output_gitkeep_tracked(self) -> None:
        path = Path("output/.gitkeep")
        assert path.exists(), "output/.gitkeep must exist so the directory is tracked"
