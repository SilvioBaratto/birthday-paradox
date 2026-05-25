"""Matplotlib visualizations and animations for the Birthday Paradox."""

from __future__ import annotations

import contextlib
import logging
import warnings
from pathlib import Path
from typing import Any

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from numpy.typing import NDArray

from birthday.core.config import BirthdayConfig
from birthday.math.probability import BirthdayProbability
from birthday.simulation.monte_carlo import MonteCarloSimulator
from birthday.visualization.writers import AnimationWriter

logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")


class MatplotlibVisualizer:
    """Generate publication-quality plots and GIFs for the Birthday Paradox."""

    __slots__ = ("_config", "_output_dir", "_style", "_dpi", "_prob", "_sim", "_animation_writer")

    DEFAULT_DPI: int = 150
    DEFAULT_STYLE: str = "seaborn-v0_8-whitegrid"

    def __init__(
        self,
        config: BirthdayConfig,
        output_dir: Path | str = "output",
        seed: int | None = 42,
        style: str | None = None,
        dpi: int | None = None,
    ) -> None:
        self._config = config
        self._output_dir = Path(output_dir)
        self._style = style or self.DEFAULT_STYLE
        self._dpi = dpi or self.DEFAULT_DPI
        self._prob = BirthdayProbability(config)
        self._sim = MonteCarloSimulator(config, seed=seed)
        self._animation_writer = AnimationWriter()
        self._output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def output_dir(self) -> Path:
        return self._output_dir

    def _apply_style(self) -> None:
        with contextlib.suppress(OSError):
            plt.style.use(self._style)

    def _save_animation(
        self, anim: animation.FuncAnimation, path: Path, fps: int,
    ) -> Path | None:
        """Save an animation using the configured writer; return path or None on failure."""
        writer = self._animation_writer.get_writer(path, fps=fps)
        if writer is None:
            return None
        try:
            anim.save(str(path), writer=writer)
            logger.info(f"Saved {path}")
            return path
        except Exception as exc:
            logger.warning(f"Could not save animation: {exc}")
            return None

    # ------------------------------------------------------------------
    # Static plots
    # ------------------------------------------------------------------

    def plot_probability_curve(self, save: bool = True, show: bool = False) -> Path | None:
        """P(match) vs n: exact, Taylor approximation, 50%/99% reference lines."""
        self._apply_style()
        ns, exact, approx = self._prob.probability_curve()
        median_n = self._prob.median_group_size()

        fig, ax = plt.subplots(figsize=(11, 6.5))
        ax.plot(ns, exact, "b-", lw=2.2, label="Exact: $1 - \\frac{D!}{D^n (D-n)!}$")
        ax.plot(
            ns, approx, "r--", lw=1.8, alpha=0.85,
            label="Approx: $1 - e^{-n(n-1)/2D}$",
        )
        ax.axhline(0.5, color="green", ls=":", alpha=0.7, label="50% threshold")
        ax.axhline(0.99, color="purple", ls=":", alpha=0.5, label="99% threshold")
        ax.axvline(
            median_n, color="green", ls="--", alpha=0.6,
            label=f"n = {median_n} (50% point)",
        )
        ax.set_xlabel("Number of people in the room (n)", fontsize=12)
        ax.set_ylabel("P(at least one shared birthday)", fontsize=12)
        ax.set_title(
            f"The Birthday Paradox  (D = {self._config.days_per_year})",
            fontsize=14,
        )
        ax.set_xlim(1, ns.max())
        ax.set_ylim(0, 1.02)
        ax.legend(loc="lower right", fontsize=10)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        path: Path | None = None
        if save:
            path = self._output_dir / "probability_curve.png"
            fig.savefig(path, dpi=self._dpi, bbox_inches="tight")
            logger.info(f"Saved {path}")
        if show:
            plt.show()
        plt.close(fig)
        return path

    def plot_simulation_vs_theory(
        self, n_trials: int = 5000, save: bool = True, show: bool = False,
    ) -> Path | None:
        """Overlay Monte Carlo empirical curve on the exact theoretical curve."""
        self._apply_style()
        ns, exact, approx = self._prob.probability_curve()
        empirical = self._sim.simulate_curve(ns, n_trials)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 9), sharex=True)

        ax1.plot(ns, exact, "b-", lw=2, label="Exact theory")
        ax1.plot(ns, approx, "r--", lw=1.5, alpha=0.7, label="Taylor approx")
        ax1.scatter(
            ns, empirical, s=14, color="orange", alpha=0.75, zorder=3,
            label=f"Monte Carlo ({n_trials:,} trials)",
        )
        ax1.set_ylabel("P(match)", fontsize=12)
        ax1.set_title("Simulation vs Theory", fontsize=14)
        ax1.legend(loc="lower right")
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 1.02)

        residual = empirical - exact
        ax2.bar(ns, residual, color="purple", alpha=0.65, width=0.8)
        ax2.axhline(0, color="black", lw=0.8)
        ax2.set_xlabel("Number of people (n)", fontsize=12)
        ax2.set_ylabel("Empirical − Exact", fontsize=12)
        ax2.set_title("Residuals (sampling noise)", fontsize=12)
        ax2.grid(True, alpha=0.3)

        fig.tight_layout()
        path: Path | None = None
        if save:
            path = self._output_dir / "simulation_vs_theory.png"
            fig.savefig(path, dpi=self._dpi, bbox_inches="tight")
            logger.info(f"Saved {path}")
        if show:
            plt.show()
        plt.close(fig)
        return path

    def plot_expected_collisions(self, save: bool = True, show: bool = False) -> Path | None:
        """E[# matching pairs] vs n."""
        self._apply_style()
        days = self._config.days_per_year
        ns = np.arange(1, self._config.max_people + 1)
        expected = np.array([self._prob.expected_collisions(int(n)) for n in ns])
        unique = np.array([self._prob.expected_unique_birthdays(int(n)) for n in ns])

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

        ax1.plot(ns, expected, "b-", lw=2)
        ax1.axhline(1.0, color="red", ls="--", alpha=0.6, label="E = 1 pair")
        n_one = int(np.ceil((1 + np.sqrt(1 + 8 * days)) / 2))
        ax1.axvline(n_one, color="red", ls=":", alpha=0.5, label=f"n = {n_one}")
        ax1.set_xlabel("People in room (n)")
        ax1.set_ylabel("E[matching pairs]")
        ax1.set_title("Expected number of matching pairs:  $\\binom{n}{2}/D$")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2.plot(ns, unique, "g-", lw=2, label="E[distinct birthdays]")
        ax2.plot(ns, ns, "k--", lw=1, alpha=0.5, label="if all distinct")
        ax2.set_xlabel("People in room (n)")
        ax2.set_ylabel("Expected count")
        ax2.set_title("Distinct birthdays: $D \\cdot (1 - (1 - 1/D)^n)$")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        fig.tight_layout()
        path: Path | None = None
        if save:
            path = self._output_dir / "expected_collisions.png"
            fig.savefig(path, dpi=self._dpi, bbox_inches="tight")
            logger.info(f"Saved {path}")
        if show:
            plt.show()
        plt.close(fig)
        return path

    def plot_first_collision_distribution(
        self, n_trials: int = 50000, save: bool = True, show: bool = False,
    ) -> Path | None:
        """Histogram of the group-size index where the first collision appears."""
        self._apply_style()
        max_n = min(self._config.max_people, self._config.days_per_year)
        first_idx = self._sim.simulate_first_collision_distribution(max_n, n_trials)
        valid = first_idx[first_idx > 0]

        fig, ax = plt.subplots(figsize=(11, 6))
        bins = np.arange(2, max_n + 2).tolist()
        ax.hist(
            valid, bins=bins, density=True, alpha=0.75, color="steelblue",
            edgecolor="white", label=f"MC ({n_trials:,} trials)",
        )
        # Analytical PMF: P(first collision at n) = P(no match n-1) - P(no match n)
        ns = np.arange(2, max_n + 1)
        pmf = np.array([
            self._prob.prob_no_match_exact(int(n - 1))
            - self._prob.prob_no_match_exact(int(n))
            for n in ns
        ])
        ax.plot(ns, pmf, "r-", lw=2, label="Analytical PMF")
        ax.set_xlabel("Index of person causing the first collision")
        ax.set_ylabel("Probability")
        ax.set_title(
            f"Where does the first collision happen?  (D = {self._config.days_per_year})",
            fontsize=13,
        )
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        path: Path | None = None
        if save:
            path = self._output_dir / "first_collision_distribution.png"
            fig.savefig(path, dpi=self._dpi, bbox_inches="tight")
            logger.info(f"Saved {path}")
        if show:
            plt.show()
        plt.close(fig)
        return path

    def _compute_k_curves(
        self, n_trials: int,
    ) -> tuple[NDArray[np.int_], list[NDArray[np.float64]], list[int], list[str]]:
        """Pre-compute k-collision probability curves for k = 2..5."""
        max_n = self._config.max_people
        ns = np.arange(1, max_n + 1)
        ks = [2, 3, 4, 5]
        colors = ["#0072B2", "#D55E00", "#009E73", "#CC79A7"]
        curves: list[NDArray[np.float64]] = []
        for k in ks:
            if k == 2:
                curves.append(
                    np.array([self._prob.prob_match_exact(int(n)) for n in ns])
                )
            else:
                curves.append(
                    np.array([
                        self._prob.prob_at_least_k_share(int(n), k, samples=n_trials)
                        for n in ns
                    ])
                )
        return ns, curves, ks, colors

    def plot_k_collision_curves(
        self, n_trials: int = 50000, save: bool = True, show: bool = False,
    ) -> Path | None:
        """P(≥ k share a birthday) vs n for k = 2..5."""
        self._apply_style()
        ns, curves, ks, colors = self._compute_k_curves(n_trials)

        fig, ax = plt.subplots(figsize=(11, 6.5))
        for k, curve, color in zip(ks, curves, colors, strict=True):
            label = f"k = {k} (exact)" if k == 2 else f"k = {k} (MC {n_trials:,})"
            ax.plot(ns, curve, lw=2, color=color, label=label)

        ax.set_xlabel("Number of people in the room (n)", fontsize=12)
        ax.set_ylabel("P(at least k share a birthday)", fontsize=12)
        ax.set_title(
            f"k-Collision Curves  (D = {self._config.days_per_year})", fontsize=14,
        )
        ax.set_xlim(1, ns.max())
        ax.set_ylim(0, 1.02)
        ax.legend(loc="lower right", fontsize=10)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        path: Path | None = None
        if save:
            path = self._output_dir / "k_collision_curves.png"
            fig.savefig(path, dpi=self._dpi, bbox_inches="tight")
            logger.info(f"Saved {path}")
        if show:
            plt.show()
        plt.close(fig)
        return path

    def plot_approximation_error(
        self, save: bool = True, show: bool = False,
    ) -> Path | None:
        """Absolute error |exact − Taylor approx| vs n."""
        self._apply_style()
        ns, exact, approx = self._prob.probability_curve()
        error = np.abs(exact - approx)
        max_error = float(error.max())
        max_idx = int(error.argmax())

        fig, ax = plt.subplots(figsize=(11, 6.5))
        ax.plot(ns, error, lw=2, color="#D55E00", label="|exact − approx|")
        ax.axhline(0.012, color="green", ls="--", alpha=0.7, label="0.012 threshold")
        ax.scatter(
            [ns[max_idx]], [max_error], color="red", s=60, zorder=3,
            label=f"max = {max_error:.5f} at n = {ns[max_idx]}",
        )
        ax.set_xlabel("Number of people in the room (n)", fontsize=12)
        ax.set_ylabel("Absolute error", fontsize=12)
        ax.set_title(
            f"Approximation Error  (D = {self._config.days_per_year})", fontsize=14,
        )
        ax.set_xlim(1, ns.max())
        ax.set_ylim(0, max(max_error * 1.1, 0.015))
        ax.legend(loc="upper right", fontsize=10)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        path: Path | None = None
        if save:
            path = self._output_dir / "approximation_error.png"
            fig.savefig(path, dpi=self._dpi, bbox_inches="tight")
            logger.info(f"Saved {path}")
        if show:
            plt.show()
        plt.close(fig)
        return path

    # ------------------------------------------------------------------
    # Animations
    # ------------------------------------------------------------------

    def animate_probability_buildup(
        self, fps: int = 8, save: bool = True,
    ) -> Path | None:
        """GIF: probability curve drawing itself frame-by-frame."""
        self._apply_style()
        ns, exact, approx = self._prob.probability_curve()
        median_n = self._prob.median_group_size()

        fig, ax = plt.subplots(figsize=(11, 6.5))
        ax.set_xlim(1, ns.max())
        ax.set_ylim(0, 1.02)
        ax.set_xlabel("Number of people in the room (n)", fontsize=12)
        ax.set_ylabel("P(at least one shared birthday)", fontsize=12)
        ax.set_title(
            f"Birthday Paradox — building up (D = {self._config.days_per_year})",
            fontsize=14,
        )
        ax.axhline(0.5, color="green", ls=":", alpha=0.7)
        ax.axhline(0.99, color="purple", ls=":", alpha=0.5)
        ax.grid(True, alpha=0.3)

        (line_exact,) = ax.plot([], [], "b-", lw=2.2, label="Exact")
        (line_approx,) = ax.plot([], [], "r--", lw=1.6, alpha=0.8, label="Approx")
        (pt,) = ax.plot([], [], "o", color="orange", ms=9)
        txt = ax.text(
            0.02, 0.96, "", transform=ax.transAxes, fontsize=12, va="top",
            bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "gray"},
        )
        ax.legend(loc="lower right")

        def init() -> tuple[Any, ...]:
            line_exact.set_data([], [])
            line_approx.set_data([], [])
            pt.set_data([], [])
            txt.set_text("")
            return line_exact, line_approx, pt, txt

        def update(frame: int) -> tuple[Any, ...]:
            i = frame + 1
            line_exact.set_data(ns[:i], exact[:i])
            line_approx.set_data(ns[:i], approx[:i])
            pt.set_data([ns[i - 1]], [exact[i - 1]])
            highlight = " — 50% reached!" if ns[i - 1] == median_n else ""
            txt.set_text(
                f"n = {ns[i - 1]}\nP(match) = {exact[i - 1]:.4f}{highlight}"
            )
            return line_exact, line_approx, pt, txt

        anim = animation.FuncAnimation(
            fig, update, init_func=init, frames=len(ns), interval=1000 // fps, blit=True,
        )

        path: Path | None = None
        if save:
            path = self._save_animation(
                anim, self._output_dir / "probability_buildup.gif", fps,
            )
        plt.close(fig)
        return path

    def animate_room_filling(
        self, group_size: int = 30, fps: int = 4, save: bool = True, seed: int | None = 7,
    ) -> Path | None:
        """
        GIF: people enter a room one at a time, each gets a random birthday;
        the first collision is highlighted with a flash.
        """
        self._apply_style()
        days = self._config.days_per_year
        rng = np.random.default_rng(seed)
        birthdays = rng.integers(0, days, size=group_size).tolist()

        # Find first collision index
        seen: dict[int, int] = {}
        first_collision = 0
        partner = -1
        for i, b in enumerate(birthdays, start=1):
            if b in seen:
                first_collision = i
                partner = seen[b]
                break
            seen[b] = i

        # Layout: people on a ring
        angles = np.linspace(0, 2 * np.pi, group_size, endpoint=False)
        radius = 4.0
        xs = radius * np.cos(angles)
        ys = radius * np.sin(angles)

        fig, (ax_room, ax_curve) = plt.subplots(1, 2, figsize=(14, 7))
        ax_room.set_xlim(-5.5, 5.5)
        ax_room.set_ylim(-5.5, 5.5)
        ax_room.set_aspect("equal")
        ax_room.set_title(f"Room filling up (n = {group_size}, D = {days})", fontsize=13)
        ax_room.axis("off")

        ns_curve, exact_curve, _ = self._prob.probability_curve(max_n=group_size)
        ax_curve.plot(ns_curve, exact_curve, "b-", lw=2)
        ax_curve.set_xlim(1, group_size)
        ax_curve.set_ylim(0, 1.02)
        ax_curve.set_xlabel("People in room (n)")
        ax_curve.set_ylabel("P(match)")
        ax_curve.set_title("Probability so far", fontsize=12)
        ax_curve.grid(True, alpha=0.3)
        ax_curve.axhline(0.5, color="green", ls=":", alpha=0.7)
        (marker,) = ax_curve.plot([], [], "o", color="orange", ms=10)

        circles: list[Circle] = []
        labels: list[Any] = []
        info = ax_room.text(
            0, 5.0, "", ha="center", fontsize=13,
            bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "gray"},
        )

        # Persistent state across frames (mutable to dodge `nonlocal` in closure)
        state: dict[str, int] = {"flash": 0}

        def init() -> tuple[Any, ...]:
            for c in circles:
                c.remove()
            circles.clear()
            for lab in labels:
                lab.remove()
            labels.clear()
            info.set_text("")
            marker.set_data([], [])
            state["flash"] = 0
            return (info, marker)

        total_frames = group_size + 6  # extra frames for the flash

        def update(frame: int) -> tuple[Any, ...]:
            if frame < group_size:
                i = frame + 1
                b = birthdays[i - 1]
                is_collision = (i == first_collision)
                color = "red" if is_collision else "C0"
                circ = Circle((xs[i - 1], ys[i - 1]), 0.45, color=color, alpha=0.85)
                ax_room.add_patch(circ)
                circles.append(circ)
                lab = ax_room.text(
                    xs[i - 1] * 1.18, ys[i - 1] * 1.18, f"{b}",
                    ha="center", va="center", fontsize=9,
                )
                labels.append(lab)
                marker.set_data([i], [exact_curve[i - 1]])
                p = exact_curve[i - 1]
                txt = f"Person {i}: birthday = day {b}\nP(match so far) = {p:.4f}"
                if is_collision and partner > 0:
                    txt += f"\n💥 Match with person {partner}!"
                info.set_text(txt)
            else:
                # Final flash frames
                if first_collision > 0:
                    state["flash"] += 1
                    if state["flash"] % 2 == 1:
                        for idx in (first_collision - 1, partner - 1):
                            if 0 <= idx < len(circles):
                                circles[idx].set_color("yellow")
                    else:
                        for idx in (first_collision - 1, partner - 1):
                            if 0 <= idx < len(circles):
                                circles[idx].set_color("red")
            return (info, marker, *circles)

        anim = animation.FuncAnimation(
            fig, update, init_func=init, frames=total_frames,
            interval=1000 // fps, blit=False, repeat=False,
        )

        path: Path | None = None
        if save:
            path = self._save_animation(
                anim, self._output_dir / "room_filling.gif", fps,
            )
        plt.close(fig)
        return path

    def animate_simulation_convergence(
        self, group_size: int = 23, max_trials: int = 5000,
        snapshots: int = 60, fps: int = 8, save: bool = True,
    ) -> Path | None:
        """
        GIF: running empirical estimate of P(match) for fixed n approaching theory.
        """
        self._apply_style()
        days = self._config.days_per_year
        rng = np.random.default_rng(123)
        draws = rng.integers(0, days, size=(max_trials, group_size))
        srt = np.sort(draws, axis=1)
        has_dup = (np.diff(srt, axis=1) == 0).any(axis=1).astype(np.float64)
        running = np.cumsum(has_dup) / np.arange(1, max_trials + 1)
        theory = self._prob.prob_match_exact(group_size)

        idxs = np.unique(np.linspace(1, max_trials, snapshots).astype(int))

        fig, ax = plt.subplots(figsize=(11, 6.5))
        ax.set_xlim(1, max_trials)
        ax.set_ylim(0, 1.0)
        ax.set_xlabel("Trials")
        ax.set_ylabel("Running estimate of P(match)")
        ax.set_title(
            f"Monte Carlo convergence  (n = {group_size}, D = {days})", fontsize=13,
        )
        ax.axhline(theory, color="red", ls="--", lw=2, label=f"Exact = {theory:.4f}")
        ax.grid(True, alpha=0.3)
        (line,) = ax.plot([], [], "b-", lw=1.5, label="Running estimate")
        ax.legend(loc="lower right")
        txt = ax.text(
            0.02, 0.96, "", transform=ax.transAxes, fontsize=11, va="top",
            bbox={"facecolor": "white", "alpha": 0.85},
        )

        def init() -> tuple[Any, ...]:
            line.set_data([], [])
            txt.set_text("")
            return line, txt

        def update(frame: int) -> tuple[Any, ...]:
            k = idxs[frame]
            line.set_data(np.arange(1, k + 1), running[:k])
            txt.set_text(
                f"Trial {k:,}\nEstimate = {running[k - 1]:.4f}\nError = "
                f"{running[k - 1] - theory:+.4f}"
            )
            return line, txt

        anim = animation.FuncAnimation(
            fig, update, init_func=init, frames=len(idxs),
            interval=1000 // fps, blit=True, repeat=False,
        )

        path: Path | None = None
        if save:
            path = self._save_animation(
                anim, self._output_dir / "convergence.gif", fps,
            )
        plt.close(fig)
        return path

    def animate_k_collision(
        self, n_trials: int = 5000, fps: int = 8, save: bool = True,
    ) -> Path | None:
        """GIF: k-collision curves drawing themselves frame-by-frame."""
        self._apply_style()
        ns, curves, ks, colors = self._compute_k_curves(n_trials)

        fig, ax = plt.subplots(figsize=(11, 6.5))
        ax.set_xlim(1, ns.max())
        ax.set_ylim(0, 1.02)
        ax.set_xlabel("Number of people in the room (n)", fontsize=12)
        ax.set_ylabel("P(at least k share a birthday)", fontsize=12)
        ax.set_title(
            f"k-Collision Curves — building up (D = {self._config.days_per_year})",
            fontsize=14,
        )
        ax.grid(True, alpha=0.3)
        lines = [
            ax.plot([], [], lw=2, color=c, label=f"k = {k}")[0]
            for k, c in zip(ks, colors, strict=True)
        ]
        ax.legend(loc="lower right", fontsize=10)
        txt = ax.text(
            0.02, 0.96, "", transform=ax.transAxes, fontsize=11, va="top",
            bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "gray"},
        )

        def init() -> tuple[Any, ...]:
            for line in lines:
                line.set_data([], [])
            txt.set_text("")
            return (*lines, txt)

        def update(frame: int) -> tuple[Any, ...]:
            i = frame + 1
            for line, curve in zip(lines, curves, strict=True):
                line.set_data(ns[:i], curve[:i])
            txt.set_text(
                f"n = {ns[i - 1]}\n"
                + "\n".join(
                    f"k={k}: {curve[i - 1]:.4f}"
                    for k, curve in zip(ks, curves, strict=True)
                )
            )
            return (*lines, txt)

        anim = animation.FuncAnimation(
            fig, update, init_func=init, frames=len(ns),
            interval=1000 // fps, blit=True,
        )
        path: Path | None = None
        if save:
            path = self._save_animation(
                anim, self._output_dir / "k_collision_animation.gif", fps,
            )
        plt.close(fig)
        return path

    # ------------------------------------------------------------------
    # Batch
    # ------------------------------------------------------------------

    def create_all(self, n_trials: int = 5000) -> list[Path]:
        """Generate every static plot and animation."""
        produced: list[Path] = []
        for p in (
            self.plot_probability_curve(),
            self.plot_simulation_vs_theory(n_trials=n_trials),
            self.plot_expected_collisions(),
            self.plot_first_collision_distribution(n_trials=max(n_trials, 20000)),
            self.plot_k_collision_curves(n_trials=max(n_trials, 50000)),
            self.plot_approximation_error(),
            self.animate_probability_buildup(),
            self.animate_room_filling(),
            self.animate_simulation_convergence(max_trials=n_trials),
            self.animate_k_collision(n_trials=n_trials),
        ):
            if p is not None:
                produced.append(p)
        return produced
