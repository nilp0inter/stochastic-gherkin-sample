import random

from roulette.base import BaseRoulette
from roulette.types import Color

# fmt: off
RED_POCKETS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
# fmt: on


class FairRoulette(BaseRoulette):
    COLORS: dict[int, Color] = {0: Color.GREEN}
    COLORS.update({i: (Color.RED if i in RED_POCKETS else Color.BLACK) for i in range(1, 37)})

    def spin(self) -> int:
        self.winning_number = random.randint(0, 36)
        self.seed_used = hex(random.getrandbits(16))
        return self.winning_number
