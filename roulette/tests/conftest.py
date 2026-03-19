"""Shared step definitions for both deterministic and stochastic roulette tests."""

from pytest_bdd import given, when, then, parsers

from roulette import FairRoulette, Color, ColorBet, NumberBet


def _parse_bet(amount: int, choice: str) -> ColorBet | NumberBet:
    """Parse a string bet choice from the feature file into a typed Bet ADT."""
    try:
        return NumberBet(amount, int(choice))
    except ValueError:
        return ColorBet(amount, Color(choice))


# ---------------------------------------------------------------------------
# Stochastic inner step definitions
# These steps are used inside embedded Atomic Behaviors. They also work in
# deterministic tests because stochastic_sample is a no-op fixture by default.
# ---------------------------------------------------------------------------

@given(
    parsers.parse("a new roulette game with a starting balance of {start_balance:d} chips"),
    target_fixture="roulette_context",
)
def given_new_game_stochastic(start_balance):
    return {"game": FairRoulette(start_balance), "initial_balance": start_balance}


@when(parsers.parse('the player bets {amount:d} chips on "{bet_choice}"'))
def when_place_bet_stochastic(roulette_context, amount, bet_choice):
    roulette_context["game"].place_bet(_parse_bet(amount, bet_choice))


@when("the wheel is spun")
def when_spin_stochastic(roulette_context):
    roulette_context["game"].spin()


@then(parsers.parse("the system identifies the winning {entity}"))
def then_identify_winning(roulette_context, entity):
    assert roulette_context["game"].winning_number is not None


@then(parsers.parse('pays the player if the winning {entity} is {target} and the bet was "{bet_choice}"'))
def then_pays_player(roulette_context, entity, target, bet_choice, stochastic_sample):
    game = roulette_context["game"]

    # Only resolve if the bet hasn't already been resolved by a prior conditional step
    if game.bet is None:
        return

    # Check if the condition matches
    if entity == "number":
        match = game.winning_number == int(target)
    else:  # color
        match = game.COLORS[game.winning_number].value == target

    if not match:
        return

    net_payout = game.resolve_bet()
    roulette_context["resolved"] = True
    stochastic_sample.observe(
        winning_number=game.winning_number,
        color_result=game.COLORS[game.winning_number].value,
        player_payout=float(net_payout),
        rng_seed=game.seed_used,
    )


@then("awards the bet to the house in all other cases")
def then_house_wins(roulette_context, stochastic_sample):
    game = roulette_context["game"]

    # If no prior conditional step resolved the bet, the house wins
    if game.bet is None:
        return

    net_payout = game.resolve_bet()
    stochastic_sample.observe(
        winning_number=game.winning_number,
        color_result=game.COLORS[game.winning_number].value,
        player_payout=float(net_payout),
        rng_seed=game.seed_used,
    )
