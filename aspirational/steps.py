from behave import given, when, then
import pandas as pd # Used by the framework to process metadata

from roulette import FairRoulette, Color, ColorBet, NumberBet


# ========================================================================
# ATOMIC BEHAVIOR STEPS (Developer's Deterministic Tests)
# ========================================================================

def _parse_bet(amount: int, choice: str) -> ColorBet | NumberBet:
    """Parse a string bet choice from the feature file into a typed Bet ADT."""
    try:
        return NumberBet(amount, int(choice))
    except ValueError:
        return ColorBet(amount, Color(choice))

@given('a new roulette game with a starting balance of {start_balance:d} chips')
def step_start_game(context, start_balance):
    context.game = FairRoulette(start_balance)
    context.initial_balance = start_balance

@when('the player bets {amount:d} chips on "{bet_choice}"')
def step_place_bet(context, amount, bet_choice):
    context.game.place_bet(_parse_bet(amount, bet_choice))

@when('the wheel is spun')
def step_spin_wheel(context):
    context.game.spin()

@then('the system identifies the winning {entity}')
def step_identify_winner(context, entity):
    # Deterministic assertion ensures the API generated a valid state before continuing
    assert context.game.winning_number is not None

@then('pays the player if the winning {entity} is {target} and the bet was "{bet_choice}"')
def step_pay_winner(context, entity, target, bet_choice):
    net_payout = context.game.resolve_bet()

    # Deterministic assertion: Did the API pay correctly for a win?
    winning_color = context.game.COLORS[context.game.winning_number]
    if (entity == "color" and winning_color == Color(target)) or \
       (entity == "number" and context.game.winning_number == int(target)):
        assert context.game.balance > context.initial_balance

    # --- FRAMEWORK MAGIC: YIELDING THE OBSERVATION ---
    # The developer feeds the stochastic engine from inside the atomic test!
    context.sample.observe(
        winning_number=context.game.winning_number,
        color_result=context.game.COLORS[context.game.winning_number].value,
        player_payout=float(net_payout),
        rng_seed=context.game.seed_used
    )

@then('awards the bet to the house in all other cases')
def step_house_wins(context):
    # A simple deterministic UI/State check could go here
    pass


# ========================================================================
# 3. STOCHASTIC FRAMEWORK STEPS (The Engine's Meta-Steps)
# ========================================================================

@given('the following Execution Strategy:')
def step_execution_strategy(context):
    # The framework parses the table into a configuration object
    context.stochastic_engine.config = {row['Setting']: row['Value'] for row in context.table}

@given('the following Sample Schema:')
def step_sample_schema(context):
    # The framework prepares the strict schema validation for the observations
    context.stochastic_engine.build_schema(context.table)

@when('the following Atomic Behavior is executed iteratively:')
def step_execute_iterations(context):
    """
    Note: Because we are using the Custom Parser approach, this step acts as 
    the trigger. Inside, the framework takes the child AST (the inner Scenarios), 
    loops them up to 'Maximum Samples', collects the 'context.sample.observe()' 
    calls, and compiles them into a Pandas DataFrame.
    """
    # Pretend API triggering the engine loop
    context.stochastic_engine.run_atomic_loop(max_iterations=int(context.stochastic_engine.config['Maximum Samples']))
    
    # Once finished, the data is available as a DataFrame for the Then steps
    # context.samples_df = pd.DataFrame([...50,000 rows of observations...])

@then('the statistical assertion "{assertion_name}" is met:')
def step_statistical_assertion(context, assertion_name):
    # We retrieve the dataset of the 50,000 runs
    df = context.stochastic_engine.samples_df 
    total_samples = len(df)
    
    for row in context.table:
        observation = row['Observation']
        operator = row['Operator']
        target_value = float(row['Value'])
        
        # ----------------------------------------------------
        # Logic A: Data Filtering (e.g., Occurrences of "Red")
        # ----------------------------------------------------
        if 'Filter' in row.headings:
            filter_val = row['Filter']
            # Pandas calculates how many rows match the string (e.g., 'Red')
            occurrences = len(df[df[observation] == filter_val])
            actual_value = occurrences / total_samples
            
        # ----------------------------------------------------
        # Logic B: Data Aggregation (e.g., Average Payout)
        # ----------------------------------------------------
        elif 'Aggregation' in row.headings:
            aggregation = row['Aggregation']
            if aggregation == "Average":
                # Pandas calculates the mean of the float column
                actual_value = df[observation].mean()
        
        # ----------------------------------------------------
        # Dynamic Evaluation
        # ----------------------------------------------------
        if operator == ">=":
            assert actual_value >= target_value, \
                f"[{assertion_name}] FAIL: {observation} was {actual_value:.4f}, expected >= {target_value}"
        elif operator == "<=":
            assert actual_value <= target_value, \
                f"[{assertion_name}] FAIL: {observation} was {actual_value:.4f}, expected <= {target_value}"
