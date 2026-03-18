import logging
import random

from pytest_bdd import scenarios, given, when, then, parsers

logger = logging.getLogger(__name__)

from roulette import FairRoulette, Color, ColorBet, NumberBet


scenarios("features/number_bet.feature")
scenarios("features/color_bet.feature")


# ---------------------------------------------------------------------------
# When (deterministic-only steps with seed)
# ---------------------------------------------------------------------------

@when(parsers.parse("the wheel is spun with seed {seed:d}"))
def when_spin(roulette_context, seed):
    random.seed(seed)
    game = roulette_context["game"]
    game.spin()
    color = game.COLORS[game.winning_number]
    logger.info("Spin result: number=%d, color=%s", game.winning_number, color.value)


# ---------------------------------------------------------------------------
# Then (deterministic-only assertions)
# ---------------------------------------------------------------------------

@then(parsers.parse("the winning number is {number:d}"))
def then_winning_number(roulette_context, number):
    assert roulette_context["game"].winning_number == number


@then(parsers.parse('the winning color is "{color}"'))
def then_winning_color(roulette_context, color):
    game = roulette_context["game"]
    assert game.COLORS[game.winning_number] == Color(color)


@then("the player is paid out")
def then_player_paid(roulette_context):
    game = roulette_context["game"]
    net_payout = game.resolve_bet()
    logger.info("Payout: net=%+.1f, balance=%.1f", net_payout, game.balance)
    assert game.balance > roulette_context["initial_balance"]
