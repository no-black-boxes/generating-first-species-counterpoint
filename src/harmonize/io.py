from enum import Enum, auto
import re

from harmonize import solution as sol


class Quality(Enum):
    MAJOR = auto()
    MINOR = auto()
    DIMINISHED = auto()


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


# We only need these seven, so I haven't written a roman numeral parser.
_ROMAN_NUMERALS = ["i", "ii", "iii", "iv", "v", "vi", "vii"]


_INVERSION_SYMBOLS = {
    "": (False, 0),
    "6": (False, 1),
    "64": (False, 2),
    "7": (True, 0),
    "65": (True, 1),
    "43": (True, 2),
    "42": (True, 3),
}


def load_solution(data: dict) -> sol.Solution:
    """Loads a solution from JSON data."""

    if "key" not in data or "notes" not in data or "chords" not in data:
        raise ValueError("Solution must have 'key', 'notes', and 'chords' keys")

    key = _parse_key(data["key"])
    voices = _parse_voices(data["notes"])
    chords = list(map(lambda chord: _parse_chord(key, chord), data["chords"]))

    return sol.Solution(key, voices, chords)


def _parse_key(key_data: dict) -> sol.Key:
    if "tonic" not in key_data or "type" not in key_data:
        raise ValueError("Key must have 'tonic' and 'type' keys")

    match key_data["type"]:
        case "major":
            intervals = sol.Intervals([2, 2, 1, 2, 2, 2])
        case "minor":
            intervals = sol.Intervals([2, 1, 2, 2, 1, 2])
        case _:
            raise ValueError(f"'{key_data['type']}' is not a supported key")

    pitch_cls = sol.PitchCls(_pitch_class_int_from_str(key_data["tonic"]))

    return sol.Key(
        pitch_cls,
        intervals,
    )


def _pitch_class_int_from_str(str_cls: str) -> int:
    try:
        return _PITCH_CLASS_NAMES.index(str_cls)
    except ValueError:
        raise ValueError(f"Pitch class {str_cls} not supported")


def _parse_voices(voices_data: list[list]) -> dict[sol.Voice, list]:
    voices = {}

    if not len(voices_data) == 4:
        raise ValueError("Solution must have four voices")

    for index, notes in enumerate(voices_data):
        voices[sol.Voice(index)] = list(map(_parse_note, notes))

    return voices


def _parse_note(note: str) -> sol.Note:
    re_match = re.match(r"^[A-Z]#/[A-Z]b|^[A-Z]", note)

    if re_match is None:
        raise ValueError(f"{note} is not a valid note")

    pitch_cls_int = _pitch_class_int_from_str(re_match[0])
    octave = int(note[len(re_match[0]) :])

    # 12 is C0.
    return sol.Note(pitch_cls_int + octave * 12 + 12)


def _parse_chord(key: sol.Key, chord: str) -> sol.Chord:
    re_match = re.match(r"([IViv]+)(M|_dim|_hdim|)(\d*)", chord)

    numeral = re_match[1]
    quality_modifier = re_match[2]
    inversion_symbol = re_match[3]

    # Note this starts with "i" as 0.
    try:
        numeral_value = _ROMAN_NUMERALS.index(numeral.lower())
    except ValueError:
        raise ValueError(f"{numeral} is not a valid numeral")

    root = key.get_scale_degree(numeral_value)

    try:
        is_seventh, inversion = _INVERSION_SYMBOLS[inversion_symbol]
    except KeyError:
        raise ValueError(f"{inversion_symbol} is not a valid inversion")

    intervals = _parse_chord_intervals(numeral, quality_modifier, is_seventh)

    return sol.Chord(root, intervals, inversion)


def _parse_chord_intervals(
    numeral: str, quality_modifier: str, is_seventh: bool
) -> sol.Intervals:
    if "dim" in quality_modifier:
        intervals = [3, 3]
    elif numeral == numeral.lower():
        intervals = [3, 4]
    elif numeral == numeral.upper():
        intervals = [4, 3]
    else:
        raise ValueError(
            f"{numeral}{quality_modifier} represents in invalid chord quality"
        )

    if not is_seventh:
        if quality_modifier == "_hdim" or quality_modifier == "M":
            raise ValueError(
                f"{quality_modifier} suggests a seventh, but no inversion is provided"
            )

        return sol.Intervals(intervals)

    if quality_modifier == "_dim":
        # Diminished seventh
        intervals.append(9 - sum(intervals))
    elif quality_modifier == "_hdim" or len(quality_modifier) == 0:
        # Minor seventh
        intervals.append(10 - sum(intervals))
    elif quality_modifier == "M":
        # Major seventh
        intervals.append(11 - sum(intervals))

    return sol.Intervals(intervals)
