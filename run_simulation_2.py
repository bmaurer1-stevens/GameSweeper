import random
import pandas as pd
from src.game.board import Board
from src.game.game_manager import GameManager
from src.ai.bayesian import BayesianAnalyzer
from src.ai.mdp import MDP
from src.ai.pattern_solver import PatternSolver
from src.ai.learning_manager import LearningManager
from src.metrics.dynamic_gr import DynamicGR
from src.utils.logger import CSVLogger  # Import the CSVLogger
import os
import sys

# Redirect all print statements to a log file
log_filename = "simulation_log.txt"
sys.stdout = open(log_filename, "w")

def board_state_hash(board):
    """
    Simple state hash: frozensets of flagged and revealed.
    """
    flagged_positions = []
    revealed_positions = []
    for y in range(board.height):
        for x in range(board.width):
            c = board.grid[y][x]
            if c.flagged:
                flagged_positions.append((x, y))
            if c.revealed:
                revealed_positions.append((x, y))
    return (frozenset(flagged_positions), frozenset(revealed_positions))


def print_board_and_probabilities(board, probabilities):
    """Prints the board and its corresponding probability matrix."""
    print("\nGame Board:")
    print(str(board))

    print("\nProbability Matrix:")
    for y in range(board.height):
        row_probs = []
        for x in range(board.width):
            cell = board.grid[y][x]
            if cell.revealed:
                row_probs.append("Revealed")
            elif cell.flagged:
                row_probs.append("Flagged")
            else:
                prob = probabilities.get((x, y), None)
                if prob is not None:
                    row_probs.append(f"{prob:.2f}")
                else:
                    row_probs.append("N/A")
        print(" ".join(row_probs))


