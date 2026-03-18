import logging
import random

from pytest_bdd import scenarios, given, when, then, parsers

logger = logging.getLogger(__name__)

from roulette import FairRoulette, Color, ColorBet, NumberBet


def _parse_bet(amount: int, choice: str) -> ColorBet | NumberBet:
    """Parse a string bet choice from the feature file into a typed Bet ADT."""
    try:
        return NumberBet(amount, int(choice))
    except ValueError:
        return ColorBet(amount, Color(choice))


scenarios("features/number_bet.feature")
scenarios("features/color_bet.feature")


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------

@given(
    parsers.parse("a new roulette game with a starting balance of {start_balance:d} chips"),
    target_fixture="roulette_context",
)
def given_new_game(start_balance):
    game = FairRoulette(start_balance)
    return {
        "game": game,
        "initial_balance": start_balance,
    }


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------

@when(parsers.parse('the player bets {amount:d} chips on "{bet_choice}"'))
def when_place_bet(roulette_context, amount, bet_choice):
    roulette_context["game"].place_bet(_parse_bet(amount, bet_choice))


@when(parsers.parse("the wheel is spun with seed {seed:d}"))
def when_spin(roulette_context, seed):
    random.seed(seed)
    game = roulette_context["game"]
    game.spin()
    color = game.COLORS[game.winning_number]
    logger.info("Spin result: number=%d, color=%s", game.winning_number, color.value)


# ---------------------------------------------------------------------------
# Then
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
