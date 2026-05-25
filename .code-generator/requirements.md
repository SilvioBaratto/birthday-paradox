# Birthday Paradox — Probability Study & Video Simulations

## Description

A scientific Python package that quantifies the **Birthday Paradox** through three lenses — exact combinatorics, asymptotic (Taylor) approximation, and Monte Carlo simulation — and renders the results as publication-quality static plots **plus** animated GIFs and MP4 videos. The project is aimed at students, educators, and probability enthusiasts who want a runnable, mathematically rigorous, and visually compelling exploration of why "23 people = 50% match" is true.

The codebase follows SOLID principles, uses a `src/`-layout, strict type checking (`mypy --strict`), and is delivered as both a Python library (`birthday.*`) and a Click-based CLI (`birthday` entrypoint).

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: None — pure scientific Python library + Click CLI
- **Core libraries**:
  - `numpy>=1.24` — vectorized Monte Carlo
  - `scipy>=1.10` — `gammaln` for numerically stable factorials
  - `matplotlib>=3.7` — plots + `FuncAnimation` for GIF/MP4
  - `pillow>=10` — GIF writer backend
  - `imageio-ffmpeg>=0.4` — MP4 writer backend (FFmpeg auto-bundled)
  - `click>=8.1` — CLI
- **Database**: none (pure computation; outputs go to filesystem under `output/`)
- **Deploy**: local pip install (`pip install -e .`); optional GitHub Release with pre-rendered videos
- **Tests**: `pytest` + `pytest-cov` (≥ 85% line coverage on `math/`, `simulation/`, `core/`)
- **Lint / format**: `ruff` (E, F, I, N, W, UP, B, C4, SIM)
- **Type check**: `mypy --strict`
- **CI**: GitHub Actions matrix on Python 3.10 / 3.11 / 3.12 running lint + mypy + pytest

## Features

Each feature below becomes a GitHub Issue and is implemented behind a Click subcommand or a public class.

1. **Frozen configuration model** (`core/config.py`)
   - `BirthdayConfig(days_per_year=365, max_people=100)` as a frozen `@dataclass(slots=True)`.
   - Validators: `days_per_year >= 2`, `max_people >= 2`.
   - Property `pigeonhole_bound` returning `D + 1`.

2. **Exact closed-form probability** (`math/probability.py`)
   - `prob_no_match_exact(n)` computed in log-space via `scipy.special.gammaln` for stability up to `D=10_000`.
   - `prob_match_exact(n) = 1 - prob_no_match_exact(n)`.
   - Unit tests verify known values: `P(23) ≈ 0.5073`, `P(50) ≈ 0.9704`, `P(70) ≈ 0.99916`.

3. **Taylor / Poisson approximation**
   - `prob_match_approx(n) = 1 - exp(-n(n-1)/(2D))`.
   - Document and visualize the error vs the exact curve (max abs error < 0.012 for `D=365`, `n ≤ 100`).

4. **Expected-value quantities**
   - `expected_collisions(n) = n(n-1)/(2D)` (expected matching pairs).
   - `expected_unique_birthdays(n) = D * (1 - (1 - 1/D)^n)` (coupon-collector counterpart).
   - `median_group_size()` returning smallest `n` with `P(match) >= 0.5` (verified by walking around the closed-form estimate `ceil((1 + sqrt(1 + 8 D ln 2))/2)`).

5. **k-way collision (generalised paradox)**
   - `prob_at_least_k_share(n, k, samples)` — for `k=2` returns the exact value; for `k>=3` falls back to Monte Carlo because no closed form exists.
   - Plot of `P(≥ k share)` vs `n` for `k ∈ {2, 3, 4, 5}`.

6. **Vectorized Monte Carlo simulator** (`simulation/monte_carlo.py`)
   - `MonteCarloSimulator(config, seed)`.
   - `simulate_group(n, trials)` returning a `SimulationResult` with empirical probability and per-trial first-collision index.
   - `simulate_curve(group_sizes, trials)` — single batch of size `max(group_sizes)` reused across all `n` for efficiency.
   - `simulate_first_collision_distribution(max_people, trials)`.
   - Reproducible via `numpy.random.default_rng(seed)`.

7. **Static plots (PNG, 150 DPI)** (`visualization/matplotlib_viz.py`)
   - `probability_curve.png` — exact + Taylor curves, 50% / 99% thresholds, median `n` marker.
   - `simulation_vs_theory.png` — two-panel: empirical scatter on exact theory + residual bar chart.
   - `expected_collisions.png` — two-panel: E[matching pairs] and E[distinct birthdays].
   - `first_collision_distribution.png` — MC histogram overlaid with analytical PMF.
   - `k_collision_curves.png` — `P(≥ k share)` for `k ∈ {2,3,4,5}` (new in v1.1).
   - `approximation_error.png` — `|exact − approx|` vs `n` (new in v1.1).

