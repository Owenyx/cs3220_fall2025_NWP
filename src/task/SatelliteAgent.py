from src.problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram
from src.mazeProblemClass import MazeProblem
import collections


class SatelliteAgent(SimpleProblemSolvingAgentProgram):
  def __init__(self, initial_state=None, dataGraph=None, goal=None, program=None, name=None):
    super().__init__(initial_state)
    self.dataGraph=dataGraph
    self.goal=goal
    self.name = name

    self.performance=len(dataGraph.nodes())

    if program is None or not isinstance(program, collections.abc.Callable):
      print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

      def program(percept):
        return eval(input('Percept={}; action? '.format(percept)))

    self.program = program

  
  def __repr__(self):
    if self.name:
      return self.name
    return self.__class__.__name__


  def update_state(self, state, action):
    # Returns resulting state
    return self.dataGraph.origin[state][action]


  def formulate_goal(self, state):
    if self.goal is not None:
      return self.goal
    else:
      print("No goal! can't work!")
      return None


  #a description of the states and actions necessary to reach the goal
  def formulate_problem(self, state, goal):
    #instance of Maze ProblemClass
    problem = MazeProblem(state,goal,self.dataGraph)
    return problem  


  def search(self, problem):
    seq = self.program(problem)

    if seq is None:
      print('No solution could be found')
      return None

    solution=self.actions_path(seq.path())
    print("Solution (a sequence of actions) from the initial state to a goal: {}".format(solution))
    return solution
  

  def actions_path(self, p):
    acts=[]
    for n in p:
      acts.append(n.action)
    return acts[1:]