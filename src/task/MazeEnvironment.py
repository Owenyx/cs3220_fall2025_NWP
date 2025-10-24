from src.environmentClass import Environment
import math
from src.mazeData import draw_maze
from time import sleep

class MazeEnvironment(Environment):
  def __init__(self, mazeGraph, mazeArray):
    super().__init__()
    self.status = mazeGraph
    self.maze = mazeArray


  def percept(self, agent): # Return agents state, and if an ghost is there with it
    ghostInLoc = self.find_ghost_at(agent.state)

    return agent.state, ghostInLoc
  
  def find_ghost_at(self, location):
    row, col = location
    if self.maze[row][col] == 3:
      return True
    return False

  def is_agent_alive(self, agent):
    return agent.alive

  def update_agent_alive(self, agent):
    draw_maze(self.maze, agent.state)
    if agent.performance <= 0:
      agent.alive = False
      print(f"Agent is dead.")

    elif agent.state==agent.goal or len(agent.seq)==0:
      print(f"Agent reached the goal: {tuple(map(int, agent.goal))}")

      i, j = agent.state

      # Check if final goal
      if self.maze[i][j] == 5 and len(agent.food) == 0:
        print('Agent Won!!')
        agent.alive = False

      # Remove food and update goal
      if self.maze[i][j] == 2: # if just food
        agent.food.remove((i, j))
        self.maze[i][j] = 1 # Change to open path
        agent(agent.state) # Redefine goal
      elif self.maze[i][j] == 6 or self.maze[i][j] == 7: # Init or goal with food
        agent.food.remove((i, j))
        self.maze[i][j] -= 2 # Remove food
        agent(agent.state) # Redefine goal
      
      # Double performance
      agent.performance *= 2

  def execute_action(self, agent, action, interactive):
    if interactive:
      input("Press Enter to continue...")
    else:  
      sleep(0.1)

    '''Check if agent alive, if so, execute action'''
    if self.is_agent_alive(agent):
        """Change agent's location -> agent's state;
        Track performance.
        -1 for each move."""
        if action is not None:
          agent.state=agent.update_state(agent.state, action)
          agent.performance -= 1
        print(f"Agent in {agent.state} with performance = {agent.performance}")
        self.update_agent_alive(agent)

  def run(self, steps=10, interactive=False):
    #Run the Environment for given number of time steps.
    for step in range(steps):
        if self.is_done():
            return
        print("\nStep {0}:".format(step+1))
        self.step(interactive)
  
  def step(self, interactive):
    if not self.is_done():
        
        for agent in self.agents:
          actions = []
          if agent.alive and len(agent.seq) > 0:
            
            action=agent.seq.pop(0)
            print(f"Agent decided to do {action}.")
            actions.append(action)
          else:
            actions.append(None)
            
        for (agent, action) in zip(self.agents, actions):
          self.execute_action(agent, action, interactive)

          # Check for ghosts
          agentState, ghostInLoc = self.percept(agent)
          if ghostInLoc:
            print(f"Agent encountered an ghost!")
            if agent.performance < len(self.status.nodes()) * 0.3:
              print(f"Agent has been captured by a ghost")
              agent.alive = False
            else:
              # Subtract 10% performance
              agent.performance = math.ceil(agent.performance - agent.performance * 0.1)
              print(f"Agent has activated defense mode")

    else:
        print("There is no one here who could work...")
  
  def is_done(self):
    done = not any(agent.alive for agent in self.agents)
    
    return done