8. **Animations — GIF (PillowWriter)**
   - `probability_buildup.gif` — exact + approx curves drawn frame-by-frame, orange marker tracks current `n`, callout highlights when the 50% threshold is crossed.
   - `room_filling.gif` — people enter a ring one at a time, each labelled with their birthday; collision pair flashes yellow/red; right panel shows running `P(match)` so far.
   - `convergence.gif` — running empirical estimate for fixed `n=23` over up to `max_trials` trials; horizontal red line = exact value.
   - `k_collision_animation.gif` — curves for `k ∈ {2,3,4,5}` drawing in parallel (new in v1.1).

9. **Animations — MP4 (ffmpeg)** *(new in v1.1; must be parity-complete with the GIFs)*
   - Every animation listed in (8) must also export to MP4 at 1080p / 30 fps using `matplotlib.animation.FFMpegWriter`.
   - Filenames mirror GIFs: `probability_buildup.mp4`, `room_filling.mp4`, `convergence.mp4`, `k_collision_animation.mp4`.
   - Constant bitrate ≥ 4 Mbps, H.264 codec, yuv420p pixel format (max compatibility).
   - Fallback: if `ffmpeg` is missing, log a warning and skip MP4 (GIF still produced).

10. **CLI (`birthday`)** (`cli.py`, Click)
    - `birthday analyze -n 23 [-D 365]` — print exact, approx, expected-pairs, expected-distinct, median `n`.
    - `birthday simulate -n 23 -t 100000 --seed 42` — print empirical vs theoretical and the error.
    - `birthday plot [--no-animations] [--no-mp4] -o output -t 5000` — generate PNGs and optionally GIFs/MP4s.
    - `birthday all -t 5000 -o output` — analyze + plot + every animation in both GIF and MP4.
    - `birthday animate <name>` — render a single animation by name (e.g. `room_filling`, `convergence`).
    - `--verbose` flag enabling DEBUG-level logging.

11. **Console reporting** (`reporting/console.py`)
    - Pretty-printed table summarising `n`, exact, approx, expected-pairs, residual at standard checkpoints `[5, 10, 23, 30, 50, 70, 100]`.

12. **Dependency injection container** (`di/container.py`)
    - Wires `BirthdayConfig` → `BirthdayProbability` → `MonteCarloSimulator` → `MatplotlibVisualizer` → CLI commands.
    - Allows swapping the visualizer (Plotly backend planned for v2.0).

13. **Tests** (`tests/`)
    - `test_probability.py` — closed-form values, monotonicity (`P(n)` non-decreasing in `n`), boundary conditions (`P(0)=0`, `P(D+1)=1`).
    - `test_simulation.py` — empirical converges to theoretical within `4σ` for `n∈{23,50,70}` at `trials=20_000`.
    - `test_visualization.py` — assert files exist with non-zero size after `create_all()`; do **not** assert on pixel content.
    - `test_cli.py` — `click.testing.CliRunner`, smoke-test each subcommand.
    - Reproducibility: fix `seed=42` everywhere in tests.

14. **README** (already implemented at v1.0, extend in v1.1)
    - Embed PNG plots and GIFs.
    - Math write-up in `Probability Formulas` section with LaTeX-rendered equations.
    - Installation, usage examples (including custom `D`), project layout, license.
    - v1.1: link to MP4 videos hosted in GitHub Release.

15. **GitHub Actions CI** (`.github/workflows/ci.yml`)
    - Matrix on `python-version: ["3.10", "3.11", "3.12"]`.
    - Steps: checkout → setup-python → `pip install -e .[dev]` → `ruff check` → `mypy src/` → `pytest --cov`.
    - On tagged release: also run `birthday all` and upload `output/*.{png,gif,mp4}` as release artifacts.

## Non-functional Requirements

- **Performance**
  - `birthday all -t 5000` must complete in under 60 s on Apple M-series / mid-range x86.
  - Monte Carlo for `n=23, trials=100_000` under 2 s (vectorized numpy, no Python loops in the hot path of `simulate_curve`).
  - GIF rendering ≤ 5 s per animation; MP4 ≤ 8 s per animation at 1080p / 30 fps.

