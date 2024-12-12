# GameSweeper: Enhancing Game Analysis with Game Theory Algorithms and Dynamic Refinement Metrics: A Case Study on Minesweeper

This project aims to improve Minesweeper AI performance and analysis by integrating advanced game theory techniques, dynamic game refinement (GR) metrics, and probabilistic reasoning. The work extends beyond conventional heuristics to include Bayesian inference for probability estimation, Markov Decision Processes (MDPs) for sequential decision-making, and dynamic GR metrics to analyze player engagement and complexity over time.

## Table of Contents

1. [Introduction](#introduction)  
2. [Project Structure](#project-structure)  
3. [Components Overview](#components-overview)  
   - [Game Logic](#game-logic)  
   - [AI and Game Theory Models](#ai-and-game-theory-models)  
   - [Metrics and Logging](#metrics-and-logging)  
   - [Utilities](#utilities)  
4. [Running the Simulation](#running-the-simulation)  
5. [Evaluating Results](#evaluating-results)  
6. [Game Theory and GR Metrics Explained](#game-theory-and-gr-metrics-explained)  
7. [Future Work](#future-work)  

## Introduction

Minesweeper is a classic puzzle that requires deducing the location of mines from numerical clues. While the rules are simple, the strategic depth and uncertainty make it an excellent model for testing game theory algorithms and analyzing player engagement.

This project advances Minesweeper AI by:  
- Using **Bayesian Inference** to calculate probabilities of cells being mines.  
- Employing **MDPs** to choose actions that maximize long-term expected utility.  
- Integrating **Dynamic Game Refinement (GR)** metrics to measure changes in complexity, uncertainty, and psychological engagement (acceleration, jerk) over the course of the game.

## Project Structure

```
project/
│
├─ src/
│  ├─ game/
│  │  ├─ board.py
│  │  ├─ cell.py
│  │  ├─ game_manager.py
│  │  └─ __init__.py
│  │
│  ├─ ai/
│  │  ├─ bayesian.py
│  │  ├─ mdp.py
│  │  ├─ pattern_solver.py
│  │  └─ __init__.py
│  │
│  ├─ metrics/
│  │  ├─ dynamic_gr.py
│  │  └─ __init__.py
│  │
│  └─ utils/
│     ├─ logger.py
│     └─ __init__.py
│
└─ run_simulation.py
```

## Components Overview

### Game Logic (src/game)

- **board.py**:  
  Creates and manages the Minesweeper board, places mines, calculates neighbor mine counts, and handles revealing cells and checking victory conditions.

- **cell.py**:  
  Defines the `Cell` class, representing a single tile (mine, revealed, flagged).

- **game_manager.py**:  
  Provides a simple interface for making moves (reveal/flag), checking game state (win/lose), and advancing the game.

### AI and Game Theory Models (src/ai)

- **bayesian.py**:  
  Implements methods to estimate the probability of each unrevealed cell being a mine. It collects constraints from revealed clues and uses local heuristics or simplified constraint-based reasoning when global constraints are infeasible.

- **mdp.py**:  
  Models Minesweeper as a sequential decision-making problem. Uses a depth-limited lookahead or heuristic approach to choose actions that maximize expected rewards. The MDP encapsulates uncertainty and future consequences of actions, aligning with game theory’s emphasis on strategic planning and optimal policies.

- **pattern_solver.py**:  
  Recognizes deterministic patterns and forced moves (like if a clue matches exactly the number of unrevealed neighbors) to minimize guesswork. Using pattern recognition reduces dependency on probabilistic inference and improves decision-making quality.

### Metrics and Logging (src/metrics and src/utils)

- **dynamic_gr.py**:  
  Implements the Dynamic Game Refinement metric. Extends traditional GR theory by incorporating:
  - Changing complexity over time.
  - Uncertainty (entropy) from probabilistic reasoning.
  - Psychological metrics: acceleration and jerk, derived from the rate of safe cell revelations over time.

- **logger.py**:  
  Logs GR metrics per step into a CSV file (`gr_metrics.csv`). This allows for post-game analysis of engagement and complexity trends.

### Utilities (src/utils)

- General utility functions and classes (e.g., for logging and data handling).

## Running the Simulation

1. **Dependencies:**  
   - Python 3.9+ (recommended)
   - `pip install pulp` (if using linear/integer programming, optional in the improved version)
   - Other standard libraries (no additional installations required for `copy`, `csv`, etc. as they are part of Python’s standard library).

2. **Run a Simulation:**  
   ```bash
   python run_simulation.py
   ```
   This will run a series of Minesweeper games using the AI described above.

3. **Outputs:**  
   - Console output: Shows win/lose outcomes of each game.
   - `gr_metrics.csv`: Logs dynamic GR values, complexity, entropy, and psychological metrics each step.

## Evaluating Results

- **Win/Loss Ratio:**  
  After running multiple games, review how often the AI wins. Increasing the number of simulations (e.g., 20+ games) provides statistically meaningful results.

- **Complexity and Entropy Trends:**  
  Examine `gr_metrics.csv` to see if the entropy decreases over time as the AI gains information. Ideally, complexity should lower as safe cells are revealed, and entropy should reduce, reflecting improved certainty.

- **GR Values:**  
  Assess how GR evolves as the game progresses. Higher GR may indicate balanced complexity and engagement. Sudden changes in GR (and acceleration/jerk) highlight dynamic shifts in player (or AI) decision-making tension.

## Game Theory and GR Metrics Explained

- **Game Theory Aspects (MDP & Probabilities):**  
  The MDP framework treats Minesweeper as a game of incomplete information. Each decision (reveal/flag) is made under uncertainty. Bayesian inference provides probabilities of mines to guide these decisions. This combination reflects fundamental game-theoretic principles:
  - **Strategic Decision-Making:** Choosing actions that maximize expected utility (winning probability).
  - **Sequential Reasoning:** Each move updates the state of the game and the AI’s knowledge, similar to multi-stage decision-making in game theory.
  
- **Dynamic Game Refinement (GR) Theory:**  
  Traditional GR theory provides a measure of game engagement. Here we enhance it by:
  - Incorporating time-dependent factors and psychological metrics (acceleration and jerk of safe reveals).
  - Measuring entropy to represent uncertainty, capturing how learning (via Bayesian updates) affects perceived complexity.
  
  These enhancements offer a richer view of the game’s evolving difficulty and the AI’s internal decision tension, providing new insight into how uncertainty and learning shape the gameplay experience.

## Future Work

- **More Advanced Pattern Recognition:**  
  Incorporate additional known Minesweeper patterns for fewer guesses and improved performance.

- **Deeper MDP and Reinforcement Learning:**  
  Extend the MDP into a full reinforcement learning framework, possibly with Monte Carlo Tree Search or Q-learning for more robust strategies.

- **Refined Probability Models:**  
  Explore more sophisticated statistical methods or factor graph approaches for probability inference, improving accuracy when constraints are complex.

- **Broader Application:**  
  Apply the methodology to other puzzle/strategy games to test the generality of these approaches.
