Stochastic Feature: Roulette Fair Play Validation  
  
  Stochastic Scenario: Verify the average house edge on a single number bet  
  
    Given the following Execution Strategy:  
      | Setting         | Value |  
      | Maximum Samples | 50000 |  
      | Warmup Samples  | 500   |  
      | Fail Fast       | false |  
  
    And the following Sample Schema:  
      | Observation     | Type    | Description                               |  
      | winning_number  | Integer | The exact pocket the ball landed in       |  
      | color_result    | String  | The color evaluated by the engine         |  
      | player_payout   | Float   | The net chip fluctuation                  |  
      | rng_seed        | String  | The randomness seed for reproducibility   |  
  
    When the following Atomic Behavior is executed iteratively:  
      Scenario: Processing a 35:1 payout for a single number bet
        Given a new roulette game with a starting balance of 100 chips
        When the player bets 10 chips on "17"
        And the wheel is spun
        Then the system identifies the winning number
        And pays the player if the winning number is 17 and the bet was "17"
        And awards the bet to the house in all other cases
  
    Then the statistical assertion "Expected_House_Edge" is met:  
      | Observation   | Aggregation | Operator | Value |  
      | player_payout | Average     | >=       | -0.40 |  
      | player_payout | Average     | <=       | -0.15 |  
