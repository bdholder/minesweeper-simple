import random


class Cell:

    sym_flagged = '!'
    sym_mined = '*'
    sym_unrevealed = '-'
    sym_zero = ' '
    
    def __init__(self, adjacent_mines=None):
        self.adjacent_mines = adjacent_mines
        self.flagged = False
        self.mined = False
        self.revealed = False

    def __str__(self):
        status = self.status()
        if status == 'flagged':
            return Cell.sym_flagged
        elif status == 'unrevealed':
            return Cell.sym_unrevealed
        elif status == 'mine':
            return Cell.sym_mined
        elif status == 0:
            return Cell.sym_zero
        else:
            return str(status)
    
    def status(self):
        if self.flagged:
            return 'flagged'
        elif not self.revealed:
            return 'unrevealed'
        elif self.mined:
            return 'mine'
        else:
            return self.adjacent_mines


class Minesweeper:
    
    DUMMY_CELL = Cell()
  
    def __init__(self, rows, columns, mines):
        """Creates a new instance of a Minesweeper game.

        Args:
            rows: the number of rows in the board
            columns: the number of columns in the board
            mines: the number of mines in the board
        """
        # TODO: remove assertion
        assert rows > 0 and columns > 0
        assert mines > 0 and mines < rows * columns
        
        self._initialized = False
        self.flags_placed = 0
        self.mines_flagged = 0
        self.result = None
        
        self.rows = rows
        self.columns = columns
        self.mines = mines
        
        self.board = [[Cell() for _ in range(columns)] for _ in range(rows)]

    def __getitem__(self, coordinates):
        r, c = coordinates
        if not (0 <= r < self.rows and 0 <= c < self.columns):
            return Minesweeper.DUMMY_CELL
        else:
            assert 0 <= r < self.rows
            assert 0 <= c < self.columns
            return self.board[r][c]

    def __setitem__(self, coordinates, value):
        r, c = coordinates
        self._test_bounds(r, c)
        self.board[r][c] = value

    def clear_flag(self, r, c):
        self._test_bounds(r, c)
        cell = self[r, c]
        cell.flagged = False
        if cell.mined:
            self.mines_flagged -= 1

    def _count_adjacent_mines(self, r, c):
        adjacent_mines = 0
        for i in (r - 1, r, r + 1):
            cols = (c - 1, c + 1) if i == r else (c - 1, c, c + 1)
            for j in cols:
                if self[i, j].mined:
                    adjacent_mines += 1
        return adjacent_mines
                
    def flag(self, r, c):
        """Flags the cell as being a mine.

        Args:
            r: row of cell
            c: column of cell

        Raises:
            IndexError: if r or c are out of bounds
        """
        self._test_bounds(r, c)
        cell = self[r, c]
        if cell.flagged:
            return
        
        self.flags_placed += 1
        cell.flagged = True
        
        if cell.mined:
            self.mines_flagged += 1
            if self.mines_flagged == self.mines:
                self.result = (True, None)

    def game_over(self) -> bool:
        return self.result is not None
        
    def _initialize_board(self, restricted_squares=frozenset()):
        self._place_mines(restricted_squares)
        self._mark_adjacent_mines()
        self._initialized = True
        
    def _mark_adjacent_mines(self):
        for r in range(self.rows):
            for c in range(self.columns):
                self[r, c].adjacent_mines = self._count_adjacent_mines(r, c)

    def _place_mines(self, restricted_squares):
        mines_remaining = self.mines
        while mines_remaining:
            r = random.randrange(self.rows)
            c = random.randrange(self.columns)
            cell = self[r, c]
            if not (cell.mined or (r, c) in restricted_squares):
                cell.mined = True
                mines_remaining -= 1

    #TODO: fix this trash
    def print(self, debug=False):
        """Prints a representation of the game board on the screen.

        Args:
            debug: prints the actual state of the game board if True
        """
        for r in range(self.rows):
            if debug:
                row = list()
                for c in range(self.columns):
                    cell = self[r, c]
                    if cell.mined:
                        sym = Cell.sym_mined
                    elif cell.adjacent_mines == 0:
                        sym = Cell.sym_zero
                    else:
                        sym = str(cell.adjacent_mines)
                    row.append(sym)
            else:
                row = (str(self[r, c]) for c in range(self.columns))
            
            print(''.join(row))
            
    def reveal(self, r, c) -> int:
        """Reveals the contents of a cell.
        
        Equivalent to clicking on a cell in GUI Minesweeper. The first call to
        reveal is guaranteed to not be a mine. If the revealed cell is not a
        mine, the number of adjacent mines is returned. If the cell is a mine,
        then -1 is returned, and the game is over.
        
        Args:
            r: row of cell
            c: column of cell
        
        Returns:
            The number of adjacent mines if cell is not a mine, and -1
            otherwise.
        
        Raises:
            IndexError: if r or c are out of bounds.
        """
        self._test_bounds(r, c)
        
        if not self._initialized:
            self._initialize_board({(r, c)})
        
        cell = self[r, c]
        cell.revealed = True
        if cell.mined:
            self.result = (False, (r, c))
            return -1

        return cell.adjacent_mines

    def status(self, r, c):
        """Returns the status of a cell.

        The status of a cell is 'flagged' if the cell has been flagged as a
        mine, 'unrevealed' if the cell is not flagged and not revealed, 'mine'
        if the cell has been revealed as is a mine, and an int with the number
        of adjacent cells that are mined otherwise.

        Args:
            r: row of cell
            c: column of cell

        Returns:
            The status as described above.

        Raises:
            IndexError: if r or c are out of bounds
        """
        self._test_bounds(r, c)
        return self[r, c].status()

    def _test_bounds(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.columns):
            raise IndexError
