from src.problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram
from src.mazeProblemClass import MazeProblem
import math


class PacmanAgent(SimpleProblemSolvingAgentProgram):
  def __init__(self, initial_state=None, dataGraph=None, goal=None, food=None, program=None):
    super().__init__(initial_state)
    self.dataGraph=dataGraph
    self.goal=goal
    self.food=food
    self.performance = math.floor(len(dataGraph.nodes()) * 0.3)
    self.program = program

  
  def update_state(self, state, action):
    # Returns resulting state
    return self.dataGraph.origin[state][action]


  def formulate_goal(self, state):
    if len(self.food) > 0: # Get food first if exists
       return self.food
    if self.goal is not None:
      return self.goal
    else:
      print("No goal! Can't work!")
      return None
    
  
  def __call__(self, percept, curGoal=None):
        """Formulate a goal and problem, then
        search for a sequence of actions to solve it."""
        #4-phase problem-solving process
        goal = self.formulate_goal(self.state)
        
        problem = self.formulate_problem(self.state, goal)
        self.seq = self.search(problem)                 
                    
        if not self.seq:
            return None
              
        return None


  #a description of the states and actions necessary to reach the goal
  def formulate_problem(self, state, goal):
    #instance of Maze ProblemClass
    problem = MazeProblem(state, goal, self.dataGraph)
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