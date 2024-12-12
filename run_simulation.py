from src.game.board import Board
from src.game.game_manager import GameManager
from src.ai.bayesian import BayesianAnalyzer
from src.ai.mdp import MDP
from src.metrics.dynamic_gr import DynamicGR
from src.utils.logger import CSVLogger
from src.ai.pattern_solver import PatternSolver

def run_single_game(width=9, height=9, mines=10, max_steps=200):
    board = Board(width, height, mines)
    gm = GameManager(board)
    bayes = BayesianAnalyzer()
    gr = DynamicGR()
    logger = CSVLogger("gr_metrics.csv")

    step = 0

    # Ensure first move is safe: reveal a cell in the middle if possible
    start_x, start_y = width // 2, height // 2
    gm.make_move(start_x, start_y, "reveal")

    while not gm.is_over() and step < max_steps:
        # Try pattern-based logic first:
        forced_moves = PatternSolver.find_forced_moves(board)
        if forced_moves:
            # Execute all forced moves before guessing
            for move in forced_moves:
                act_type, x, y = move
                gm.make_move(x, y, act_type)
                if gm.is_over():
                    break
            if gm.is_over():
                break
        else:
            # No forced moves found, use Bayesian + MDP
            probabilities = bayes.compute_probabilities(board)
            mdp = MDP(board, probabilities, depth=3)  # Increase depth slightly
            action = mdp.find_best_action()

            if action is None:
                # No action found -> might be stuck or no moves left
                break

            act_type, x, y = action
            gm.make_move(x, y, act_type)

        # Update and log GR after moves
        probabilities = bayes.compute_probabilities(board)
        gr_value, gr_data = gr.update(board, step, probabilities)
        logger.log(step, gr_data)

        step += 1

    return gm.is_victory()

if __name__ == "__main__":
    # Run multiple simulations
    num_games = 5
    wins = 0
    for i in range(num_games):
        result = run_single_game(9,9,10)
        if result:
            wins += 1
        print(f"Game {i+1}/{num_games}: {'Win' if result else 'Lose'}")

    print(f"Win rate: {wins}/{num_games}")
