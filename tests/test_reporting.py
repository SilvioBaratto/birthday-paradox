"""Tests for ConsoleReporter and birthday report CLI."""

from __future__ import annotations

from click.testing import CliRunner

from birthday.cli import cli
from birthday.core.config import BirthdayConfig
from birthday.math.probability import BirthdayProbability


class TestConsoleReporter:
    """ConsoleReporter formats a checkpoint table."""

    def test_report_contains_all_checkpoints(self) -> None:
        from birthday.reporting.console import ConsoleReporter

        prob = BirthdayProbability(BirthdayConfig())
        reporter = ConsoleReporter(prob)
        output = reporter.report()
        for n in (5, 10, 23, 30, 50, 70, 100):
            assert str(n) in output

    def test_report_contains_all_columns(self) -> None:
        from birthday.reporting.console import ConsoleReporter

        prob = BirthdayProbability(BirthdayConfig())
        reporter = ConsoleReporter(prob)
        output = reporter.report()
        assert "exact" in output.lower() or "P(match)" in output
        assert "approx" in output.lower() or "P(match)" in output
        assert "E[pairs]" in output or "pairs" in output.lower()
        assert "residual" in output.lower()

    def test_report_lines_fit_80_columns(self) -> None:
        from birthday.reporting.console import ConsoleReporter

        prob = BirthdayProbability(BirthdayConfig())
        reporter = ConsoleReporter(prob)
        output = reporter.report()
        for line in output.splitlines():
            assert len(line) <= 80, f"line too long: {line!r} ({len(line)} chars)"

    def test_report_has_header_and_separator(self) -> None:
        from birthday.reporting.console import ConsoleReporter

        prob = BirthdayProbability(BirthdayConfig())
        reporter = ConsoleReporter(prob)
        output = reporter.report()
        lines = output.splitlines()
        assert len(lines) >= 9  # header + separator + 7 checkpoints

    def test_default_checkpoints(self) -> None:
        from birthday.reporting.console import ConsoleReporter

        prob = BirthdayProbability(BirthdayConfig())
        reporter = ConsoleReporter(prob)
        assert reporter.checkpoints == [5, 10, 23, 30, 50, 70, 100]

    def test_custom_checkpoints(self) -> None:
        from birthday.reporting.console import ConsoleReporter

        prob = BirthdayProbability(BirthdayConfig())
        reporter = ConsoleReporter(prob, checkpoints=[10, 23])
        output = reporter.report()
        lines = [ln for ln in output.splitlines() if ln.strip() and not ln.startswith("---")]
        data_lines = lines[1:]  # skip header
        first_cols = [ln[:3].strip() for ln in data_lines]
        assert "10" in first_cols
        assert "23" in first_cols
        assert "50" not in first_cols


class TestCliReportCommand:
    """birthday report CLI subcommand."""

    def test_report_command_exists(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["report"])
        assert result.exit_code == 0, result.output

    def test_report_outputs_table(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["report"])
        assert "23" in result.output
        assert "exact" in result.output.lower() or "P(match)" in result.output

    def test_report_respects_days_option(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["report", "--days", "10"])
        assert result.exit_code == 0, result.output
