import pytest

from harmonize import io
from harmonize import solution as sol


def test_loads_midi_pitch_from_note_name():
    sol_input = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "melody": ["C4"],
        "counterMelody": ["G#/Ab5"],
    }

    expected_melody = [60]
    expected_counter_melody = [80]

    solution = io.load_solution(sol_input)

    assert expected_melody == solution.melody
    assert expected_counter_melody == solution.counter_melody


def test_loads_unknown_pitch():
    sol_input = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "melody": ["C4"],
        "counterMelody": ["X"],
    }

    expected_melody = [60]
    expected_counter_melody = [sol.UNKNOWN_NOTE]

    solution = io.load_solution(sol_input)

    assert expected_melody == solution.melody
    assert expected_counter_melody == solution.counter_melody


def test_loads_multiple_pitches():
    sol_input = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "melody": ["C4", "G4", "F4", "C5"],
        "counterMelody": ["C3", "B2", "G3", "C4"],
    }

    expected_melody = [60, 67, 65, 72]
    expected_counter_melody = [48, 47, 55, 60]

    solution = io.load_solution(sol_input)

    assert expected_melody == solution.melody
    assert expected_counter_melody == solution.counter_melody


def test_loads_extreme_pitches():
    sol_input = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "melody": ["G9"],
        "counterMelody": ["C-1"],
    }

    expected_melody = [127]
    expected_counter_melody = [0]

    solution = io.load_solution(sol_input)

    assert expected_melody == solution.melody
    assert expected_counter_melody == solution.counter_melody


def test_error_on_invalid_pitch():
    sol_input = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "melody": ["H5"],
        "counterMelody": ["C3"],
    }

    with pytest.raises(ValueError):
        io.load_solution(sol_input)


def test_error_on_length_difference():
    sol_input = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "melody": ["C4", "D4"],
        "counterMelody": ["C3"],
    }

    with pytest.raises(ValueError):
        io.load_solution(sol_input)


def test_error_on_unknown_in_melody():
    sol_input = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "melody": ["X"],
        "counterMelody": ["C3"],
    }

    with pytest.raises(ValueError):
        io.load_solution(sol_input)


def test_error_on_too_low_pitch():
    sol_input = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "melody": ["B-2"],
        "counterMelody": ["X"],
    }

    with pytest.raises(ValueError):
        io.load_solution(sol_input)


def test_error_on_too_high_pitch():
    sol_input = {
        "key": {
            "tonic": "C",
            "type": "major",
        },
        "melody": ["G#/Ab9"],
        "counterMelody": ["X"],
    }

    with pytest.raises(ValueError):
        io.load_solution(sol_input)


def test_dumps_pitch():
    solution = sol.Solution([60], [80], set())

    expected_melody = ["C4"]
    expected_counter_melody = ["G#/Ab5"]

    result = io.dump_solution(solution)

    assert expected_melody == result["melody"]
    assert expected_counter_melody == result["counterMelody"]


def test_dumps_unknown():
    solution = sol.Solution([60], [sol.UNKNOWN_NOTE], set())

    expected_melody = ["C4"]
    expected_counter_melody = ["X"]

    result = io.dump_solution(solution)

    assert expected_melody == result["melody"]
    assert expected_counter_melody == result["counterMelody"]


def test_dumps_multiple_pitches():
    solution = sol.Solution([60, 67, 65, 72], [48, 47, 55, 60], set())

    expected_melody = ["C4", "G4", "F4", "C5"]
    expected_counter_melody = ["C3", "B2", "G3", "C4"]

    result = io.dump_solution(solution)

    assert expected_melody == result["melody"]
    assert expected_counter_melody == result["counterMelody"]
