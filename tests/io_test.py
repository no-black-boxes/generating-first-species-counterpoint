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
