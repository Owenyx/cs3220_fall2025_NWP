import collections

from src.problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram
from src.graphProblemClass import GraphProblem
from src.graphClass import Graph

class MazeProblemSolvingAgent(SimpleProblemSolvingAgentProgram):
  def __init__(
      self, 
      initial_state: str = None, 
      dataGraph: Graph = None, 
      goals: list[str] = None, # Treasure 
      end_goal: str = None, # Maze end
      program: collections.abc.Callable = None
  ):
    super().__init__(initial_state)

    self.dataGraph = dataGraph
    self.goals = goals
    self.end_goal = end_goal
    self.has_treasure = False
    
    self.performance = len(dataGraph.nodes()) // 2
    

    if program is None or not isinstance(program, collections.abc.Callable):
      print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

      def program(percept):
        return eval(input('Percept={}; action? '.format(percept)))

    self.program = program


  def update_state(self, state, percept):
    return percept

  def formulate_goal(self, state):
    if self.goals is not None:
      return self.goals
    else:
      print("No goal! can't work!")
      return None

  # A description of the states and actions necessary to reach the goal
  def formulate_problem(self, state, goal):
    problem = GraphProblem(state, goal, self.dataGraph)
    return problem  

  def search(self, problem):
    seq = self.program(problem)
    solution=self.actions_path(seq.path())
    print("Solution (a sequence of actions) from the initial state to a goal: {}".format(solution))
    return solution
  
  def actions_path(self, p):
    acts=[]
    for n in p:
      acts.append(n.action)
    return acts[1:]

  def run(self):
    print("goal list:", self.goals)
    if isinstance(self.goals, list) and len(self.goals) > 1:
      percept=self.state

      while len(self.goals) > 0:
        
        if self.has_treasure:
          current_goal = self.end_goal
        else:
          current_goal = self.goals[0]

        print("current percept:", percept)
        print("current goal:", current_goal)
        """Formulate a goal and problem, then search for a sequence of actions to solve it."""
        # 4-phase problem-solving process
        self.state = self.update_state(self.state, percept)
        goal = current_goal
        problem = self.formulate_problem(self.state, goal)
        self.seq.append(self.search(problem))
        percept=current_goal
        self.goals.remove(goal)
        print("goal list:", self.goals)
      if not self.seq:
        return None
      return self.seq
    else:
      print ("I have the only goal = {}". format(self.goals))
      return super().__call__(self.state)
