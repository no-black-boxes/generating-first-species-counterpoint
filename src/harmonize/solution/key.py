from dataclasses import dataclass

from harmonize.solution.note import PitchCls
from harmonize.solution.intervals import Intervals


@dataclass(frozen=True)
class Key:
    """Represents a key's tonic pitch and tonality/mode."""

    pitch_cls: PitchCls
    intervals: Intervals
