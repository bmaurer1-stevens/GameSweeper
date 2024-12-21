import random
from src.game.board import Board
from src.game.game_manager import GameManager
from src.ai.bayesian import BayesianAnalyzer
from src.ai.mdp import MDP
from src.ai.pattern_solver import PatternSolver
from src.ai.learning_manager import LearningManager
from src.metrics.dynamic_gr import DynamicGR
from src.utils.logger import CSVLogger  # Import the CSVLogger
import os


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
                action = guess_safest_cell(board, bayes)
                if not action:
                    break
                act_type, x, y = action
                gm.make_move(x, y, act_type)

        step += 1

    outcome = "win" if gm.is_victory() else "lose"
    print(f"\nGame Over: {outcome}\n")
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
    print(f"\nGame Over: {outcome}\n")
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

    num_games = 10  # Total number of games to simulate
    learning_mgr = LearningManager("experience_data.json")
    game_key = "5x5_5mines"

    ai_wins = 0
    classic_wins = 0

    print("\n--- Starting Classic Games ---")
    for i in range(num_games // 2):
        print(f"\n--- Classic Game {i + 1} ---\n")
        result = run_classic_game_with_visualization(5, 5, 5, 50)
        if result:
            classic_wins += 1

    print("\n--- Starting AI Games ---")
    for i in range(num_games // 2):
        print(f"\n--- AI Game {i + 1} ---\n")
        result = run_ai_game_with_visualization(5, 5, 5, 50, learning_mgr, game_key, game_id=i + 1)
        if result:
            ai_wins += 1

    print(f"\nClassic Wins: {classic_wins}/{num_games // 2}")
    print(f"AI Wins: {ai_wins}/{num_games // 2}")
