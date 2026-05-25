# Graph Report - birthday-paradox  (2026-05-25)

## Corpus Check
- 43 files · ~102,230 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 579 nodes · 848 edges · 49 communities (42 shown, 7 thin omitted)
- Extraction: 68% EXTRACTED · 32% INFERRED · 0% AMBIGUOUS · INFERRED: 274 edges (avg confidence: 0.67)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3b5a8868`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]

## God Nodes (most connected - your core abstractions)
1. `BirthdayConfig` - 92 edges
2. `MatplotlibVisualizer` - 65 edges
3. `BirthdayProbability` - 64 edges
4. `AnimationWriter` - 38 edges
5. `Container` - 34 edges
6. `MonteCarloSimulator` - 33 edges
7. `ConsoleReporter` - 17 edges
8. `TestContainerOverrides` - 15 edges
9. `TestReadmeV11` - 15 edges
10. `prompt_hashes` - 14 edges

## Surprising Connections (you probably didn't know these)
- `config()` --calls--> `BirthdayConfig`  [INFERRED]
  tests/test_plots.py → src/birthday/core/config.py
- `viz()` --calls--> `MatplotlibVisualizer`  [INFERRED]
  tests/test_plots.py → src/birthday/visualization/matplotlib_viz.py
- `test_calls_prob_methods()` --calls--> `MatplotlibVisualizer`  [INFERRED]
  tests/test_plots.py → src/birthday/visualization/matplotlib_viz.py
- `test_max_n_respects_config()` --calls--> `MatplotlibVisualizer`  [INFERRED]
  tests/test_plots.py → src/birthday/visualization/matplotlib_viz.py
- `test_uses_probability_curve()` --calls--> `MatplotlibVisualizer`  [INFERRED]
  tests/test_plots.py → src/birthday/visualization/matplotlib_viz.py

## Communities (49 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (24): base_commit, cache_prewarmed, cache_ttl_probe, client_alive_at, codex_model, current_cycle, cycles, effort_hints (+16 more)

### Community 1 - "Community 1"
Cohesion: 0.15
Nodes (10): Overlay Monte Carlo empirical curve on the exact theoretical curve., Overlay Monte Carlo empirical curve on the exact theoretical curve., E[# matching pairs] vs n., E[# matching pairs] vs n., Histogram of the group-size index where the first collision appears., Histogram of the group-size index where the first collision appears., Absolute error |exact − Taylor approx| vs n., Generate every static plot and animation. (+2 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (30): analyze(), animate(), cli(), main(), plot(), Command-line interface for the Birthday Paradox analysis., Render a single animation by name (GIF + optional MP4)., Print a checkpoint table summarising the Birthday Paradox. (+22 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (34): BirthdayConfig, Immutable configuration for the Birthday Paradox model., Immutable configuration for the Birthday Paradox.      Attributes:         days_, BirthdayProbability, P(at least k people share a single birthday).          Closed-form is intractabl, Closed-form probability calculations for the Birthday Paradox.      Implements t, Exact P(all n birthdays distinct).          Uses log-gamma for numerical stabili, Exact P(at least one shared birthday). (+26 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (26): all(), Run analyze + plot + animations end-to-end., Run analyze + plot + animations end-to-end., CollisionCurve, Result containers for simulations and analyses., Outcome of a Monte Carlo run for a single group size.      Attributes:         g, Probability curve across group sizes.      Attributes:         group_sizes: Arra, SimulationResult (+18 more)

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (3): config(), Analytical probability formulas for the Birthday Paradox., Monte Carlo simulation of the Birthday Paradox.

### Community 6 - "Community 6"
Cohesion: 0.4
Nodes (5): repo, full, host, name, owner

### Community 11 - "Community 11"
Cohesion: 0.07
Nodes (14): Real file creation tests for dual format., TestIntegrationDualFormat, Tests for the AnimationWriter abstraction., TestAnimationWriterInit, TestDiscoverFfmpeg, TestGetWriter, TestSupports, TestTryFfmpeg (+6 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (33): Birthday Paradox, Build-up animation, code:block1 (D · (D-1) · (D-2) · ... · (D-n+1)        D!), code:bash (# Smaller pool (D = 16): collisions become near-certain fast), code:block11 (birthday-paradox/), code:block2 (P(match) = 1 − P(all distinct)), code:block3 (log P(no match) = lgamma(D + 1) − lgamma(D − n + 1) − n · lo), code:block4 (P(match) ≈ 1 − exp(−n(n−1) / (2D))) (+25 more)

### Community 13 - "Community 13"
Cohesion: 0.08
Nodes (7): Tests for CLI wiring of new visualizations., TestCliAllCommand, TestCliAnalyze, TestCliAnimate, TestCliPlotCommand, TestCliReport, TestCliSimulate

### Community 14 - "Community 14"
Cohesion: 0.09
Nodes (5): Tests for README v1.1 content., README file must exist., Validate v1.1 additions per issue #18 acceptance criteria., TestReadmeExists, TestReadmeV11

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (9): config(), Tests for dual-format animation output in MatplotlibVisualizer., When ffmpeg is unavailable, GIF is still produced., Each animation method should produce both .gif and .mp4., no_mp4=True should skip MP4 generation., TestDualFormatAnimationOutput, TestGracefulFfmpegFallback, TestNoMp4Flag (+1 more)

### Community 16 - "Community 16"
Cohesion: 0.11
Nodes (5): Tests for the GitHub Actions CI workflow., Workflow file must exist., Structure and commands inside ci.yml., TestCiWorkflowContent, TestCiWorkflowExists

### Community 17 - "Community 17"
Cohesion: 0.14
Nodes (14): prompt_hashes, prompt-cycle-specializer.md, prompt-optimize-requirements.md, prompt-phase-0-complexity.md, prompt-phase-1-planning.md, prompt-phase-2-batch-review.md, prompt-phase-3-implementation.md, prompt-phase-5-final-review.md (+6 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (3): Tests for the birthday animate CLI subcommand., birthday animate <name> renders a single animation., TestAnimateSubcommand

### Community 19 - "Community 19"
Cohesion: 0.15
Nodes (8): config(), Tests for static plot methods in MatplotlibVisualizer., test_calls_prob_methods(), test_max_error_below_threshold_for_d365(), test_max_n_respects_config(), test_uses_probability_curve(), TestPlotKCollisionCurves, viz()

### Community 20 - "Community 20"
Cohesion: 0.18
Nodes (7): GIF: probability curve drawing itself frame-by-frame., GIF: people enter a room one at a time, each gets a random birthday;         the, GIF: probability curve drawing itself frame-by-frame., GIF: people enter a room one at a time, each gets a random birthday;         the, GIF: running empirical estimate of P(match) for fixed n approaching theory., Save an animation using the configured writer; return path or None on failure., Save animation as GIF and optionally MP4; return all successful paths.

### Community 21 - "Community 21"
Cohesion: 0.18
Nodes (11): cache_read, cache_write, cache_write_1h, cache_write_5m, clear_events, compaction_events, input, num_turns (+3 more)

### Community 22 - "Community 22"
Cohesion: 0.27
Nodes (6): TestCreateAllProducesTenFiles, Verify MatplotlibVisualizer can use AnimationWriter without inline writer= strin, TestIntegrationWithMatplotlibVisualizer, MatplotlibVisualizer, Generate publication-quality plots and GIFs for the Birthday Paradox., Generate publication-quality plots and GIFs for the Birthday Paradox.

### Community 23 - "Community 23"
Cohesion: 0.22
Nodes (8): Acceptance criteria, Cycle 1 — Visualization v1.1, Following cycles, In scope, Objective, Out of scope, Preceding cycles, Project vision

### Community 24 - "Community 24"
Cohesion: 0.22
Nodes (8): Acceptance criteria, Cycle 2 — MP4 Export & CLI, Following cycles, In scope, Objective, Out of scope, Preceding cycles, Project vision

### Community 25 - "Community 25"
Cohesion: 0.22
Nodes (8): Acceptance criteria, Cycle 3 — Reporting, DI & Tests, Following cycles, In scope, Objective, Out of scope, Preceding cycles, Project vision

### Community 26 - "Community 26"
Cohesion: 0.22
Nodes (8): Acceptance criteria, Cycle 4 — CI & Documentation, Following cycles, In scope, Objective, Out of scope, Preceding cycles, Project vision

### Community 27 - "Community 27"
Cohesion: 0.22
Nodes (8): Additional Notes, Birthday Paradox — Probability Study & Video Simulations, code:block1 (birthday-paradox/), Description, Features, Non-functional Requirements, Project Structure, Tech Stack

### Community 28 - "Community 28"
Cohesion: 0.22
Nodes (9): phase8, attempt, ci_run_id, ci_status, finished_at, repair_attempts, started_at, status (+1 more)

### Community 29 - "Community 29"
Cohesion: 0.22
Nodes (5): config(), Integration tests for MatplotlibVisualizer.create_all batch output., create_all produces all expected PNG and GIF files with non-zero size., TestCreateAllBatch, viz()

### Community 30 - "Community 30"
Cohesion: 0.29
Nodes (3): Tests for .gitignore rules., Verify repository hygiene rules in .gitignore., TestGitignore

### Community 31 - "Community 31"
Cohesion: 0.33
Nodes (5): base_url, entry_cmd, requirements_hash, scenarios, tiers

### Community 32 - "Community 32"
Cohesion: 0.33
Nodes (3): Pre-compute k-collision probability curves for k = 2..5., P(≥ k share a birthday) vs n for k = 2..5., GIF: k-collision curves drawing themselves frame-by-frame.

## Knowledge Gaps
- **228 isolated node(s):** `mode`, `started_at`, `updated_at`, `current_cycle`, `cycles` (+223 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BirthdayConfig` connect `Community 3` to `Community 33`, `Community 34`, `Community 2`, `Community 4`, `Community 11`, `Community 13`, `Community 15`, `Community 19`, `Community 22`, `Community 29`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `MatplotlibVisualizer` connect `Community 22` to `Community 32`, `Community 1`, `Community 33`, `Community 34`, `Community 2`, `Community 3`, `Community 4`, `Community 7`, `Community 11`, `Community 13`, `Community 15`, `Community 19`, `Community 20`, `Community 29`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Why does `BirthdayProbability` connect `Community 3` to `Community 33`, `Community 34`, `Community 2`, `Community 4`, `Community 5`, `Community 11`, `Community 19`, `Community 22`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 89 inferred relationships involving `BirthdayConfig` (e.g. with `TestPlotKCollisionCurves` and `TestAnimateKCollision`) actually correct?**
  _`BirthdayConfig` has 89 INFERRED edges - model-reasoned connections that need verification._
- **Are the 45 inferred relationships involving `MatplotlibVisualizer` (e.g. with `TestPlotKCollisionCurves` and `TestAnimateKCollision`) actually correct?**
  _`MatplotlibVisualizer` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `BirthdayProbability` (e.g. with `.__init__()` and `TestPlotKCollisionCurves`) actually correct?**
  _`BirthdayProbability` has 54 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `AnimationWriter` (e.g. with `TestPlotKCollisionCurves` and `TestAnimateKCollision`) actually correct?**
  _`AnimationWriter` has 32 INFERRED edges - model-reasoned connections that need verification._