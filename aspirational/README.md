# Stochastic Testing Framework: Roulette Implementation

This repository contains a reference implementation of a Domain-Specific extension to Gherkin (BDD), designed to automate the testing of non-deterministic and stochastic systems.

## Problem Statement

Standard BDD frameworks (such as Behave, Cucumber, or Pytest-BDD) are designed for deterministic testing. They evaluate a single execution path and return a tri-state result (Pass/Fail/Error). 

However, when testing stochastic systems (e.g., Random Number Generators, Machine Learning models, or complex behavioral economies), a single execution is insufficient to determine system correctness. System validation requires evaluating the **statistical distribution** of outcomes over $N$ iterations.

Attempting to force iterative statistical evaluation into standard BDD typically results in semantic overloading—such as hiding `while` loops, data aggregation, and statistical math within a single `Then` step. This destroys test readability, traceability, and state isolation.

## Architectural Solution

This framework resolves the limitation by introducing a **Meta-Testing Architecture** via a custom Gherkin superset. It explicitly separates the orchestrator (Macro) from the payload (Micro).

1. **The Micro-Domain (Atomic Behavior):** A standard, deterministic BDD scenario representing a single system interaction.
2. **The Macro-Domain (Stochastic Scenario):** A wrapper that declares configuration limits, defines a strict data schema, iteratively executes the Micro-Domain, and queries the aggregated results.

## Framework Semantics and Syntax

The extension introduces specialized keywords and blocks to handle the macro-execution lifecycle logically from top to bottom:

### 1. Top-Level Domain Boundaries
To prevent the standard BDD runner from attempting to execute a simulation sequentially, the framework introduces domain-specific root keywords: **`Stochastic Feature`** and **`Stochastic Scenario`**. 

These act as routing directives. When the custom parser reads these keywords, it delegates the entire block to the Stochastic Orchestration Engine instead of the standard task runner.

```gherkin
Stochastic Feature: Roulette Fair Play Validation  
  
  Stochastic Scenario: Verify the average house edge on a single number bet  
```

### 2. Engine Configuration and Contract Definition
Inside the Stochastic Scenario, the environment is initialized by defining the execution boundaries and the strict shape of the data that will be collected during the iterations.

```gherkin
    Given the following Execution Strategy:  
      | Setting         | Value |  
      | Maximum Samples | 50000 |  

    And the following Sample Schema:  
      | Observation     | Type    | Description                               |  
      | color_result    | String  | The color evaluated by the engine         |  
```
*Note: Declaring the schema in the feature file allows the framework to enforce strict type validation during runtime and establishes a single source of truth for downstream data-analysis tools.*

### 3. Execution Payload (Atomic Behavior)
This block represents the Micro-Domain. It is written in standard Gherkin. The Stochastic runner parses this block, treats it as an independent test suite, and executes it iteratively based on the `Execution Strategy`.

```gherkin
    When the following Atomic Behavior is executed iteratively:  
      Scenario Outline: Processing 1:1 payouts for color bets
        Given a new roulette game with a starting balance of 100 chips
        When the player bets 10 chips on "<color_choice>"
        Then the system identifies the winning color
```
*Implementation Note:* Inside the Python step definition for the core `Then` step, the developer calls `context.sample.observe(color_result="Red")`. This yields the iteration's data point back to the orchestration engine without breaking the deterministic test flow.

### 4. Statistical Aggregation and Assertion
Once the engine completes the specified iterations, it compiles the yielded observations into a localized, queryable dataset (e.g., a Pandas DataFrame). The final assertions act as declarative data queries against this exact dataset.

```gherkin
    Then the statistical assertion "Red_Occurrence" is met:  
      | Observation  | Filter | Operator | Value |  
      | color_result | Red    | >=       | 0.470 |  
      | color_result | Red    | <=       | 0.495 |  
```
