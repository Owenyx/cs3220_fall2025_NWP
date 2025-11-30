from src.gameClass import Game
from src.board5MiseryClass import Board5Misery

class FiveMisery(Game):

    def __init__(self):
        self.initial = Board5Misery(to_move='X')

    def actions(self, board):
        '''Legal moves are counting up by 1, 2, or 3'''
        return [1, 2, 3]

    def result(self, board, count):
        """Increment the board counter by count, which is 1-3"""
        player = board.to_move
        board = board.new('O' if player == 'X' else 'X', count)
        game_over = board.counter >= 5
        # If the player was X and reached 5, then -1 utility, else +1
        board.utility = (0 if not game_over else -1 if player == 'X' else +1)
        return board

    def utility(self, board, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return board.utility if player == 'X' else -board.utility

    def is_terminal(self, board):
        """A board is a terminal state if it is won by a player"""
        return board.utility != 0

    def display(self, board): print(board)     