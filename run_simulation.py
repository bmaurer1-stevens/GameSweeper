# run_simulation.py
import random
from src.game.board import Board
from src.game.game_manager import GameManager
from src.ai.bayesian import BayesianAnalyzer
from src.ai.mdp import MDP
from src.ai.pattern_solver import PatternSolver
from src.metrics.dynamic_gr import DynamicGR

def run_ai_game(width=5, height=5, mines=5, max_steps=50):
    board = Board(width, height, mines)
    gm = GameManager(board)
    bayes = BayesianAnalyzer()
    gr = DynamicGR()
    pattern_solver = PatternSolver()

    # optional first reveal
    gm.make_move(width//2, height//2, "reveal")
    step = 0
    last_forced_move_count = -1

    while not gm.is_over() and step < max_steps:
        # 1. Pattern-based forced moves
        forced_moves = pattern_solver.find_forced_moves(board)
        if forced_moves:
            # If we keep generating forced moves but remain stuck, break
            if last_forced_move_count == len(forced_moves):
                # Possibly guess a low-prob cell to break the loop
                guess = guess_safest_cell(board, bayes)
                if guess:
                    gm.make_move(guess[0], guess[1], "reveal")
                else:
                    break
            else:
                last_forced_move_count = len(forced_moves)

            for move in forced_moves:
                act_type, x, y = move
                gm.make_move(x, y, act_type)
                if gm.is_over():
                    break
        else:
            # 2. Bayesian probability & MDP
            probs = bayes.compute_probabilities(board)
            mdp = MDP(board, probs, depth=3)
            action = mdp.find_best_action()

            if action is None:
                # 3. fallback guess if MDP can't find a better move
                guess = guess_safest_cell(board, bayes)
                if guess is not None:
                    gm.make_move(guess[0], guess[1], "reveal")
                else:
                    break
            else:
                gm.make_move(action[1], action[2], action[0])

        step += 1

    return gm.is_victory()

def guess_safest_cell(board, bayes):
    # pick the cell with the lowest probability of being a mine
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
    return best_cell

def run_classic_game(width=5, height=5, mines=5, max_steps=50):
    # random approach for baseline
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

if __name__ == "__main__":
    num_games = 10
    print("Starting advanced AI approach vs. classic on a 5x5 board with 5 mines...")

    ai_wins = 0
    classic_wins = 0
    for i in range(num_games):
        print(f"\n=== Classic Game {i+1} ===")
        res = run_classic_game()
        if res:
            classic_wins += 1
            print("Classic: Win")
        else:
            print("Classic: Lose")

    for i in range(num_games):
        print(f"\n=== AI Game {i+1} ===")
        res = run_ai_game()
        if res:
            ai_wins += 1
            print("AI: Win")
        else:
            print("AI: Lose")

    print("\nResults:")
    print(f"Classic Wins: {classic_wins}/{num_games} = {(classic_wins/num_games)*100:.2f}%")
    print(f"AI Wins: {ai_wins}/{num_games} = {(ai_wins/num_games)*100:.2f}%")
