from argparse import ArgumentParser
from pathlib import Path


def _parse_args() -> tuple[Path, Path]:
    parser = ArgumentParser(
        prog="harmonize",
        description="Generates four-part harmony using constraints",
    )

    parser.add_argument("input", help="JSON file with initial conditions")
    parser.add_argument("output", help="JSON file for the solution")

    args = parser.parse_args()

    return Path(args.input), Path(args.output)


def main() -> None:
    in_path, out_path = _parse_args()
    print(f"Input path: {in_path}")
    print(f"Output path: {out_path}")
