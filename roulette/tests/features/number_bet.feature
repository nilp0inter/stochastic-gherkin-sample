Feature: Single Number Bet Processing

  Scenario: Processing a 35:1 payout for a single number bet
    Given a new roulette game with a starting balance of 100 chips
    When the player bets 10 chips on "17"
    And the wheel is spun with seed 45
    Then the winning number is 17
    And the player is paid out
