import re

from harmonize import solution as sol


_PITCH_CLASS_NAMES = [
    "C",
    "C#/Db",
    "D",
    "D#/Eb",
    "E",
    "F",
    "F#/Gb",
    "G",
    "G#/Ab",
    "A",
    "A#/Bb",
    "B",
]

_UNKNOWN_NAME = "X"


def load_solution(data: dict) -> sol.Solution:
    """Loads a solution from JSON data."""

    melody = _parse_voice(data["melody"])
    counter_melody = _parse_voice(data["counterMelody"])

    return sol.Solution(melody, counter_melody)


def _parse_voice(voice: list[str]) -> list[int]:
    notes = []

    for note_str in voice:
        if note_str == _UNKNOWN_NAME:
            notes.append(sol.UNKNOWN_NOTE)
            continue

        note_match = re.match(r"([A-G]#/[A-G]b|[A-G])(\d)", note_str)

        if note_match is None:
            raise ValueError(f"{note_str} is not a valid note")

        pitch_class = _PITCH_CLASS_NAMES.index(note_match[1])
        octave = int(note_match[2])

        notes.append(octave * 12 + pitch_class + 12)

    return notes
