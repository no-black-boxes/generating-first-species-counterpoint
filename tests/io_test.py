import pytest

from harmonize import io
from harmonize import solution as sol


def test_loads_midi_pitch_from_note_name():
    sol_input = {
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
        "melody": ["C4", "G4", "F4", "C5"],
        "counterMelody": ["C3", "B2", "G3", "C4"],
    }

    expected_melody = [60, 67, 65, 72]
    expected_counter_melody = [48, 47, 55, 60]
    
    solution = io.load_solution(sol_input)

    assert expected_melody == solution.melody
    assert expected_counter_melody == solution.counter_melody


def test_error_on_invalid_pitch():
    sol_input = {
        "melody": ["H5"],
        "counterMelody": ["C3"],
    }
    
    with pytest.raises(ValueError):
        io.load_solution(sol_input)


def test_error_on_length_difference():
    sol_input = {
        "melody": ["C4", "D4"],
        "counterMelody": ["C3"],
    }
    
    with pytest.raises(ValueError):
        io.load_solution(sol_input)


def test_error_on_unknown_in_melody():
    sol_input = {
        "melody": ["X"],
        "counterMelody": ["C3"],
    }
    
    with pytest.raises(ValueError):
        io.load_solution(sol_input)
