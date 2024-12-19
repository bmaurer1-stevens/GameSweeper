class BayesianAnalyzer:
    def __init__(self):
        pass

    def compute_probabilities(self, board):
        unrevealed_cells = board.get_unrevealed_cells()
        if not unrevealed_cells:
            return {}

        # Collect constraints from each revealed cell with a clue
        constraints = []
        cell_probs = {(c.x, c.y): [] for c in unrevealed_cells}

        for y in range(board.height):
            for x in range(board.width):
                cell = board.grid[y][x]
                if cell.revealed and not cell.has_mine:
                    # Clue given by this cell
                    clue = cell.neighbor_mines
                    neighbors = board.get_neighbors(x, y)
                    unrevealed_unflagged = [n for n in neighbors if not n.revealed and not n.flagged]

                    if unrevealed_unflagged:
                        k = len(unrevealed_unflagged)
                        # Base probability per neighbor = clue/k
                        # We will adjust this probability based on how often a cell appears in other constraints.
                        for n in unrevealed_unflagged:
                            cell_probs[(n.x, n.y)].append(clue/k)

        # Combine probabilities for each cell (likelihood density)
        final_prob = {}
        for coord, p_list in cell_probs.items():
            if p_list:
                # Average them or use a different combination strategy
                # e.g., weighted average. For simplicity, take mean.
                mean_p = sum(p_list) / len(p_list)
                final_prob[coord] = max(0.0, min(1.0, mean_p))
            else:
                # No clues mentioning this cell — fallback to global ratio
                total_mines = board.mines
                flagged = sum(1 for row in board.grid for c in row if c.flagged)
                remaining_mines = total_mines - flagged
                remaining_cells = len(unrevealed_cells)
                fallback_p = remaining_mines / remaining_cells if remaining_cells > 0 else 0
                final_prob[coord] = fallback_p

        return final_prob
