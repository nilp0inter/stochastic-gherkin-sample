from abc import ABC, abstractmethod


class BaseRoulette(ABC):
    POCKETS: dict[int, str]

    def __init__(self, balance: float = 0.0) -> None:
        self._balance = balance
        self._bet_amount: float = 0.0
        self._bet_choice: int | str | None = None
        self._last_pocket: int | None = None

    @property
    def balance(self) -> float:
        return self._balance

    @abstractmethod
    def spin(self) -> int:
        """Spin the wheel and return the winning pocket number."""

    def color(self, pocket: int) -> str:
        """Return the color for a pocket number."""
        return self.POCKETS[pocket]

    def place_bet(self, amount: float, choice: int | str) -> None:
        """Place a bet. Choice can be a pocket number (int) or a color name (str)."""
        if amount <= 0:
            raise ValueError("Bet amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient balance")
        self._bet_amount = amount
        self._bet_choice = choice
        self._balance -= amount

    def resolve(self) -> float:
        """Resolve the last spin against the current bet. Returns net payout."""
        if self._last_pocket is None:
            raise RuntimeError("Must spin before resolving")
        if self._bet_choice is None:
            raise RuntimeError("No bet placed")

        pocket = self._last_pocket
        pocket_color = self.POCKETS[pocket]
        payout = 0.0

        if isinstance(self._bet_choice, int):
            if self._bet_choice == pocket:
                payout = self._bet_amount * 36  # 35:1 plus original bet
        elif isinstance(self._bet_choice, str):
            if self._bet_choice == pocket_color:
                payout = self._bet_amount * 2  # 1:1 plus original bet

        self._balance += payout
        net = payout - self._bet_amount
        self._bet_amount = 0.0
        self._bet_choice = None
        return net
