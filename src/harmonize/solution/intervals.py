from dataclasses import dataclass


@dataclass(frozen=True)
class Intervals:
    """Represents sequential intervals in half steps.

    For example, [4, 3] off of C would be C, E, G. This is used to represent
    scales and chords' tonality/quality.
    """

    intervals: tuple[int]
