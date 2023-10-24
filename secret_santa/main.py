import logging
import argparse
from typing import Set, List, Tuple
from pathlib import Path

from secret_santa import lib


logger = logging.getLogger(__name__)


def parse_input_names(file: Path) -> Set[str]:
    """Open and read file. Return a curated list of names.

    Duplicates are removed.
    """
    names = set()

    with file.open() as f:
        for line in f:
            # TODO further clear undesired characters here.
            if line := line.strip():
                names.add(line)

    return names


def parse_input_exclusions(file: Path) -> List[Tuple[str, str]]:
    """Open and parse file. Return a list of name pairs."""
    pairs = []

    with file.open() as f:
        for line in f:
            if line := line.strip():
                left, right = line.split(",")

                if (left := left.strip()) and (right := right.strip()):
                    pairs.append((left, right))

    return pairs


if "__main__" == __name__:
    parser = argparse.ArgumentParser(prog="SantaSorter", description="OuiHelp's Secret Santa Sorter!", epilog="\u201CHo Ho Ho!\u201D")
    parser.add_argument("names", type=Path, help="The party participants as a text file.")
    parser.add_argument("exclusions", type=Path, help="The exclusions as a text file.")
    parser.add_argument("sorting", type=argparse.FileType("w", encoding="utf-8"),
                        help="A file where to write the computed result.")

    args = parser.parse_args()

    # TODO add a random factor so consecutive calls produce different results (--random flag?).

    # TODO add a flag to show results at the end (--output flag?).

    names = parse_input_names(args.names)
    print(f"Got {len(names)} name(s) from \"{args.names}\".")
    logging.debug(f"{names=!r}")

    exclusions = parse_input_exclusions(args.exclusions)
    print(f"Got {len(exclusions)} exclusion(s) from \"{args.exclusions}\".")
    logging.debug(f"{exclusions=!r}")

    # TODO ensure names found in exclusions exist in participants.

    print("Prepping datasets…")
    participants = lib.parse_data(names, exclusions)

    print("Securing participants with limited options…")
    participants = lib.secure_one_option_participants(participants)

    print("Working Santa's magic…")
    path = []
    if lib.work_a_distribution(participants, path):
        path.append(path[0])  # Duplicate the first node to "close" the path.

        for i in range(len(path) - 1):
            args.sorting.write(f"{path[i].name:10.10s} makes a gift to {path[i+1].name}.\n")

        print(f"Hurray! Santa sorted things out in \"{args.sorting.name}\".")
    else:
        print("Hu-oh… I failed to find a satisfying solution for you dataset and contraints.")