- **Numerical accuracy**
  - All closed-form probabilities accurate to `1e-12` for `D ≤ 10_000`, `n ≤ D`.
  - MC empirical estimates within `4 · sqrt(p(1-p)/trials)` of theory at any tested `n`.

- **Reproducibility**
  - All randomness routed through `numpy.random.default_rng(seed)`; CLI exposes `--seed` everywhere.
  - Same seed + same inputs → byte-identical PNG / GIF outputs (where matplotlib permits).

- **Type safety**
  - `mypy --strict` passes with zero errors.
  - Public APIs fully annotated; `from __future__ import annotations` everywhere.

- **Code quality**
  - SOLID: each module has a single responsibility (math, simulation, visualization, CLI, reporting, DI are all separate packages).
  - No circular imports.
  - `ruff check` passes with zero warnings.
  - `__slots__` on all dataclasses and core service classes for memory efficiency.

- **Test coverage**
  - ≥ 85% line coverage on `math/`, `simulation/`, `core/`.
  - ≥ 70% on `visualization/` (skip pixel-level assertions).

- **Accessibility / inclusivity of plots**
  - All plots colour-blind safe (use Okabe-Ito palette or `viridis` for sequential).
  - Minimum font size 11 pt.
  - Every figure has a title, axis labels, legend, and gridlines.

- **Cross-platform**
  - macOS, Linux, Windows (CI runs all three for the release build).
  - No hardcoded path separators (`pathlib.Path` everywhere).

- **Logging**
  - `logging.getLogger(__name__)` per module.
  - CLI controls log level via `-v / --verbose`.

## Project Structure

```
birthday-paradox/
├── pyproject.toml
├── requirements.txt
├── README.md
├── LICENSE
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── birthday/
│       ├── __init__.py
│       ├── cli.py                          # Click entrypoint
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py                   # BirthdayConfig (frozen dataclass)
│       │   └── models.py                   # SimulationResult, CollisionCurve
│       ├── math/
│       │   ├── __init__.py
│       │   └── probability.py              # exact, approx, expected, k-share
│       ├── simulation/
│       │   ├── __init__.py
│       │   └── monte_carlo.py              # MonteCarloSimulator
│       ├── visualization/
│       │   ├── __init__.py
│       │   ├── matplotlib_viz.py           # PNG + GIF + MP4
│       │   └── writers.py                  # Pillow + FFMpeg writer wrappers
│       ├── reporting/
│       │   ├── __init__.py
│       │   └── console.py                  # pretty-printed tables
│       └── di/
│           ├── __init__.py
│           └── container.py                # service wiring
├── tests/
│   ├── __init__.py
│   ├── test_probability.py
│   ├── test_simulation.py
│   ├── test_visualization.py
│   └── test_cli.py
└── output/                                 # generated PNG / GIF / MP4 (gitignored except .gitkeep)
```

## Additional Notes

- **Animation strategy**: every animation must be implementable in **both** GIF (`PillowWriter`) and MP4 (`FFMpegWriter`). A thin wrapper in `visualization/writers.py` selects the right writer based on the target file extension and gracefully skips MP4 when `ffmpeg` is not on the system PATH.
- **Reference project**: the architecture mirrors [`SilvioBaratto/bingo-probability-analysis`](https://github.com/SilvioBaratto/bingo-probability-analysis) — same SOLID layout, same `src/` package style, same use of `FuncAnimation` + `PillowWriter`. Reuse the visual style (`seaborn-v0_8-whitegrid`, DPI 150).
- **k-collision intractability**: closed-form formulas for `P(≥ k share)` with `k ≥ 3` involve Stirling numbers of the second kind and are numerically painful for `D = 365`. Use Monte Carlo with ≥ 50 000 trials and document the convergence rate.
- **MP4 distribution**: do **not** commit large `.mp4` files to git. Add `output/*.mp4` to `.gitignore` and instead upload them to GitHub Releases or host elsewhere. Embed only GIF previews in the README.
- **Educational angle**: the README should explicitly walk through the "why 23?" intuition using the pairs argument (`C(23,2)=253`), not just present the formulas — the project's value is pedagogical.
- **Extensions deliberately out of scope (v1.x)**: leap-year aware modelling with February 29, non-uniform birthday distributions (real-world data shows clustering around September), partial-match generalisation (people sharing birthday *month* only). Track these as separate epics for v2.0.
- **Versioning**: SemVer. v1.0 already ships PNG + GIF outputs and the closed-form math. v1.1 adds MP4 export, k-collision plots, and CI. v2.0 reserved for the Plotly interactive backend and non-uniform priors.
- **Licence**: MIT.
