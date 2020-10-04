#! /bin/env python

"""Command-line tool for viewing hunting horn melodies.

Usage:
    horn list [--notes=<notes>] [(--horn=<horn>|--select-horn)]
    horn -h | --help
    horn --version

Options:
    --help -h        Show this screen.
    --version        Show version.
    --notes=<notes>  Notes to filter by [default: ABGMRWY]
"""

from typing import Optional, Set

from docopt import docopt

from pkg_resources import get_distribution

from huntinghorn.constants import NOTES, Note, horns, melodies
from huntinghorn.prompt import prompt_for_horn
from huntinghorn.utils import Horn

__version__ = get_distribution("huntinghorn").version


def main() -> None:
    """Entry point for the command line interface."""
    arguments = docopt(__doc__, version=f"horn {__version__}")

    notes: Set[Note] = set()
    horn: Optional[Horn] = None

    for name in arguments["--notes"]:
        if note := NOTES.get(name):
            notes.add(note)

    horn = horns.get(arguments["--horn"])
    if arguments["--select-horn"]:
        horn = prompt_for_horn() or horn

    available_melodies = horn.melodies if horn else [
        melody for melody in melodies if notes >= set(melody.actions)
    ]

    padding = max(len(str(melody)) for melody in available_melodies)

    for melody in available_melodies:
        print(melody.as_str(padding + 1))
