# Cycle 4 — CI & Documentation

## Objective
Add a GitHub Actions workflow that runs lint, mypy, and pytest across Python 3.10/3.11/3.12, uploads release artifacts, and update README to v1.1 with MP4 links and installation notes for `imageio-ffmpeg`.

## Project vision
A scientific Python package that quantifies the Birthday Paradox through exact combinatorics, asymptotic approximation, and Monte Carlo simulation, rendering results as publication-quality static plots plus animated GIFs and MP4 videos. Cycles 1–3 complete all code, visualizations, CLI, reporting, DI, and tests. This cycle closes the project with continuous integration and documentation.

## Preceding cycles
- v1.0 shipped core modules, 4 PNGs, 3 GIFs, and basic CLI
- Cycle 1 added `writers.py`, k-collision plots/animation, and approximation-error plot
- Cycle 2 added MP4 export, `birthday animate <name>`, `--no-mp4`, and ffmpeg fallback
- Cycle 3 added console reporting, DI container, and full pytest suite with coverage

## Following cycles
None — this is the final cycle.

## In scope
- `.github/workflows/ci.yml` — matrix on `python-version: ["3.10", "3.11", "3.12"]`; steps: checkout → setup-python → `pip install -e .[dev]` → `ruff check` → `mypy src/` → `pytest --cov`
- Release job triggered on tagged releases: run `birthday all` and upload `output/*.{png,gif,mp4}` as release artifacts
- README v1.1 updates: embed MP4 links pointing to GitHub Release assets, document `imageio-ffmpeg` installation, update usage examples to include `birthday animate`
- `.gitignore` update: ensure `output/*.mp4` is ignored so large binaries are not committed
- Ensure `LICENSE` remains MIT

## Out of scope
- New code features, plot types, or animation types (Cycles 1–2)
- Console reporting, DI container, or test files (Cycle 3)
- Non-uniform birthday distributions, leap-year modelling, or Plotly backend (v2.0 epics)

## Acceptance criteria
- CI passes on all three Python versions with zero lint, mypy, or test failures
- Tagged release runs `birthday all` and attaches all PNG, GIF, and MP4 files to the GitHub Release
- README documents how to install with `imageio-ffmpeg`, how to use `birthday animate`, and links to hosted MP4s
- `.gitignore` excludes `output/*.mp4`
- No large media files are committed to the repository
