# **GameSweeper AI: Enhancing Game Analysis with Game Theory Algorithms and Dynamic Refinement Metrics**

## 🚀 **Project Overview**

GameSweeper AI is an advanced Minesweeper agent leveraging **Game Theory**, **Dynamic Game Refinement (GR) Metrics**, and **Reinforcement Learning** to optimize decision-making and improve performance over time. By integrating **Bayesian Inference**, **Markov Decision Processes (MDPs)**, and **Entropy Analysis**, the project provides a robust framework for strategic gameplay and deeper insights into complexity trends.

The project aims to:
- Improve AI decision-making using **Bayesian Probability Models** and **MDPs**.
- Analyze **Entropy**, **Complexity**, and **Dynamic Game Refinement (GR) Metrics**.
- Compare AI performance against **Classic Human-like Heuristics**.
- Enable continuous improvement through **Experience Data Storage**.

---

## 📚 **Table of Contents**

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
7. [Continuous AI Learning](#continuous-ai-learning)  
8. [Future Work](#future-work)  

---

## 🧠 **Introduction**

Minesweeper is a classic puzzle requiring logical deduction and probabilistic reasoning. While simple in rules, the game's strategic depth and uncertainty make it an excellent testbed for **Game Theory** algorithms and **AI decision systems**.

### **Core Objectives:**
- Use **Bayesian Inference** for mine probability estimation.
- Apply **Markov Decision Processes (MDPs)** for sequential, utility-driven decision-making.
- Leverage **Dynamic GR Metrics** to monitor engagement, uncertainty, and decision-making tension.

This project goes beyond traditional heuristic approaches by implementing adaptive AI techniques and robust data analysis.

---

## 📂 **Project Structure**

```
GameSweeper/
├── run_simulation.py     # Main simulation runner
├── src/
│   ├── game/
│   │   ├── board.py      # Board representation and game logic
│   │   ├── cell.py       # Cell properties and states
│   │   ├── game_manager.py # High-level game operations
│   ├── ai/
│   │   ├── ai_agent.py   # Core AI logic
│   │   ├── bayesian_model.py # Bayesian probability calculations
│   │   ├── mdp_solver.py # MDP solver for strategic planning
│   │   ├── pattern_solver.py # Pattern recognition for deterministic moves
│   │   ├── learning_manager.py # AI experience storage and retrieval
│   ├── metrics/
│   │   ├── dynamic_gr.py # Dynamic Game Refinement calculations
│   │   ├── metrics.py    # Entropy and complexity metrics
│   ├── utils/
│   │   ├── logger.py     # Logs game progress and metrics
│   │   ├── visualizer.py # Console board printing
├── experience_data.json  # AI learning history
├── analysis.ipynb        # Post-simulation analysis notebook
├── README.md             # Project documentation
```

---

## 🛠️ **Components Overview**

### ✅ **Game Logic (`src/game`)**
- **board.py**: Handles board creation, mine placement, and cell operations.
- **cell.py**: Represents individual cell states (e.g., flagged, revealed).
- **game_manager.py**: Coordinates moves, validates win/loss states, and manages overall game flow.

### ✅ **AI and Game Theory Models (`src/ai`)**
- **ai_agent.py**: Core AI logic for decision-making.
- **bayesian_model.py**: Calculates probabilities for each cell using Bayesian reasoning.
- **mdp_solver.py**: Implements Markov Decision Processes for optimal sequential actions.
- **pattern_solver.py**: Recognizes deterministic patterns to reduce randomness in moves.
- **learning_manager.py**: Stores and retrieves AI learning experiences from `experience_data.json`.

### ✅ **Metrics and Logging (`src/metrics`)**
- **dynamic_gr.py**: Computes dynamic GR metrics, including psychological metrics like acceleration and jerk.
- **metrics.py**: Tracks entropy, complexity, and GR over time.
- **logger.py**: Logs step-by-step actions and outcomes into `gr_metrics.csv`.

### ✅ **Utilities (`src/utils`)**
- **visualizer.py**: Prints the board state after each move for easy debugging.
- **logger.py**: Logs game states and metrics.

---

## 🚦 **Running the Simulation**

1. **Dependencies:**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Simulations:**  
   ```bash
   python run_simulation.py
   ```

3. **Outputs:**
- Win/Loss Ratio
- Entropy Trends
- Complexity Analysis
- Logs in `experience_data.json` and `gr_metrics.csv`

4. **Visualize Board Progress:**  
   Board state is printed after every AI action for better transparency.

---

## 📊 **Evaluating Results**

### ✅ **1. Win/Loss Ratio**
- Compares AI and Classic approaches.
- Provides statistical insight into the AI's learning efficiency.

### ✅ **2. Entropy Trends**
- Measures uncertainty reduction over time.
- Lower final entropy indicates improved certainty.

### ✅ **3. Complexity Analysis**
- Tracks complexity trends as the game progresses.

### ✅ **4. Dynamic GR Metrics**
- Tracks **GR**, **Acceleration**, and **Jerk** values.
- Analyzes AI decision tension and engagement.

### 📈 **Post-Simulation Analysis:**
Run the **`analysis.ipynb`** notebook to generate graphs and tables.

---

## 🎲 **Game Theory and GR Metrics Explained**

### ✅ **Game Theory Aspects:**
- **Bayesian Inference:** Calculates probabilities of mines in neighboring cells.
- **MDP Framework:** Optimizes sequential moves for long-term utility.

### ✅ **Dynamic GR Metrics:**
- Tracks **Game Rigidity (GR)** to measure complexity and engagement.
- Monitors **Entropy**, **Acceleration**, and **Jerk** as psychological proxies.

These metrics create a richer understanding of the AI’s decision-making process and the evolving game state.

---

## 🤖 **Continuous AI Learning**

### ✅ **How It Works:**
1. **Experience Storage:** Logs each run in `experience_data.json`.
2. **Pattern Recognition:** Identifies high-probability moves.
3. **Entropy Reduction:** Updates probabilities for future games.
4. **Self-Improvement:** Adjusts AI logic after every iteration.

### ✅ **Benefits:**
- Smarter AI decision-making over time.
- Reduced reliance on guesswork.
- Faster convergence towards optimal strategies.

---

## 🔮 **Future Work**
1. **Incorporate Neighbor Clues:** Better pattern analysis for safer moves.
2. **Advanced MDP Integration:** Longer planning horizons.
3. **Monte Carlo Methods:** Better handling of probabilistic edge cases.
4. **Scaling Grid Size:** Larger grids for deeper testing.
