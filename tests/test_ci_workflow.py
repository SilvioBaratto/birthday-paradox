"""Tests for the GitHub Actions CI workflow."""

from pathlib import Path

import pytest

WORKFLOW = Path(".github/workflows/ci.yml")


class TestCiWorkflowExists:
    """Workflow file must exist."""

    def test_file_exists(self) -> None:
        assert WORKFLOW.exists(), f"{WORKFLOW} must exist"


class TestCiWorkflowContent:
    """Structure and commands inside ci.yml."""

    @pytest.fixture
    def content(self) -> str:
        if not WORKFLOW.exists():
            pytest.skip(f"{WORKFLOW} not present yet")
        return WORKFLOW.read_text()

    @pytest.fixture
    def lines(self, content: str) -> set[str]:
        return set(content.splitlines())

    def test_python_matrix_includes_310_311_312(self, content: str) -> None:
        assert '"3.10"' in content, "matrix must include Python 3.10"
        assert '"3.11"' in content, "matrix must include Python 3.11"
        assert '"3.12"' in content, "matrix must include Python 3.12"

    def test_ruff_check_step(self, content: str) -> None:
        assert "ruff check" in content, "workflow must run ruff check"

    def test_mypy_step(self, content: str) -> None:
        assert "mypy" in content, "workflow must run mypy"

    def test_pytest_step(self, content: str) -> None:
        assert "pytest" in content, "workflow must run pytest"

    def test_release_trigger_on_version_tags(self, content: str) -> None:
        assert "v*" in content, "release must trigger on tags matching v*"

    def test_release_runs_birthday_all(self, content: str) -> None:
        assert "birthday all -t 5000" in content, "release job must run birthday all -t 5000"

    def test_release_uses_ubuntu(self, content: str) -> None:
        assert "ubuntu-latest" in content, "jobs should run on ubuntu-latest"

    def test_release_uploads_artifacts(self, content: str) -> None:
        has_upload = "upload" in content.lower() or "gh release" in content.lower()
        assert has_upload, "release job must upload output artifacts"

    def test_ffmpeg_install_step(self, content: str) -> None:
        assert "ffmpeg" in content.lower(), "release job must install ffmpeg for MP4 generation"
