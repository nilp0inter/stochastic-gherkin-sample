Stochastic Feature: Roulette Fair Play Validation

  Stochastic Scenario: Verify the RNG color distribution conforms to European Roulette probabilities

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
      Scenario Outline: Processing 1:1 payouts for color bets
        Given a new roulette game with a starting balance of 100 chips
        When the player bets 10 chips on "<color_choice>"
        And the wheel is spun
        Then the system identifies the winning color
        And pays the player if the winning color is Red and the bet was "Red"
        And pays the player if the winning color is Black and the bet was "Black"
        And awards the bet to the house in all other cases

        Examples:
          | color_choice |
          | Red          |
          | Black        |

    Then the statistical assertion "Green_Occurrence" is met:
      | Observation  | Filter | Operator | Value |
      | color_result | Green  | >=       | 0.025 |
      | color_result | Green  | <=       | 0.029 |

    And the statistical assertion "Red_Occurrence" is met:
      | Observation  | Filter | Operator | Value |
      | color_result | Red    | >=       | 0.470 |
      | color_result | Red    | <=       | 0.495 |

    And the statistical assertion "Black_Occurrence" is met:
      | Observation  | Filter | Operator | Value |
      | color_result | Black  | >=       | 0.470 |
      | color_result | Black  | <=       | 0.495 |
