Feature: Color Bet Processing

  Scenario Outline: Processing 1:1 payouts for color bets
    Given a new roulette game with a starting balance of 100 chips
    When the player bets 10 chips on "<color_choice>"
    And the wheel is spun with seed <seed>
    Then the winning color is "<color_choice>"
    And the player is paid out

    Examples:
      | color_choice | seed |
      | Red          | 2    |
      | Black        | 0    |
