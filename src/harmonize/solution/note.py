from dataclasses import dataclass


@dataclass(frozen=True)
class PitchCls:
    """Represents a pitch class (pitch without an octave)."""

    pitch: int

    def __post_init__(self):
        # Keeping PitchCls immutable but intentially reassigning to keep pitch
        # modulo 12.
        object.__setattr__(self, "pitch", self.pitch % 12)

    def interval_to(self, other: PitchCls) -> int:
        """Returns the interval in half steps between the two pitch classes,
        treating the other as the higher pitch.
        """
        return (other.pitch - self.pitch) % 12


@dataclass(frozen=True)
class Note:
    """Represents a pitch with an octave."""

    pitch: int
