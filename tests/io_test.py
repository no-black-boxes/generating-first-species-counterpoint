import pytest

from harmonize import io
from harmonize import solution as sol


@pytest.fixture
def dict_solution() -> dict:
    return {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "notes": [[], [], [], []],
        "chords": [],
    }


@pytest.fixture
def solution() -> sol.Solution:
    return sol.Solution(
        key=sol.Key(sol.PitchCls(0), sol.Intervals([2, 2, 1, 2, 2, 2])),
        voices={
            sol.Voice.SOPRANO: [],
            sol.Voice.ALTO: [],
            sol.Voice.TENOR: [],
            sol.Voice.BASS: [],
        },
        chords=[],
    )


def test_reads_major_key(dict_solution, solution) -> None:
    dict_solution["key"] = {
        "tonic": "C",
        "type": "major",
    }

    solution.key = sol.Key(sol.PitchCls(0), sol.Intervals([2, 2, 1, 2, 2, 2]))

    parsed = io.load_solution(dict_solution)

    assert solution == parsed


def test_reads_minor_key(dict_solution, solution) -> None:
    dict_solution["key"] = {
        "tonic": "F#/Gb",
        "type": "minor",
    }

    solution.key = sol.Key(sol.PitchCls(6), sol.Intervals([2, 1, 2, 2, 1, 2]))

    parsed = io.load_solution(dict_solution)

    assert solution == parsed


def test_errors_on_invalid_pitch_class_in_key(dict_solution) -> None:
    dict_solution["key"] = {
        # Yes, it's enharmonically the same as C, but it's not supported.
        "tonic": "B#",
        "type": "minor",
    }

    with pytest.raises(ValueError):
        io.load_solution(dict_solution)


def test_errors_on_invalid_key_type(dict_solution) -> None:
    dict_solution["key"] = {
        "tonic": "C",
        "type": "Major",
    }

    with pytest.raises(ValueError):
        io.load_solution(dict_solution)


def test_reads_one_note(dict_solution, solution) -> None:
    dict_solution["notes"][sol.Voice.SOPRANO.value] = ["C4"]

    solution.voices[sol.Voice.SOPRANO] = [sol.Note(60)]

    parsed = io.load_solution(dict_solution)

    assert solution == parsed


def test_reads_multiple_notes(dict_solution, solution) -> None:
    dict_solution["key"] = {
        "tonic": "A#/Bb",
        "type": "major",
    }

    dict_solution["notes"][sol.Voice.SOPRANO.value] = ["A#/Bb4", "G4", "F4", "F4"]
    dict_solution["notes"][sol.Voice.ALTO.value] = ["F4", "D#/Eb4", "C4", "D4"]
    dict_solution["notes"][sol.Voice.TENOR.value] = ["D4", "A#/Bb3", "A3", "A#/Bb3"]
    dict_solution["notes"][sol.Voice.BASS.value] = ["A#/Bb2", "D#/Eb3", "F3", "A#/Bb2"]

    solution.key = sol.Key(sol.PitchCls(10), sol.Intervals([2, 2, 1, 2, 2, 2]))

    solution.voices[sol.Voice.SOPRANO] = [
        sol.Note(70),
        sol.Note(67),
        sol.Note(65),
        sol.Note(65),
    ]
    solution.voices[sol.Voice.ALTO] = [
        sol.Note(65),
        sol.Note(63),
        sol.Note(60),
        sol.Note(62),
    ]
    solution.voices[sol.Voice.TENOR] = [
        sol.Note(62),
        sol.Note(58),
        sol.Note(57),
        sol.Note(58),
    ]
    solution.voices[sol.Voice.BASS] = [
        sol.Note(46),
        sol.Note(51),
        sol.Note(53),
        sol.Note(46),
    ]

    parsed = io.load_solution(dict_solution)

    assert solution == parsed


def test_reads_negative_octave(dict_solution, solution) -> None:
    dict_solution["notes"][sol.Voice.SOPRANO.value] = ["C-1"]

    solution.voices[sol.Voice.SOPRANO] = [sol.Note(0)]

    parsed = io.load_solution(dict_solution)

    assert solution == parsed


def test_errors_on_invalid_pitch_class(dict_solution) -> None:
    dict_solution["notes"][sol.Voice.SOPRANO.value] = ["H4"]

    with pytest.raises(ValueError):
        io.load_solution(dict_solution)


def test_errors_on_non_alphabetic_pitch_class(dict_solution) -> None:
    dict_solution["notes"][sol.Voice.SOPRANO.value] = ["@4"]

    with pytest.raises(ValueError):
        io.load_solution(dict_solution)
