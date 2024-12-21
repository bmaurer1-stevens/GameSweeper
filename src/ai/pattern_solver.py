# src/ai/pattern_solver.py
class PatternSolver:
    def __init__(self):
        # Keep track of repeated forced moves so we don't loop infinitely
        self.forced_history = set()

    def find_forced_moves(self, board):
        forced_moves = []
        # Check standard forced moves first: if clue - flagged = unrevealed => all must be mines, etc.
        self._find_standard_forced(board, forced_moves)
        # Then advanced patterns (1-2 pattern for example):
        self._find_1_2_pattern(board, forced_moves)

        # Filter out repeated moves to avoid toggling flags in a loop
        unique_moves = []
        for move in forced_moves:
            # move = ("flag" or "reveal", x, y)
            if (move, self._board_hash(board)) not in self.forced_history:
                unique_moves.append(move)
                self.forced_history.add((move, self._board_hash(board)))

        return unique_moves

    def _find_standard_forced(self, board, forced_moves):
        for y in range(board.height):
            for x in range(board.width):
                cell = board.grid[y][x]
                if cell.revealed and not cell.has_mine:
                    clue = cell.neighbor_mines
                    neighbors = board.get_neighbors(x, y)
                    flagged = [n for n in neighbors if n.flagged]
                    unrevealed = [n for n in neighbors if not n.revealed and not n.flagged]
                    if len(unrevealed) == clue - len(flagged) and len(unrevealed) > 0:
                        # All unrevealed must be flagged
                        for n in unrevealed:
                            forced_moves.append(("flag", n.x, n.y))
                    elif (clue - len(flagged)) == 0 and len(unrevealed) > 0:
                        # All unrevealed are safe => reveal them
                        for n in unrevealed:
                            forced_moves.append(("reveal", n.x, n.y))

    def _find_1_2_pattern(self, board, forced_moves):
        """
        A simple example of a known 1-2 pattern:
          - If we see a pattern of adjacent revealed cells with clues 1 and 2, 
            and there's some shared unrevealed neighbors arrangement, we can deduce certain flags.
        This is just a demonstration, real Minesweeper has many patterns.
        """
        # Pseudocode approach:
        # 1. Find revealed cells with clue 1 next to revealed cells with clue 2.
        # 2. Check their neighbors for overlapping unrevealed sets.
        # 3. If the pattern matches (like the 1's neighbor set is a subset, etc.), apply forced logic.
        pass  # Implementation left as an exercise—this can get quite detailed.

    def _board_hash(self, board):
        # Simple approach: hash positions of flagged cells + revealed cells
        # This helps us identify if we're in the same state
        flagged_positions = []
        revealed_positions = []
        for y in range(board.height):
            for x in range(board.width):
                c = board.grid[y][x]
                if c.flagged:
                    flagged_positions.append((x, y))
                if c.revealed:
                    revealed_positions.append((x, y))
        # Return a frozenset or string that represents the combination
        return (frozenset(flagged_positions), frozenset(revealed_positions))
