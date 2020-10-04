from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import Dict, List, Union

from colorama import Back, Fore, Style

import huntinghorn


class Button:
    UP = "▲"
    LEFT = "◀"
    DOWN = "▼"
    RIGHT = "⬤"


class Note(Enum):
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    MAGENTA = "MAGENTA"
    AQUA = "LIGHTBLUE_EX"
    WHITE = "LIGHTWHITE_EX"

    @cached_property
    def fore_colour(self) -> str:
        return getattr(Fore, self.value)

    @cached_property
    def back_colour(self) -> str:
        return getattr(Back, self.value)

    def __str__(self):
        return f"{Style.RESET_ALL}{self.fore_colour}♪{Style.RESET_ALL}"


@dataclass
class Move:
    buttons: List[str]
    note: Note

    def __str__(self) -> str:
        return (
            f"{Back.RESET}{self.note.fore_colour}"
            f"{'+'.join(self.buttons)} {Style.RESET_ALL}"
        ).center(18, " ")


@dataclass
class Melody:
    name: str
    actions: Union[List[Note], List[Move]]

    rest_string: str = f"{Fore.WHITE}𝄽{Fore.RESET}"

    def __post_init__(self) -> None:
        # Don't include rests for normal notes
        if type(self.actions[0]) is Note:
            self.rest_string = ""

    def __str__(self) -> str:
        return self.name

    def as_str(self, padding: int) -> str:
        return (
            f"{Fore.WHITE}{self.name.ljust(padding)}{Style.RESET_ALL}" + (
                f"{self.rest_string} ".join(map(str, self.actions))
            )
        )


@dataclass
class Horn:
    """Represent an instrument that can play melodies."""

    name: str
    moves: List[Move]

    @cached_property
    def notes(self) -> Dict[Note, Move]:
        return {move.note: move for move in self.moves}

    @cached_property
    def melodies(self) -> List[Melody]:
        return [
            Melody(
                name=melody.name,
                actions=[self.notes[note] for note in melody.actions]
            )
            for melody in huntinghorn.constants.melodies
            if self.notes.keys() >= set(melody.actions)
        ]
