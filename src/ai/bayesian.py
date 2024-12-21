# src/ai/bayesian.py
import itertools

class BayesianAnalyzer:
    def __init__(self):
        pass

    def compute_probabilities(self, board):
        # Return a dict: {(x, y): probability_of_mine}
        unrevealed_cells = board.get_unrevealed_cells()
        if not unrevealed_cells:
            return {}

        # 1. Collect constraints from revealed clues:
        constraints = []
        for y in range(board.height):
            for x in range(board.width):
                cell = board.grid[y][x]
                if cell.revealed and not cell.has_mine:
                    clue = cell.neighbor_mines
                    neighbors = board.get_neighbors(x, y)
                    flagged_count = sum(1 for n in neighbors if n.flagged)
                    unrevealed_unflagged = [n for n in neighbors if not n.revealed and not n.flagged]
                    mines_needed = clue - flagged_count
                    if mines_needed < 0:
                        # Contradiction: too many flags => can skip or handle
                        continue
                    if mines_needed > len(unrevealed_unflagged):
                        # Another contradiction => skip or handle
                        continue
                    if unrevealed_unflagged:
                        constraints.append((unrevealed_unflagged, mines_needed))

        if not constraints:
            # No constraints => uniform probability fallback
            total_mines = board.mines
            flagged_mines = sum(1 for row in board.grid for c in row if c.flagged)
            remaining_mines = total_mines - flagged_mines
            base_prob = remaining_mines / float(len(unrevealed_cells)) if len(unrevealed_cells) else 0.0
            return {(c.x, c.y): base_prob for c in unrevealed_cells}

        # 2. Build a set of all relevant unrevealed cells from constraints
        relevant_cells = set()
        for (neighbors, _) in constraints:
            for n in neighbors:
                relevant_cells.add((n.x, n.y))

        # For cells not in constraints, fallback to uniform
        fallback_prob_cells = [(c.x, c.y) for c in unrevealed_cells if (c.x, c.y) not in relevant_cells]

        # 3. Enumerate possible ways to assign mines to these relevant cells consistent with constraints
        relevant_list = list(relevant_cells)
        # If it's huge, enumeration can be slow, but on a small board it's feasible
        assignments = []
        flagged_mines = sum(1 for row in board.grid for c in row if c.flagged)
        total_mines_left = board.mines - flagged_mines
        # We can try all subsets of relevant_list of size up to total_mines_left.
        # But for demonstration, let's just generate all subsets of relevant_list.

        valid_assignments = []
        for subset_size in range(0, len(relevant_list) + 1):
            if subset_size > total_mines_left:
                break  # no need to look for subsets bigger than available mines
            for combo in itertools.combinations(relevant_list, subset_size):
                # combo is a set of cells that have mines
                # check constraints
                if self._check_constraints(constraints, combo):
                    valid_assignments.append(combo)

        if not valid_assignments:
            # Contradictory or no solution => fallback to uniform
            total_mines = board.mines
            flagged_mines = sum(1 for row in board.grid for c in row if c.flagged)
            remaining_mines = total_mines - flagged_mines
            base_prob = remaining_mines / float(len(unrevealed_cells)) if len(unrevealed_cells) else 0.0
            prob_dict = {(c.x, c.y): base_prob for c in unrevealed_cells}
            return prob_dict

        # 4. For each cell, count in how many valid assignments it is a mine
        cell_mine_count = {rc: 0 for rc in relevant_list}
        for assignment in valid_assignments:
            for rc in assignment:
                cell_mine_count[rc] += 1

        # Probability = (#assignments with cell as mine) / (total valid assignments)
        prob_dict = {}
        total_valid = len(valid_assignments)
        for rc in relevant_list:
            p = cell_mine_count[rc] / float(total_valid)
            prob_dict[rc] = p

        # For fallback cells, just assume uniform
        if fallback_prob_cells:
            uniform_prob = (board.mines - flagged_mines) / float(len(unrevealed_cells))
            for fc in fallback_prob_cells:
                prob_dict[fc] = max(0.0, min(1.0, uniform_prob))

        return prob_dict

    def _check_constraints(self, constraints, combo):
        # combo is a set of (x, y) that have mines
        # For each constraint (neighbors, mines_needed):
        # we check how many of these neighbors are in combo
        for (neighbors, mines_needed) in constraints:
            count_mines = 0
            for n in neighbors:
                if (n.x, n.y) in combo:
                    count_mines += 1
            if count_mines != mines_needed:
                return False
        return True
