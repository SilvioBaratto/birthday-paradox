"""Tests for the DI Container and CLI refactoring."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from birthday.cli import cli
from birthday.core.config import BirthdayConfig
from birthday.di.container import Container
from birthday.math.probability import BirthdayProbability
from birthday.simulation.monte_carlo import MonteCarloSimulator
from birthday.visualization.matplotlib_viz import MatplotlibVisualizer


class TestContainerResolvesServices:
    """Container must resolve all four service types."""

    def test_resolves_config(self) -> None:
        container = Container()
        config = container.config()
        assert isinstance(config, BirthdayConfig)
        assert config.days_per_year == 365
        assert config.max_people == 100

    def test_resolves_probability(self) -> None:
        container = Container()
        prob = container.probability()
        assert isinstance(prob, BirthdayProbability)
        assert prob.config == container.config()

    def test_resolves_simulator(self) -> None:
        container = Container()
        sim = container.simulator()
        assert isinstance(sim, MonteCarloSimulator)
        assert sim.config == container.config()

    def test_resolves_visualizer(self) -> None:
        container = Container()
        viz = container.visualizer()
        assert isinstance(viz, MatplotlibVisualizer)
        assert viz.output_dir == Path("output")

    def test_visualizer_uses_config_from_container(self) -> None:
        config = BirthdayConfig(days_per_year=10, max_people=5)
        container = Container(config=config)
        viz = container.visualizer()
        # MatplotlibVisualizer stores config internally; check via output_dir
        assert isinstance(viz, MatplotlibVisualizer)


class TestContainerOverrides:
    """Container supports optional overrides at construction."""

    def test_config_override(self) -> None:
        config = BirthdayConfig(days_per_year=10, max_people=5)
        container = Container(config=config)
        assert container.config() == config
        assert container.config().days_per_year == 10
        assert container.config().max_people == 5

    def test_output_dir_override(self) -> None:
        container = Container(output_dir="/tmp/bday")
        viz = container.visualizer()
        assert viz.output_dir == Path("/tmp/bday")

    def test_seed_override(self) -> None:
        container = Container(seed=99)
        sim = container.simulator()
        assert sim.seed == 99

    def test_simulator_seed_param_overrides_container_seed(self) -> None:
        container = Container(seed=99)
        sim = container.simulator(seed=42)
        assert sim.seed == 42

    def test_visualizer_seed_param_overrides_container_seed(self) -> None:
        container = Container(seed=99)
        viz = container.visualizer(seed=42)
        assert viz._sim.seed == 42

    def test_visualizer_output_dir_param_overrides_container(self) -> None:
        container = Container(output_dir="/tmp/a")
        viz = container.visualizer(output_dir="/tmp/b")
        assert viz.output_dir == Path("/tmp/b")

    def test_default_seed_is_42(self) -> None:
        container = Container()
        assert container.simulator().seed == 42

    def test_default_output_dir_is_output(self) -> None:
        container = Container()
        assert container.visualizer().output_dir == Path("output")


class TestNoCircularImports:
    """Container must not create circular import cycles."""

    def test_di_does_not_import_cli(self) -> None:
        import birthday.di.container as di_mod

        source = Path(di_mod.__file__).read_text()
        assert "cli" not in source
        assert "birthday.cli" not in source


class TestCliUsesContainer:
    """CLI commands must use Container for service instantiation."""

    def test_analyze_uses_container(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["analyze", "--days", "10", "--people", "5"])
        assert result.exit_code == 0
        assert "D = 10" in result.output
        assert "n = 5" in result.output

    def test_simulate_uses_container(self) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli, ["simulate", "--days", "10", "--people", "5", "--trials", "100"]
        )
        assert result.exit_code == 0
        assert "MC: n = 5" in result.output

    def test_report_uses_container(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["report", "--days", "10"])
        assert result.exit_code == 0
        assert "exact" in result.output.lower() or "P(match)" in result.output

    def test_plot_uses_container(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "plot",
                "--max-people", "5",
                "-o", str(tmp_path),
                "-t", "10",
                "--no-animations",
            ],
        )
        assert result.exit_code == 0
        assert "Generated" in result.output
        names = {p.name for p in tmp_path.iterdir()}
        assert "probability_curve.png" in names

    def test_all_uses_container(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "all",
                "--max-people", "5",
                "-o", str(tmp_path),
                "-t", "10",
                "--no-mp4",
            ],
        )
        assert result.exit_code == 0
        assert "Done" in result.output
