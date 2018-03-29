from collections import defaultdict, deque
from itertools import product

import random

class MinesweeperSolver:

    def __init__(self, game, verbose=False):
        self.game = game
        self.verbose = verbose
        
        self.rows = game.rows
        self.columns = game.columns
        self.mines_remaining = game.mines
        self.num_cells_revealed = 0
        
        self.reveal_queue = deque()
        self.update_queue = deque()
        # a dictionary that contains probabilities of cells being mined
        self.probability = \
            defaultdict(lambda: game.mines / (game.rows * game.columns))

    #Should be called when no cells are available to be revealed or updated
    #Decides what cell should be revealed and reveals it
    def guess(self):
        pass

    #Reveals a randomly chosen cell
    def random(self):
        # do...while
        while True:
            row = random.randrange(self.rows)
            col = random.randrange(self.columns)
            status = self.game.status(row, col)
            if status == 'unrevealed':
                break

        cell = (row, col)
        if self.verbose:
            print('random({})'.format(cell))
        self.reveal(cell)

    #Returns the neighborhood of the given cell
    def neighborhood(self, cell):
        pass

    #Reveals a cell and does associated processing
    def reveal(self, cell):
        pass

    #Main solving loop
    def solve(self):
        steps = 0
        while not self.game.game_over():
            steps += 1
            if self.reveal_queue:
                self.reveal(self.reveal_queue.pop())
            elif self.update_queue:
                self.update(self.update_queue.pop())
            else:
                self.guess()
        print('Terminated after', steps, 'steps')
        if self.game.result[0]:
            print('Victory!')
        else:
            print('You detonated a mine at', self.game.result[1])
        self.game.print()

    # Updates cell and does associated processing
    def update(self, cell):
        pass
            
