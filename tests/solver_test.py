import pytest

from harmonize import solution as sol
from harmonize.solver import Solver


@pytest.fixture
def input_solution() -> dict:
    return sol.Solution(
        [60, 62, 64, 65, 67, 60],
        [
            48,
            sol.UNKNOWN_NOTE,
            sol.UNKNOWN_NOTE,
            sol.UNKNOWN_NOTE,
            sol.UNKNOWN_NOTE,
            48,
        ],
        set(),
    )


def test_creates_solution_without_modifying_fixed_notes(input_solution) -> None:
    solver = Solver()

    output_solution = solver.solve(input_solution)

    for in_note, out_note in zip(input_solution.melody, output_solution.melody):
        if in_note == sol.UNKNOWN_NOTE:
            continue

        assert in_note == out_note

    for in_note, out_note in zip(
        input_solution.counter_melody, output_solution.counter_melody
    ):
        if in_note == sol.UNKNOWN_NOTE:
            continue

        assert in_note == out_note


def test_creates_counter_melody_without_unknowns(input_solution) -> None:
    solver = Solver()

    output_solution = solver.solve(input_solution)

    for note in output_solution.counter_melody:
        assert note != sol.UNKNOWN_NOTE
