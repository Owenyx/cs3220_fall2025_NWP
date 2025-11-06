from collections import defaultdict

class Board5Misery(defaultdict):
    """A board has the current value of the counter,
    the player to move, 
    a cached utility value, 
    where player is 'X' or 'O'."""
  
    
    def __init__(self, counter=1, to_move=None, **kwds):
        self.__dict__.update(counter=counter, to_move=to_move, **kwds)

    
    def __repr__(self):
        return f"state ({self.counter,self.to_move})"
        #def row(y): return ' '.join(self[x, y] for x in range(self.width))
        #return '\n'.join(map(row, range(self.height))) +  '\n'