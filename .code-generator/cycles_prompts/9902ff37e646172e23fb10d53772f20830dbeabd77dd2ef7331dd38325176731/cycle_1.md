# Cycle 1 — Visualization v1.1

## Objective
Add the two missing static plots (`k_collision_curves.png`, `approximation_error.png`), the missing `k_collision_animation.gif`, and introduce `visualization/writers.py` as a thin abstraction that selects `PillowWriter` or `FFMpegWriter` based on file extension.

## Project vision
A scientific Python package that quantifies the Birthday Paradox through exact combinatorics, asymptotic approximation, and Monte Carlo simulation, rendering results as publication-quality static plots plus animated GIFs and MP4 videos. v1.0 already ships the core math, simulation, four static PNGs, and three GIF animations. v1.1 fills the remaining visualization gaps and prepares a writer abstraction so MP4 export can be wired in the next cycle.

## Preceding cycles
v1.0 (pre-cycle) delivered:
- `core/config.py` — `BirthdayConfig` frozen dataclass with validators and `pigeonhole_bound`
- `core/models.py` — `SimulationResult` and `CollisionCurve` dataclasses
- `math/probability.py` — `BirthdayProbability` with exact, approx, expected values, median, and `prob_at_least_k_share` (k-collision math exists but has no plots yet)
- `simulation/monte_carlo.py` — `MonteCarloSimulator` with `simulate_group`, `simulate_curve`, `simulate_first_collision_distribution`
- `visualization/matplotlib_viz.py` — `MatplotlibVisualizer` producing 4 PNGs (`probability_curve`, `simulation_vs_theory`, `expected_collisions`, `first_collision_distribution`) and 3 GIFs (`probability_buildup`, `room_filling`, `convergence`)
- `cli.py` — Click commands `analyze`, `simulate`, `plot`, `all`
- `pyproject.toml` — v1.0.0 with dependencies through `pillow>=10.0.0`

## Following cycles
- Cycle 2 will wire MP4 export into the CLI, add `birthday animate <name>`, and implement `--no-mp4`
- Cycle 3 will add console reporting, DI container, and the full pytest suite
- Cycle 4 will add GitHub Actions CI and README v1.1 updates with MP4 links

## In scope
- `visualization/writers.py` — `AnimationWriter` class that picks `PillowWriter` for `.gif` and `FFMpegWriter` for `.mp4`, with a `supports(extension: str) -> bool` check and graceful skip when ffmpeg is missing
- `MatplotlibVisualizer.plot_k_collision_curves()` — static PNG showing `P(≥ k share)` vs `n` for `k ∈ {2, 3, 4, 5}`; uses Monte Carlo for `k ≥ 3` with ≥50 000 trials
- `MatplotlibVisualizer.plot_approximation_error()` — static PNG of `|exact − approx|` vs `n`, documenting max abs error < 0.012 for `D = 365`, `n ≤ 100`
- `MatplotlibVisualizer.animate_k_collision()` — GIF where curves for `k ∈ {2,3,4,5}` draw in parallel frame-by-frame
- Update `MatplotlibVisualizer.create_all()` to include the two new PNGs and the new GIF
- Ensure all new plots use Okabe-Ito or `viridis`, minimum 11 pt font, title/labels/legend/gridlines

## Out of scope
- CLI `--no-mp4` flag or `birthday animate <name>` subcommand (Cycle 2)
- Actual MP4 file generation (Cycle 2)
- Console reporting tables (Cycle 3)
- DI container (Cycle 3)
- Test files (Cycle 3)
- CI workflow (Cycle 4)

## Acceptance criteria
- `k_collision_curves.png` renders four curves (k = 2 exact, k = 3..5 via MC) with legend and grid
- `approximation_error.png` shows absolute error between exact and Taylor curves; documented max error < 0.012
- `k_collision_animation.gif` draws all four curves in parallel using `FuncAnimation` + `PillowWriter`
- `writers.py` exposes a clean wrapper that can be imported and used by `MatplotlibVisualizer` methods without inline `writer=` strings
- All visualizations remain colour-blind safe and maintain the existing `seaborn-v0_8-whitegrid` style at 150 DPI
