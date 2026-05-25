"""Command-line interface for the Birthday Paradox analysis."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click

from birthday.core.config import BirthdayConfig
from birthday.math.probability import BirthdayProbability
from birthday.simulation.monte_carlo import MonteCarloSimulator
from birthday.visualization.matplotlib_viz import MatplotlibVisualizer


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )


@click.group()
@click.version_option(version="1.0.0", prog_name="birthday")
@click.option("-v", "--verbose", is_flag=True, help="Verbose logs")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Birthday Paradox: analytical + Monte Carlo study with animated plots."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    _setup_logging(verbose)


def _config_options(f):  # type: ignore[no-untyped-def]
    f = click.option("-D", "--days", default=365, show_default=True, help="Days per year")(f)
    f = click.option("--max-people", default=100, show_default=True, help="Max group size")(f)
    return f


@cli.command()
@_config_options
@click.option("-n", "--people", default=23, show_default=True, help="Group size to analyse")
def analyze(days: int, max_people: int, people: int) -> None:
    """Print analytical probabilities for a given group size."""
    config = BirthdayConfig(days_per_year=days, max_people=max_people)
    prob = BirthdayProbability(config)
    exact = prob.prob_match_exact(people)
    approx = prob.prob_match_approx(people)
    expected = prob.expected_collisions(people)
    unique = prob.expected_unique_birthdays(people)
    median = prob.median_group_size()

    click.echo(f"\nBirthday Paradox — D = {days}, n = {people}")
    click.echo("-" * 50)
    click.echo(f"  P(match)  exact:        {exact:.6f}")
    click.echo(f"  P(match)  Taylor:       {approx:.6f}")
    click.echo(f"  E[matching pairs]:      {expected:.4f}")
    click.echo(f"  E[distinct birthdays]:  {unique:.4f}")
    click.echo(f"  Smallest n with P≥0.5:  {median}")
    click.echo("")


@cli.command()
@_config_options
@click.option("-n", "--people", default=23, show_default=True, help="Group size")
@click.option("-t", "--trials", default=100_000, show_default=True, help="MC trials")
@click.option("--seed", default=42, show_default=True, help="Random seed")
def simulate(days: int, max_people: int, people: int, trials: int, seed: int) -> None:
    """Run a Monte Carlo simulation and compare against theory."""
    config = BirthdayConfig(days_per_year=days, max_people=max_people)
    sim = MonteCarloSimulator(config, seed=seed)
    prob = BirthdayProbability(config)

    result = sim.simulate_group(people, trials)
    theoretical = prob.prob_match_exact(people)
    click.echo(f"\nMC: n = {people}, trials = {trials:,}, seed = {seed}")
    click.echo("-" * 50)
    click.echo(f"  Empirical P(match):  {result.empirical_probability:.6f}")
    click.echo(f"  Theoretical:         {theoretical:.6f}")
    click.echo(
        f"  Error:               {result.empirical_probability - theoretical:+.6f}"
    )
    click.echo("")


@cli.command()
@_config_options
@click.option(
    "-o", "--output", type=click.Path(path_type=Path), default="output", show_default=True,
)
@click.option("-t", "--trials", default=5000, show_default=True, help="MC trials for plots")
@click.option("--seed", default=42, show_default=True)
@click.option("--no-animations", is_flag=True, help="Skip GIF animations")
@click.option("--no-mp4", is_flag=True, help="Skip MP4 animations")
def plot(
    days: int, max_people: int, output: Path, trials: int, seed: int,
    no_animations: bool, no_mp4: bool,
) -> None:
    """Generate all PNG plots (and GIF animations unless --no-animations)."""
    config = BirthdayConfig(days_per_year=days, max_people=max_people)
    viz = MatplotlibVisualizer(config, output_dir=output, seed=seed)

    paths: list[Path] = []
    for p in (
        viz.plot_probability_curve(),
        viz.plot_simulation_vs_theory(n_trials=trials),
        viz.plot_expected_collisions(),
        viz.plot_first_collision_distribution(n_trials=max(trials, 20000)),
        viz.plot_k_collision_curves(n_trials=max(trials, 50000)),
        viz.plot_approximation_error(),
    ):
        if p is not None:
            paths.append(p)

    if not no_animations:
        for method_paths in (
            viz.animate_probability_buildup(no_mp4=no_mp4),
            viz.animate_room_filling(no_mp4=no_mp4),
            viz.animate_simulation_convergence(max_trials=trials, no_mp4=no_mp4),
            viz.animate_k_collision(n_trials=trials, no_mp4=no_mp4),
        ):
            paths.extend(method_paths)

    click.echo("")
    click.echo(f"Generated {len(paths)} files in {output}:")
    for p in paths:
        click.echo(f"  • {p.name}")
    click.echo("")


@cli.command()
@_config_options
@click.option(
    "-o", "--output", type=click.Path(path_type=Path), default="output", show_default=True,
)
@click.option("-t", "--trials", default=5000, show_default=True)
@click.option("--seed", default=42, show_default=True)
@click.option("--no-mp4", is_flag=True, help="Skip MP4 animations")
def all(days: int, max_people: int, output: Path, trials: int, seed: int, no_mp4: bool) -> None:
    """Run analyze + plot + animations end-to-end."""
    config = BirthdayConfig(days_per_year=days, max_people=max_people)
    prob = BirthdayProbability(config)
    viz = MatplotlibVisualizer(config, output_dir=output, seed=seed)

    click.echo(f"\nMedian (50%) group size: {prob.median_group_size()}")
    click.echo(f"Generating plots + animations in {output} ...\n")
    produced = viz.create_all(n_trials=trials, no_mp4=no_mp4)
    click.echo("")
    click.echo(f"Done — {len(produced)} files written:")
    for p in produced:
        click.echo(f"  • {p.name}")
    click.echo("")


def main() -> None:
    cli(obj={})


if __name__ == "__main__":
    main()
