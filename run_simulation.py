from src.game.board import Board
from src.game.game_manager import GameManager
from src.ai.bayesian import BayesianAnalyzer
from src.ai.mdp import MDP
from src.ai.pattern_solver import PatternSolver
from src.metrics.dynamic_gr import DynamicGR
import random

def run_classic_game(width=5, height=5, mines=5, max_steps=50):
    """A simple 'classic' (human-like) random approach on a 5x5 board with 5 mines."""
    board = Board(width, height, mines)
    gm = GameManager(board)
    step = 0

    while not gm.is_over() and step < max_steps:
        unrevealed = board.get_unrevealed_cells()
        if not unrevealed:
            break

        # Pick a random cell to reveal
        cell = random.choice(unrevealed)
        gm.make_move(cell.x, cell.y, "reveal")

        # Print board after the move
        print(f"\n[Classic] After step {step}:")
        print(board)
        print("-------------------------------------")
        
        step += 1

    return gm.is_victory()

def run_ai_game(width=5, height=5, mines=5, max_steps=50):
    """An AI-based approach (Bayesian + MDP + pattern solver) on a 5x5 board with 5 mines."""
    board = Board(width, height, mines)
    gm = GameManager(board)
    bayes = BayesianAnalyzer()
    gr = DynamicGR()
    pattern_solver = PatternSolver()
    step = 0

    # Make an initial reveal in the center if desired
    start_x, start_y = width // 2, height // 2
    gm.make_move(start_x, start_y, "reveal")
    print("\n[AI] Initial Board after first reveal:")
    print(board)
    print("-------------------------------------")

    while not gm.is_over() and step < max_steps:
        forced_moves = pattern_solver.find_forced_moves(board)

        if forced_moves:
            # Make all forced moves
            for move in forced_moves:
                act_type, x, y = move
                gm.make_move(x, y, act_type)

                # Print board state
                print(f"\n[AI] After forced move {step}: {move}")
                print(board)
                print("-------------------------------------")

                if gm.is_over():
                    break
        else:
            # Use Bayesian + MDP to choose the best action
            probabilities = bayes.compute_probabilities(board)
            mdp = MDP(board, probabilities, depth=3)
            action = mdp.find_best_action()

            if action is None:
                # No meaningful action found
                break

            act_type, x, y = action
            gm.make_move(x, y, act_type)

            # Print board state
            print(f"\n[AI] After step {step}: {action}")
            print(board)
            print("-------------------------------------")

        step += 1

    return gm.is_victory()

if __name__ == "__main__":
    num_games = 2  # Run fewer games for demonstration
    print("Starting simulation on a 5x5 board with 5 mines...")
    print(f"Running {num_games} classic approach games and {num_games} AI approach games.\n")

    classic_wins = 0
    ai_wins = 0

    # Run classic games
    for i in range(num_games):
        print(f"=== Classic Game {i+1}/{num_games} ===")
        result = run_classic_game()
        if result:
            classic_wins += 1
            print(f"\nClassic Game {i+1} Result: Win")
        else:
            print(f"\nClassic Game {i+1} Result: Lose")
        print("=====================================\n")

    # Run AI games
    for i in range(num_games):
        print(f"=== AI Game {i+1}/{num_games} ===")
        result = run_ai_game()
        if result:
            ai_wins += 1
            print(f"\nAI Game {i+1} Result: Win")
        else:
            print(f"\nAI Game {i+1} Result: Lose")
        print("=====================================\n")

    # Final results
    print("All simulations completed.")
    print(f"Classic Approach Win Rate: {classic_wins}/{num_games} = {(classic_wins/num_games)*100:.2f}%")
    print(f"AI Approach Win Rate: {ai_wins}/{num_games} = {(ai_wins/num_games)*100:.2f}%")
