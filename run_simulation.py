from src.game.board import Board
from src.game.game_manager import GameManager
from src.ai.bayesian import BayesianAnalyzer
from src.ai.mdp import MDP
from src.ai.pattern_solver import PatternSolver
from src.metrics.dynamic_gr import DynamicGR
import random

def run_classic_game(width=9, height=9, mines=10, max_steps=200):
    board = Board(width, height, mines)
    gm = GameManager(board)
    step = 0
    while not gm.is_over() and step < max_steps:
        unrevealed = board.get_unrevealed_cells()
        if not unrevealed:
            break
        cell = random.choice(unrevealed)
        gm.make_move(cell.x, cell.y, "reveal")
        step += 1
    return gm.is_victory()

def run_ai_game(width=9, height=9, mines=10, max_steps=200):
    board = Board(width, height, mines)
    gm = GameManager(board)
    bayes = BayesianAnalyzer()
    gr = DynamicGR()
    pattern_solver = PatternSolver()
    step = 0

    # Initial safe move
    gm.make_move(width//2, height//2, "reveal")

    while not gm.is_over() and step < max_steps:
        forced_moves = pattern_solver.find_forced_moves(board)
        if forced_moves:
            for move in forced_moves:
                act_type, x, y = move
                gm.make_move(x, y, act_type)
                if gm.is_over():
                    break
        else:
            probabilities = bayes.compute_probabilities(board)
            mdp = MDP(board, probabilities, depth=3)
            action = mdp.find_best_action()
            if action is None:
                break
            act_type, x, y = action
            gm.make_move(x, y, act_type)
        step += 1

    return gm.is_victory()

if __name__ == "__main__":
    num_games = 20
    print("Starting simulation...")
    print(f"Running {num_games} classic approach games and {num_games} AI approach games.")

    classic_wins = 0
    ai_wins = 0

    # Run classic games
    for i in range(num_games):
        print(f"Running classic game {i+1}/{num_games}...", end='')
        result = run_classic_game()
        if result:
            classic_wins += 1
            print(" Won")
        else:
            print(" Lost")
        
        # Print intermediate results
        if (i+1) % 5 == 0:
            print(f"Classic approach intermediate results: {classic_wins}/{i+1} = {(classic_wins/(i+1))*100:.2f}%")

    # Run AI games
    for i in range(num_games):
        print(f"Running AI game {i+1}/{num_games}...", end='')
        result = run_ai_game()
        if result:
            ai_wins += 1
            print(" Won")
        else:
            print(" Lost")
        
        # Print intermediate results
        if (i+1) % 5 == 0:
            print(f"AI approach intermediate results: {ai_wins}/{i+1} = {(ai_wins/(i+1))*100:.2f}%")

    # Final results
    print("All simulations completed.")
    print(f"Classic Approach Win Rate: {classic_wins}/{num_games} = {(classic_wins/num_games)*100:.2f}%")
    print(f"AI Approach Win Rate: {ai_wins}/{num_games} = {(ai_wins/num_games)*100:.2f}%")