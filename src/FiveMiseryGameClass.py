from src.gameClass import Game
from src.board5MiseryClass import Board5Misery

class FiveMisery(Game):
    """
    The game “5 Misery” is 2-player version of 21 game.
    Players take turns increasing a counter. 
    The counter starts at 1 and each player in turn increases the counter by 1, 2, or 3, 
    but may not exceed 5.
    The player who says “5” or larger loses.
    'X' plays first against 'O'.
    """
    

    def __init__(self):
        #self.squares = {(x, y) for x in range(width) for y in range(height)} # set
        self.counter=1
        self.initial = Board5Misery(counter=self.counter, to_move='X', utility=0)
  

    def actions(self, state):
        """actions(s) = {1, 2, 3} - each player in turn increases the counter by 1, 2, or 3"""
        return {1,2,3}

    def result(self, state, act):
        """Place a marker for current player on square."""
        player = state.to_move
        print(f"The current Player is {player}")
        self.counter+=act
        if player == 'X':
            to_move='O'
        else:
            to_move='X'
        print(f"The next Player is {to_move}")
        board=Board5Misery(counter=self.counter, to_move=to_move, utility=0)
        if board.counter>=5:
            if player == 'X':
                board.utility=-1
            else:
                board.utility=1
        else:
            board.utility=0
        
        return board

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return 1 if player == 'X' else -1

    def is_terminal(self, state):
        """A board is a terminal state if state.utility>=5."""
        return state.counter >= 5

    def display(self, state): print(state)     


    

