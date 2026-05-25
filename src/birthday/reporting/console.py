"""Console reporting for the Birthday Paradox."""

from __future__ import annotations

from birthday.math.probability import BirthdayProbability


class ConsoleReporter:
    """Pretty-print a checkpoint table for the Birthday Paradox."""

    __slots__ = ("_probability", "_checkpoints")

    _DEFAULT_CHECKPOINTS: list[int] = [5, 10, 23, 30, 50, 70, 100]

    def __init__(
        self,
        probability: BirthdayProbability,
        checkpoints: list[int] | None = None,
    ) -> None:
        self._probability = probability
        self._checkpoints = checkpoints or list(self._DEFAULT_CHECKPOINTS)

    @property
    def checkpoints(self) -> list[int]:
        return list(self._checkpoints)

    def report(self) -> str:
        lines = [self._header(), self._separator()]
        for n in self._checkpoints:
            lines.append(self._row(n))
        return "\n".join(lines) + "\n"

    def _header(self) -> str:
        return (
            f"{'n':>3} "
            f"{'exact':>10} "
            f"{'approx':>10} "
            f"{'E[pairs]':>10} "
            f"{'residual':>10}"
        )

    def _separator(self) -> str:
        return (
            f"{'---':>3} "
            f"{'----------':>10} "
            f"{'----------':>10} "
            f"{'----------':>10} "
            f"{'----------':>10}"
        )

    def _row(self, n: int) -> str:
        exact = self._probability.prob_match_exact(n)
        approx = self._probability.prob_match_approx(n)
        pairs = self._probability.expected_collisions(n)
        residual = exact - approx
        return (
            f"{n:>3} "
            f"{exact:>10.6f} "
            f"{approx:>10.6f} "
            f"{pairs:>10.4f} "
            f"{residual:>+10.6f}"
        )
