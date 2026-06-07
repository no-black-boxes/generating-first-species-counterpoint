from dataclasses import dataclass

from harmonize.solution.note import PitchCls
from harmonize.solution.intervals import Intervals


@dataclass(frozen=True)
class Key:
    """Represents a key's tonic pitch and tonality/mode."""

    pitch_cls: PitchCls
    intervals: Intervals

    def get_scale_degree(self, scale_degree: int) -> PitchCls:
        """Gets the pitch class of a given scale degree.

        Scale degrees start at zero, with zero being the tonic of the scale.
        """

        interval_sum = sum(self.intervals[:scale_degree])

        return PitchCls(self.pitch_cls.pitch + interval_sum)
