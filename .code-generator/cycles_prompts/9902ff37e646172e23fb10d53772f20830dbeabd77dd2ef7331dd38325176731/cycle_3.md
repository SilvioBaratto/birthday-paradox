# Cycle 3 — Reporting, DI & Tests

## Objective
Deliver pretty-printed console reporting tables, a dependency injection container that wires all services, and a comprehensive pytest suite with ≥85% line coverage on `math/`, `simulation/`, `core/` and ≥70% on `visualization/`.

## Project vision
A scientific Python package that quantifies the Birthday Paradox through exact combinatorics, asymptotic approximation, and Monte Carlo simulation, rendering results as publication-quality static plots plus animated GIFs and MP4 videos. Cycles 1–2 complete all visual outputs and CLI commands. This cycle adds internal quality infrastructure: reporting, DI, and tests.

## Preceding cycles
- v1.0 shipped core modules, 4 PNGs, 3 GIFs, and basic CLI (`analyze`, `simulate`, `plot`, `all`)
- Cycle 1 added `writers.py`, k-collision plots/animation, and approximation-error plot
- Cycle 2 added MP4 export, `birthday animate <name>`, `--no-mp4`, and ffmpeg fallback

## Following cycles
- Cycle 4 will add GitHub Actions CI and README v1.1 updates with MP4 links

## In scope
- `reporting/console.py` — pretty-printed table for standard checkpoints `[5, 10, 23, 30, 50, 70, 100]` showing `n`, exact `P(match)`, approx `P(match)`, `E[matching pairs]`, and residual
- `di/container.py` — DI container wiring `BirthdayConfig` → `BirthdayProbability` → `MonteCarloSimulator` → `MatplotlibVisualizer`; supports swapping the visualizer (Plotly backend planned for v2.0)
- `tests/test_probability.py` — verify known values (`P(23) ≈ 0.5073`, `P(50) ≈ 0.9704`, `P(70) ≈ 0.99916`), monotonicity, boundary conditions (`P(0)=0`, `P(D+1)=1`)
- `tests/test_simulation.py` — verify empirical converges to theoretical within `4σ` for `n ∈ {23, 50, 70}` at `trials = 20_000` with fixed `seed=42`
- `tests/test_visualization.py` — assert files exist with non-zero size after `create_all()`; do not assert on pixel content
- `tests/test_cli.py` — `click.testing.CliRunner` smoke tests for each subcommand (`analyze`, `simulate`, `plot`, `all`, `animate`)
- Ensure `pytest-cov` is configured and all tests use `seed=42` for reproducibility

## Out of scope
- New plot or animation types (Cycle 1)
- MP4 export logic or CLI `--no-mp4` (Cycle 2)
- GitHub Actions workflow (Cycle 4)
- README updates beyond what is needed for test instructions

## Acceptance criteria
- Console table prints cleanly at the standard checkpoints with exact, approx, expected-pairs, and residual columns
- DI container resolves `MatplotlibVisualizer` from a `BirthdayConfig` without circular imports
- `test_probability.py` passes with assertions on exact values, monotonicity, and boundaries
- `test_simulation.py` passes with empirical within `4σ` of theory at the tested group sizes
- `test_visualization.py` passes by asserting file existence and non-zero size after batch generation
- `test_cli.py` passes by smoke-testing every subcommand via `CliRunner`
- Line coverage ≥ 85% on `math/`, `simulation/`, `core/` and ≥ 70% on `visualization/`
- `mypy --strict` and `ruff check` continue to pass with zero errors
