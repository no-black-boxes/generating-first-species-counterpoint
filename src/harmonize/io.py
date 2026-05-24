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

    try:
        pitch_cls = sol.PitchCls(_PITCH_CLASS_NAMES.index(key_data["tonic"]))
    except ValueError:
        raise ValueError(f"Pitch class {key_data['tonic']} not supported")

    return sol.Key(
        pitch_cls,
        intervals,
    )


def _parse_voices(voices_data: list[list]) -> dict[sol.Voice, list]:
    return {
        sol.Voice.SOPRANO: [],
        sol.Voice.ALTO: [],
        sol.Voice.TENOR: [],
        sol.Voice.BASS: [],
    }
    # voices = []

    # for index, notes in enumerate(voices_data):
    #    voices[sol.Voice(index)] = _parse_notes(notes)

    # return voices


def _parse_notes(notes_data: list[str]) -> list[sol.Note]:
    return map(_parse_note, notes_data)


def _parse_note(note: str) -> sol.Note:
    return sol.Note(
        sol.PitchCls(note[0]),
        sol.Accidental(note[1:-1]),
        int(note[-1]),
    )


def _parse_chords(chord_data: list[str]) -> list[sol.Chord]:
    return []
