import math
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus, LpContinuous

class BayesianAnalyzer:
    def __init__(self):
        pass

    def compute_probabilities(self, board):
        unrevealed_cells = board.get_unrevealed_cells()
        if not unrevealed_cells:
            return {}

        constraints = []
        revealed_clue_cells = []
        for y in range(board.height):
            for x in range(board.width):
                cell = board.grid[y][x]
                if cell.revealed and not cell.has_mine:
                    clue = cell.neighbor_mines
                    unrevealed_neighbors = [c for c in board.get_neighbors(x, y) 
                                            if not c.revealed and not c.flagged]
                    if unrevealed_neighbors:
                        constraints.append((unrevealed_neighbors, clue))
                        revealed_clue_cells.append(cell)

        if not constraints:
            # No constraints, fallback to uniform probability
            total_mines = board.mines
            flagged_mines = sum(1 for row in board.grid for c in row if c.flagged)
            remaining_mines = total_mines - flagged_mines
            remaining_cells = len(unrevealed_cells)
            base_prob = remaining_mines / remaining_cells if remaining_cells > 0 else 0.0
            return {(c.x, c.y): base_prob for c in unrevealed_cells}

        total_mines = board.mines
        flagged_mines = sum(c.flagged for row in board.grid for c in row)
        remaining_mines = total_mines - flagged_mines

        cell_to_idx = {(c.x, c.y): i for i, c in enumerate(unrevealed_cells)}
        idx_to_cell = {i: c for i, c in enumerate(unrevealed_cells)}

        # Setup LP problem
        # We'll allow fractional solutions to get probabilities as a relaxation
        prob = LpProblem("Minesweeper_Prob", LpMinimize)

        vars = [LpVariable(f"cell_{i}", lowBound=0, upBound=1, cat=LpContinuous) 
                for i in range(len(unrevealed_cells))]

        # Each constraint: sum of variables for that constraint = clue
        for (neighbors, clue) in constraints:
            prob += lpSum([vars[cell_to_idx[(n.x, n.y)]] for n in neighbors]) == clue

        # Global constraint: sum of all variables = remaining_mines
        prob += lpSum(vars) == remaining_mines

        # Objective: Minimize sum of vars (arbitrary - we just need a feasible solution)
        prob.setObjective(lpSum([0*var for var in vars]))

        status = prob.solve()

        if LpStatus[status] != "Optimal":
            # Infeasible or no solution, fallback to uniform
            base_prob = remaining_mines / len(unrevealed_cells) if unrevealed_cells else 0
            return {(c.x, c.y): base_prob for c in unrevealed_cells}

        # If optimal, use the fractional values as probabilities
        probabilities = {}
        for i, c in idx_to_cell.items():
            p = vars[i].varValue
            probabilities[(c.x, c.y)] = p

        return probabilities
