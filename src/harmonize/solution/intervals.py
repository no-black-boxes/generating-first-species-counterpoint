from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Intervals(Sequence):
    """Represents sequential intervals in half steps.

    For example, [4, 3] off of C would be C, E, G. This is used to represent
    scales and chords' tonality/quality.
    """

    intervals: tuple[int]

    def __getitem__(self, index: int | slice) -> int | tuple[int]:
        return self.intervals[index]

    def __len__(self) -> int:
        return len(self.intervals)
