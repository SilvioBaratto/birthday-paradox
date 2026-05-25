# Cycle 2 — MP4 Export & CLI

## Objective
Export all four animations to MP4 at 1080p / 30 fps via `matplotlib.animation.FFMpegWriter`, add the `birthday animate <name>` subcommand, introduce `--no-mp4` flags, and implement graceful fallback when ffmpeg is not on PATH.

## Project vision
A scientific Python package that quantifies the Birthday Paradox through exact combinatorics, asymptotic approximation, and Monte Carlo simulation, rendering results as publication-quality static plots plus animated GIFs and MP4 videos. Cycle 1 completes the missing visualizations and writer abstraction. This cycle wires MP4 export into the CLI so every animation has parity across GIF and MP4 formats.

## Preceding cycles
- v1.0 shipped `MatplotlibVisualizer` with 3 GIFs (`probability_buildup`, `room_filling`, `convergence`) and 4 PNGs
- Cycle 1 adds `writers.py`, the `k_collision_animation.gif`, `k_collision_curves.png`, and `approximation_error.png`

## Following cycles
- Cycle 3 will add console reporting, DI container, and the full pytest suite
- Cycle 4 will add GitHub Actions CI and README v1.1 updates with MP4 links

## In scope
- Update `MatplotlibVisualizer` so every animation method (`animate_probability_buildup`, `animate_room_filling`, `animate_simulation_convergence`, `animate_k_collision`) can emit both `.gif` and `.mp4` by calling the writer wrapper twice
- Add `imageio-ffmpeg>=0.4` to `pyproject.toml` dependencies
- Add `--no-mp4` flag to `birthday plot` and `birthday all`
- Add `birthday animate <name>` CLI subcommand where `<name>` is one of `probability_buildup`, `room_filling`, `convergence`, `k_collision`
- Graceful fallback: if ffmpeg is missing, log a warning and skip MP4 (GIF is still produced)
- MP4 settings: 1080p, 30 fps, constant bitrate ≥ 4 Mbps, H.264 codec, yuv420p pixel format
- Update `create_all()` to produce both formats unless `--no-mp4` is set

## Out of scope
- New plot types or new animation concepts (Cycle 1)
- Console reporting tables (Cycle 3)
- DI container (Cycle 3)
- Test files (Cycle 3)
- CI workflow (Cycle 4)
- README updates for MP4 links (Cycle 4)

## Acceptance criteria
- `probability_buildup.mp4`, `room_filling.mp4`, `convergence.mp4`, and `k_collision_animation.mp4` are generated when ffmpeg is available
- Filenames mirror their GIF counterparts exactly (same stem, `.mp4` extension)
- `birthday animate room_filling -o output` renders only that one animation in both GIF and MP4
- `--no-mp4` in `plot` and `all` suppresses MP4 generation without affecting PNG or GIF
- Missing ffmpeg logs a clear warning and does not crash the CLI
- `pyproject.toml` includes `imageio-ffmpeg>=0.4` in main dependencies
