from abc import ABC, abstractmethod

from roulette.types import Bet, ColorBet, NumberBet, Color


class BaseRoulette(ABC):
    COLORS: dict[int, Color]

    def __init__(self, balance: float = 0.0) -> None:
        self.balance = balance
        self.bet: Bet | None = None
        self.winning_number: int | None = None
        self.payout: float = 0.0
        self.seed_used: str = ""

    @abstractmethod
    def spin(self) -> int:
        """Spin the wheel and return the winning pocket number."""

    def place_bet(self, bet: Bet) -> None:
        self.bet = bet
        self.balance -= bet.amount

    def resolve_bet(self) -> float:
        if self.winning_number is None:
            raise RuntimeError("Must spin before resolving")
        if self.bet is None:
            raise RuntimeError("No bet placed")

        winning_color = self.COLORS[self.winning_number]

        match self.bet:
            case NumberBet(amount, number):
                self.payout = amount * 36 if number == self.winning_number else 0.0
            case ColorBet(amount, color):
                self.payout = amount * 2 if color == winning_color else 0.0

        self.balance += self.payout
        net = self.payout - self.bet.amount
        self.bet = None
        return net
