"""Immutable configuration for the Birthday Paradox model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BirthdayConfig:
    """
    Immutable configuration for the Birthday Paradox.

    Attributes:
        days_per_year: Size of the birthday pool (D). 365 by default,
            use 366 for leap-year aware analyses.
        max_people: Maximum group size considered in plots/animations.
    """

    days_per_year: int = 365
    max_people: int = 100

    def __post_init__(self) -> None:
        if self.days_per_year < 2:
            raise ValueError("days_per_year must be >= 2")
        if self.max_people < 2:
            raise ValueError("max_people must be >= 2")
        if self.max_people > self.days_per_year:
            # Above D people, collision is guaranteed (pigeonhole).
            # Allow it but it's not meaningful past D+1.
            pass

    @property
    def pigeonhole_bound(self) -> int:
        """Group size at which collision is guaranteed (D + 1)."""
        return self.days_per_year + 1
