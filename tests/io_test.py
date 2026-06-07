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


@pytest.mark.parametrize(
    "chord_str, root, intervals, inversion",
    [
        ("I", sol.PitchCls(0), sol.Intervals([4, 3]), 0),
        ("V", sol.PitchCls(7), sol.Intervals([4, 3]), 0),
        ("vi", sol.PitchCls(9), sol.Intervals([3, 4]), 0),
        ("vii_dim", sol.PitchCls(11), sol.Intervals([3, 3]), 0),
        ("IV6", sol.PitchCls(5), sol.Intervals([4, 3]), 1),
        ("vii_dim64", sol.PitchCls(11), sol.Intervals([3, 3]), 2),
        ("V7", sol.PitchCls(7), sol.Intervals([4, 3, 3]), 0),
        ("V65", sol.PitchCls(7), sol.Intervals([4, 3, 3]), 1),
        ("V43", sol.PitchCls(7), sol.Intervals([4, 3, 3]), 2),
        ("V42", sol.PitchCls(7), sol.Intervals([4, 3, 3]), 3),
        ("IVM7", sol.PitchCls(5), sol.Intervals([4, 3, 4]), 0),
        ("vi7", sol.PitchCls(9), sol.Intervals([3, 4, 3]), 0),
        ("vii_hdim7", sol.PitchCls(11), sol.Intervals([3, 3, 4]), 0),
        ("vii_dim7", sol.PitchCls(11), sol.Intervals([3, 3, 3]), 0),
        ("vii_dim65", sol.PitchCls(11), sol.Intervals([3, 3, 3]), 1),
    ],
)
def test_reads_single_chord(
    dict_solution, solution, chord_str, root, intervals, inversion
) -> None:
    dict_solution["chords"] = [chord_str]

    solution.chords = [sol.Chord(root, intervals, inversion)]

    parsed = io.load_solution(dict_solution)

    assert solution == parsed


@pytest.mark.parametrize(
    "chord_str",
    [
        "viiii",
        "Vi",
        "I5",
        "vii_hdim",
        "VM",
    ],
)
def test_errors_on_invalid_single_chord(dict_solution, chord_str) -> None:
    dict_solution["chords"] = [chord_str]

    with pytest.raises(ValueError):
        io.load_solution(dict_solution)


def test_reads_single_chord_in_different_key(dict_solution, solution) -> None:
    dict_solution["key"] = {
        "tonic": "D",
        "type": "minor",
    }

    dict_solution["chords"] = ["V"]

    solution.key = sol.Key(sol.PitchCls(2), sol.Intervals([2, 1, 2, 2, 1, 2]))
    solution.chords = [sol.Chord(sol.PitchCls(9), sol.Intervals([4, 3]), 0)]

    parsed = io.load_solution(dict_solution)

    assert solution == parsed


def test_errors_when_missing_key() -> None:
    dict_solution = {
        "notes": [[], [], [], []],
        "chords": [],
    }

    with pytest.raises(ValueError):
        io.load_solution(dict_solution)


def test_errors_when_missing_notes() -> None:
    dict_solution = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "chords": [],
    }

    with pytest.raises(ValueError):
        io.load_solution(dict_solution)


def test_errors_when_missing_chords() -> None:
    dict_solution = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "notes": [[], [], [], []],
    }

    with pytest.raises(ValueError):
        io.load_solution(dict_solution)


def test_errors_when_malformed_key() -> None:
    dict_solution = {
        "key": {
            "root": "C",
            "type": "major",
        },
        "notes": [[], [], [], []],
        "chords": [],
    }

    with pytest.raises(ValueError):
        io.load_solution(dict_solution)


def test_errors_when_wrong_voice_count() -> None:
    dict_solution = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "notes": [[], [], []],
        "chords": [],
    }

    with pytest.raises(ValueError):
        io.load_solution(dict_solution)
