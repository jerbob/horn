"""Constants and Enums for use in the main program."""

import json
from pathlib import Path
from typing import Dict, List

from huntinghorn.utils import Horn, Melody, Move, Note

DATA_ROOT = Path(__file__).parent / "data"


with (DATA_ROOT / "horns.json").open() as file:
    horns: Dict[str, Horn] = {
        name: Horn(name, moves=[Move(move[0], Note(move[1])) for move in horn])
        for name, horn in json.load(file).items()
    }

with (DATA_ROOT / "melodies.json").open() as file:
    melodies: List[Melody] = [
        Melody(name=melody[0], actions=[Note(note) for note in melody[1]])
        for melody in json.load(file)
    ]
