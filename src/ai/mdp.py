# src/ai/mdp.py
import math

class MDP:
    def __init__(self, board, probabilities, depth=2):
        self.board = board
        self.probabilities = probabilities
        self.depth = depth

    def find_best_action(self):
        # 1. Build a list of possible actions
        # 2. Evaluate expected reward
        # 3. Pick the best
        actions = self._list_actions()
        if not actions:
            return None

        best_action = None
        best_value = -9999

        for act in actions:
            exp_value = self._expected_value_of_action(act)
            if exp_value > best_value:
                best_value = exp_value
                best_action = act

        return best_action

    def _list_actions(self):
        # For each unrevealed cell, we can either reveal or flag
        # But typically we prefer reveal if probabilities < 1
        # We'll let forced moves handle near-100% mines. 
        # Here, we just consider reveals for cells with < 1 probability
        # and flags for cells with probability > 0.99, for instance.
        unrevealed = [(c.x, c.y) for row in self.board.grid for c in row if not c.revealed and not c.flagged]
        actions = []
        for x,y in unrevealed:
            p = self.probabilities.get((x, y), 0.5)
            if p < 0.99:
                actions.append(("reveal", x, y))
            else:
                actions.append(("flag", x, y))
        return actions

    def _expected_value_of_action(self, action):
        # simple approach:
        # "reveal": reward = (1 - pMine)*[1 + info_gain_bonus] + pMine*(-10)
        # "flag": reward = 0. (or slight negative if you want to discourage pointless flags)
        act_type, x, y = action
        p_mine = self.probabilities.get((x, y), 0.5)
        if act_type == "reveal":
            # approximate info gain bonus: if p_mine < 0.5, assume revealing yields decent new clues
            info_gain = 0.2 if p_mine < 0.5 else 0.0
            return (1 - p_mine)*(1 + info_gain) + p_mine*(-10)
        else:  # flag
            # If we strongly believe it's a mine, we get a small reward for correct flag
            # but let's keep it neutral for now.
            return 0.0
