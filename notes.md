Initial state should only be added into a derived class
State is an object, and active player will be a property of the state object

A state is a terminal state if it has no actions available from it - i.e. it is a leaf node
- This is reflected in the implementation of is_terminal in the game class

Strategy is only calculated **once** for each player, at the start of the game
- During the game, each player just follows their predetermined moves
- They call their strategy function at each step just to grab the move they should take

## Board
defaultdict is a customizable dictionary
We can add more customization in Board class by inheriting defaultdict, while still getting all functionality of a dictionary

__init__ is for initialization, which requires that the object is already created
- When moving from one state to another, we cannot be making a new instance each time, we just change an existing one
- So, we use .new since it's a custom function for updating a current assignment