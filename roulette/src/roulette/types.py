from dataclasses import dataclass
from enum import Enum


class Color(Enum):
    GREEN = "Green"
    RED = "Red"
    BLACK = "Black"


@dataclass(frozen=True)
class NumberBet:
    amount: float
    number: int


@dataclass(frozen=True)
class ColorBet:
    amount: float
    color: Color


Bet = NumberBet | ColorBet
