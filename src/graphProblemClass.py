from src.problemClass import Problem

class GraphProblem(Problem):

    """The problem of searching a graph from one node to another."""
    '''
    The state space is stored as nested dictionaries
    G={'node1':{'neighbor1_of_Node1':distance_from_Node1_to_neighbor1_of_Node1,..},
       .....}

    '''

    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph # The state space - This is Graph class

    def actions(self, A):
        """The actions at a graph node are just its neighbors."""
        return list(self.graph.get(A).values()) # List of neighbours

    def result(self, state, action):
      """Return the resulting state after performing an action, or None if invalid."""
      if state not in self.graph:
        return None  # no outgoing actions from this state

      for next_state, act in self.graph[state].items():
        if act == action:
            return next_state

      return None  # action not valid for this state

    def path_cost(self, cost_so_far, A, B):
      #An action cost function
        return cost_so_far + self.graph.get(A, B)