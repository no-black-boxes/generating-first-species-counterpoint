from dataclasses import dataclass

from harmonize.solution.note import PitchCls
from harmonize.solution.intervals import Intervals


@dataclass(frozen=True)
class Chord:
    """Represents a chord's root, quality, and inversion.

    Intervals are specified off of the chord root, not the bass note.
    """

    root: PitchCls
    intervals: Intervals
    inversion: int
