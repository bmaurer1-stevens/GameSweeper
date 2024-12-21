# src/game/board.py
import random
from .cell import Cell

class Board:
    def __init__(self, width=5, height=5, mines=5):
        self.width = width
        self.height = height
        self.mines = mines
        self.grid = []
        self.game_over = False
        self._initialize_board()

    def _initialize_board(self):
        cells = [Cell(x, y) for y in range(self.height) for x in range(self.width)]
        mine_positions = random.sample(cells, self.mines)
        for c in mine_positions:
            c.has_mine = True

        self.grid = [cells[i*self.width:(i+1)*self.width] for i in range(self.height)]
        # Calculate neighbor mine counts
        for row in self.grid:
            for c in row:
                if not c.has_mine:
                    c.neighbor_mines = self.count_neighbor_mines(c.x, c.y)

    def count_neighbor_mines(self, x, y):
        return sum(1 for n in self.get_neighbors(x, y) if n.has_mine)

    def get_neighbors(self, x, y):
        neighbors = []
        for nx in [x-1, x, x+1]:
            for ny in [y-1, y, y+1]:
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not (nx == x and ny == y):
                        neighbors.append(self.grid[ny][nx])
        return neighbors

    def reveal_cell(self, x, y):
        cell = self.grid[y][x]
        if cell.flagged or cell.revealed:
            return
        cell.revealed = True
        if cell.has_mine:
            self.game_over = True
            return
        if cell.neighbor_mines == 0:
            # Flood fill for zero neighbors
            for n in self.get_neighbors(x, y):
                if not n.revealed and not n.flagged:
                    self.reveal_cell(n.x, n.y)

    def flag_cell(self, x, y):
        cell = self.grid[y][x]
        if not cell.revealed:
            cell.flagged = not cell.flagged

    def is_victory(self):
        # All non-mine cells must be revealed
        for row in self.grid:
            for c in row:
                if not c.has_mine and not c.revealed:
                    return False
        return True

    def get_unrevealed_cells(self):
        return [c for row in self.grid for c in row if not c.revealed and not c.flagged]

    def __str__(self):
        rows = []
        for row in self.grid:
            rows.append(' '.join(str(c) for c in row))
        return '\n'.join(rows)
