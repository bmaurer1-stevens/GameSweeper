# run_simulation.py

import random
from src.game.board import Board
from src.game.game_manager import GameManager
from src.ai.bayesian import BayesianAnalyzer
from src.ai.mdp import MDP
from src.ai.pattern_solver import PatternSolver
from src.ai.learning_manager import LearningManager
from src.metrics.dynamic_gr import DynamicGR

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

def run_ai_game(width=5, height=5, mines=5, max_steps=50, learning_mgr=None, game_key="5x5_5mines"):
    """
    AI approach with partial 'learning' from previous runs.
    """
    board = Board(width, height, mines)
    gm = GameManager(board)
    bayes = BayesianAnalyzer()
    gr = DynamicGR()
    pattern_solver = PatternSolver()

    gm.make_move(width//2, height//2, "reveal")  # optional first reveal in center

    step = 0
    step_records = []  # to store (state_hash, action) for each step

    while not gm.is_over() and step < max_steps:
        # Build a state hash for learning
        st_hash = board_state_hash(board)

        # 1. Check if we have a 'best action' from previous experience
        best_act_from_history = None
        if learning_mgr:
            best_act_from_history = learning_mgr.best_action_for_state(game_key, st_hash)

        if best_act_from_history:
            # If we have a historically good action, do that
            act_type, x, y = best_act_from_history
            gm.make_move(x, y, act_type)
            step_records.append((st_hash, best_act_from_history))
        else:
            # No historical data => proceed with pattern / MDP approach
            forced_moves = pattern_solver.find_forced_moves(board)
            if forced_moves:
                # Just pick the first forced move for simplicity
                fm = forced_moves[0]
                gm.make_move(fm[1], fm[2], fm[0])
                step_records.append((st_hash, fm))
            else:
                probs = bayes.compute_probabilities(board)
                mdp = MDP(board, probs, depth=3)
                action = mdp.find_best_action()
                if action is None:
                    # fallback: random reveal or guess the safest cell
                    action = guess_safest_cell(board, bayes)
                    if not action:
                        break
                    act_type, x, y = action
                    gm.make_move(x, y, act_type)
                    step_records.append((st_hash, action))
                else:
                    gm.make_move(action[1], action[2], action[0])
                    step_records.append((st_hash, action))

        step += 1

    # Record outcome for learning
    outcome = "win" if gm.is_victory() else "lose"
    if learning_mgr:
        learning_mgr.record_game(game_key, step_records, outcome)

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
    # Return an action in the same format: ("reveal", x, y)
    return ("reveal", best_cell[0], best_cell[1])

def run_classic_game(width=5, height=5, mines=5, max_steps=50):
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
    from src.ai.learning_manager import LearningManager

    num_games = 20
    learning_mgr = LearningManager("experience_data.json")
    game_key = "5x5_5mines"

    classic_wins = 0
    ai_wins = 0

    print("Starting simulation with Learning Manager...")

    # Run some classic games for baseline
    for i in range(num_games // 2):
        res = run_classic_game()
        if res:
            classic_wins += 1

    # Run some AI games that store data and (re)use experience_data.json
    for i in range(num_games // 2):
        res = run_ai_game(5, 5, 5, 50, learning_mgr, game_key)
        if res:
            ai_wins += 1

    print(f"Classic Approach Wins: {classic_wins}/{num_games//2}")
    print(f"AI Approach Wins: {ai_wins}/{num_games//2}")

    # Save experiences to file for future runs
    learning_mgr.save_experience()
    print("Experience data saved.")
