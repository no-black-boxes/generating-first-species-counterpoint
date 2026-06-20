from argparse import ArgumentParser
import json
from pathlib import Path
import sys

from harmonize import io
from harmonize.solution import Solution


def _parse_args() -> tuple[Path, Path]:
    parser = ArgumentParser(
        prog="harmonize",
        description="Generates first-species counterpoint",
    )

    parser.add_argument("input", help="JSON file with the melody and constraints")
    parser.add_argument("output", help="JSON output file for the solution")

    args = parser.parse_args()

    return Path(args.input), Path(args.output)


def _read_initial_solution(path: Path) -> Solution:
    try:
        with open(path, "r") as file:
            solution_dict = json.load(file)
    except FileNotFoundError:
        print(f"Unable to find input file {path.absolute()}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Input file {path.absolute()} is invalid JSON", file=sys.stderr)
        sys.exit(1)

    try:
        solution = io.load_solution(solution_dict)
    except ValueError as error:
        print(f"Failed to load input file {path.absolute()}:\n{error}", file=sys.stderr)
        sys.exit(1)

    return solution


def main() -> None:
    in_path, out_path = _parse_args()

    solution = _read_initial_solution(in_path)

    print(f"Output path: {out_path}")
    print(f"Melody: {solution.melody}")
    print(f"Counter-melody: {solution.counter_melody}")
