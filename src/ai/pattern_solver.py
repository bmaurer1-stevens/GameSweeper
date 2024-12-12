class PatternSolver:
    @staticmethod
    def find_forced_moves(board):
        """
        Scan the board for patterns that yield guaranteed safe or guaranteed mine moves.
        Returns:
           forced_moves (list): A list of moves like ("flag", x, y) or ("reveal", x, y) that are guaranteed.
        """
        forced_moves = []
        for y in range(board.height):
            for x in range(board.width):
                cell = board.grid[y][x]
                if cell.revealed and not cell.has_mine:
                    clue = cell.neighbor_mines
                    neighbors = board.get_neighbors(x, y)
                    unrevealed = [n for n in neighbors if not n.revealed and not n.flagged]
                    flagged = [n for n in neighbors if n.flagged]

                    # Number of mines still needed around this clue
                    mines_needed = clue - len(flagged)

                    if mines_needed == len(unrevealed) and len(unrevealed) > 0:
                        # All unrevealed neighbors must be mines
                        for n in unrevealed:
                            # If not already flagged, flag them
                            if not n.flagged:
                                forced_moves.append(("flag", n.x, n.y))

                    elif mines_needed == 0 and len(unrevealed) > 0:
                        # All unrevealed neighbors must be safe
                        for n in unrevealed:
                            forced_moves.append(("reveal", n.x, n.y))

        return forced_moves
