import random

from roulette.base import BaseRoulette

# fmt: off
RED_POCKETS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
# fmt: on


class FairRoulette(BaseRoulette):
    POCKETS: dict[int, str] = {0: "Green"}
    POCKETS.update({i: ("Red" if i in RED_POCKETS else "Black") for i in range(1, 37)})

    def spin(self) -> int:
        self._last_pocket = random.randint(0, 36)
        return self._last_pocket
