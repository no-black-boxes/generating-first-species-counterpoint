import pytest

from harmonize import io
from harmonize import solution as sol


def test_reads_major_key() -> None:
    solution = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "notes": [[], [], [], []],
        "chords": [],
    }
    expected = sol.Solution(
        key=sol.Key(sol.PitchCls(0), sol.Intervals([2, 2, 1, 2, 2, 2])),
        voices={
            sol.Voice.SOPRANO: [],
            sol.Voice.ALTO: [],
            sol.Voice.TENOR: [],
            sol.Voice.BASS: [],
        },
        chords=[],
    )

    parsed = io.load_solution(solution)

    assert expected == parsed


def test_reads_minor_key() -> None:
    solution = {
        "key": {
            "tonic": "F#/Gb",
            "type": "minor",
        },
        "notes": [[], [], [], []],
        "chords": [],
    }
    expected = sol.Solution(
        key=sol.Key(sol.PitchCls(6), sol.Intervals([2, 1, 2, 2, 1, 2])),
        voices={
            sol.Voice.SOPRANO: [],
            sol.Voice.ALTO: [],
            sol.Voice.TENOR: [],
            sol.Voice.BASS: [],
        },
        chords=[],
    )

    parsed = io.load_solution(solution)

    assert expected == parsed


def test_errors_on_invalid_pitch_class_in_key() -> None:
    solution = {
        "key": {
            # Yes, it's enharmonically the same as C, but it's not supported.
            "tonic": "B#",
            "type": "minor",
        },
        "notes": [[], [], [], []],
        "chords": [],
    }

    with pytest.raises(ValueError):
        io.load_solution(solution)


def test_errors_on_invalid_key_type() -> None:
    solution = {
        "key": {
            "tonic": "C",
            "type": "Major",
        },
        "notes": [[], [], [], []],
        "chords": [],
    }

    with pytest.raises(ValueError):
        io.load_solution(solution)