def run_ai_game_with_visualization(width=5, height=5, mines=5, max_steps=50, learning_mgr=None, game_key="5x5_5mines", game_id=1):
    """
    AI approach with visualization of each step, including DynamicGR updates.
    Each game logs to a separate CSV file.
    """
    board = Board(width, height, mines)
    gm = GameManager(board)
    bayes = BayesianAnalyzer()
    pattern_solver = PatternSolver()
    dynamic_gr = DynamicGR()  # Initialize DynamicGR

    # Create a unique filename for the current game
    csv_filename = f"gr_metrics_game_{game_id}.csv"
    logger = CSVLogger(csv_filename)  # Initialize CSV Logger for this game

    gm.make_move(width // 2, height // 2, "reveal")  # optional first reveal in center

    step = 0
    while not gm.is_over() and step < max_steps:
        # Build a state hash for learning
        st_hash = board_state_hash(board)

        # Compute probabilities
        probabilities = bayes.compute_probabilities(board)

        # Update DynamicGR and get metrics
        gr_value, gr_data = dynamic_gr.update(board, step, probabilities)
        print(f"\nStep {step}:")
        print(f"DynamicGR Value: {gr_value:.4f}")  # Display DynamicGR value
        print(f"DynamicGR Metrics: {gr_data}")  # Display other metrics

        # Log DynamicGR metrics to CSV
        logger.log(step, {**gr_data, 'game_id': game_id})

        # Print the board and probabilities
        print_board_and_probabilities(board, probabilities)

        # Select action using existing logic
        best_act_from_history = None
        if learning_mgr:
            best_act_from_history = learning_mgr.best_action_for_state(game_key, st_hash)

        if best_act_from_history:
            act_type, x, y = best_act_from_history
            gm.make_move(x, y, act_type)
        else:
            forced_moves = pattern_solver.find_forced_moves(board)
            if forced_moves:
                fm = forced_moves[0]
                gm.make_move(fm[1], fm[2], fm[0])
            else:
                mdp = MDP(board, probabilities, depth=3)  # Initialize MDP
                action = mdp.find_best_action()  # Use MDP to find the best action
                if action:
                    act_type, x, y = action
                    gm.make_move(x, y, act_type)
                else:
                    action = guess_safest_cell(board, bayes)
                    if not action:
                        break
                    act_type, x, y = action
                    gm.make_move(x, y, act_type)

        step += 1

    outcome = "win" if gm.is_victory() else "lose"
    print(f"\nGame Over: {outcome}")
    return gm.is_victory()


def run_classic_game_with_visualization(width=5, height=5, mines=5, max_steps=50):
    """
    Classic approach with visualization of each step.
    """
    board = Board(width, height, mines)
    gm = GameManager(board)

    step = 0
    while not gm.is_over() and step < max_steps:
        unrevealed = board.get_unrevealed_cells()
        if not unrevealed:
            break

        # Randomly select an unrevealed cell to reveal
        cell = random.choice(unrevealed)
        gm.make_move(cell.x, cell.y, "reveal")

        # Print the board after the move
        print(f"\nStep {step}:")
        print("\nGame Board:")
        print(str(board))

        step += 1

    outcome = "win" if gm.is_victory() else "lose"
    print(f"\nGame Over: {outcome}")
    return gm.is_victory()


def guess_safest_cell(board, bayes):
    unrevealed = board.get_unrevealed_cells()
    if not unrevealed:
        return None
    probs = bayes.compute_probabilities(board)
    best_cell = None
    best_prob = 1.0
    for c in unrevealed:
        p = probs.get((c.x, c.y), 0.5)
        if p < best_prob:
            best_prob = p
            best_cell = (c.x, c.y)
    return ("reveal", best_cell[0], best_cell[1])


if __name__ == "__main__":
    from src.ai.learning_manager import LearningManager

    num_games = 10  # Total games in a batch (5 classic, 5 AI)
    learning_mgr = LearningManager("experience_data.json")
    game_key = "5x5_5mines"
    batch_count = 0
    threshold = 0.9
    max_batches = 10
    max_ai_win_rate = 0.0
    while batch_count < max_batches:
        batch_count += 1
        # Simulate 5 classic games
        classic_wins = 0
        print(f"\n--- Starting Classic Games ---")
        for i in range(num_games):
            print(f"\n--- Classic Game {i + 1} ---")
            if run_classic_game_with_visualization(9, 9, 20, 200):
                classic_wins += 1

        classic_win_rate = classic_wins / num_games
        print(f"\nClassic Win Rate: {classic_win_rate:.2%}")

        # Simulate 5 AI games
        ai_wins = 0
        print(f"\n--- Starting AI Games ---")
        for i in range(num_games):
            print(f"\n--- AI Game {i + 1} ---")
            if run_ai_game_with_visualization(9, 9, 20, 200, learning_mgr, game_key, game_id=i + 1):
                ai_wins += 1

        ai_win_rate = ai_wins / num_games
        max_ai_win_rate = max(max_ai_win_rate, ai_win_rate)
        print(f"\nAI Win Rate: {ai_win_rate:.2%}")

        # Update maximum win rate and save GR metrics
        if ai_win_rate > max_ai_win_rate:
            max_ai_win_rate = ai_win_rate
            best_batch_id = batch_count

            # Consolidate GR metrics for this batch
            gr_files = [f"gr_metrics_game_{batch_count * num_games + i + 1}.csv" for i in range(num_games)]
            gr_data = pd.concat([pd.read_csv(file) for file in gr_files])
            gr_data.to_csv("gr_metrics_max_batch.csv", index=False)

        # Check AI win rate threshold
        if ai_win_rate >= threshold:
            print("\nAI Win Rate threshold of 50% achieved! Stopping simulation.")
            print(f"\nClassic Wins: {classic_wins}/{num_games}")
            print(f"AI Wins: {ai_wins}/{num_games}")
            print(f"\nAI Win Rate threshold of {threshold*100}% achieved in Batch {batch_count}! Stopping simulation.")

            break
    print(f"\nMaximum AI Win Rate Achieved: {max_ai_win_rate:.2%}")
    if batch_count == max_batches:
        print(f"\nReached maximum batch limit {max_batches} without consistently achieving : {threshold*100}% AI Win Rate.")


# Revert stdout to default (console)
sys.stdout.close()
sys.stdout = sys.__stdout__
