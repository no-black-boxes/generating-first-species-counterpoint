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


def load_solution(data: dict) -> sol.Solution:
    """Loads a solution from JSON data."""
    return sol.Solution(
        _parse_key(data["key"]),
        _parse_voices(data["notes"]),
        _parse_chords(data["chords"]),
    )


def _parse_key(key_data: dict) -> sol.Key:
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


def _parse_chords(chord_data: list[str]) -> list[sol.Chord]:
    return []
