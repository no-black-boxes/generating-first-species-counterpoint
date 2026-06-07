from dataclasses import dataclass
from enum import Enum

from harmonize.solution.key import Key
from harmonize.solution.note import Note
from harmonize.solution.chord import Chord


class Voice(Enum):
    SOPRANO = 0
    ALTO = 1
    TENOR = 2
    BASS = 3


@dataclass
class Solution:
    """Represents a complete or incomplete realization of four-part harmony."""

    key: Key
    voices: dict[Voice, list[Note]]
    chords: list[Chord]
