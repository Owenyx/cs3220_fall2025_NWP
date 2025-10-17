from src.environmentClass import Environment
from src.task.Enemy import Enemy
import numpy as np
import math

class AsteroidEnvironment(Environment):
  def __init__(self, mazeGraph, mazeArray):
    super().__init__()
    self.status = mazeGraph

    # Add enemies at their respective locations
    self.enemies = []
    locations = np.argwhere(mazeArray == 2)

    for loc in locations:
      # loc is like [row, col]
      row, col = map(int, loc)
      enemy = Enemy((row, col), len(mazeGraph.nodes()))
      self.enemies.append(enemy)
    

  def percept(self, agent): # Return agents state, and if an enemy is there with it
    enemy = self.find_enemy_at(agent.state)

    return agent.state, enemy
  
  def find_enemy_at(self, location):
    for enemy in self.enemies:
      if enemy.location == location:
        return enemy
    return None

  def is_agent_alive(self, agent):
    return agent.alive

  def update_agent_alive(self, agent):
    if agent.performance <= 0:
      agent.alive = False
      print(f"{agent} is dead.")
    elif agent.state==agent.goal or len(agent.seq)==0:
      agent.alive = False
      if len(agent.seq)==0:
        print(f"{agent} reached all goals")
      else:
        print(f"{agent} reached the goal: {agent.goal}")
      

  def execute_action(self, agent, action):
    '''Check if agent alive, if so, execute action'''
    if self.is_agent_alive(agent):
        """Change agent's location -> agent's state;
        Track performance.
        -1 for each move."""
        agent.state=agent.update_state(agent.state, action)
        agent.performance -= 1
        print(f"{agent} in {agent.state} with performance = {agent.performance}")
        self.update_agent_alive(agent)

  
  def step(self):
    if not self.is_done():
        actions = []
        for agent in self.agents:
          if agent.alive:

            action=agent.seq.pop(0)
            print(f"{agent} decided to do {action}.")
            actions.append(action)
          else:
            actions.append("")
            
        for (agent, action) in zip(self.agents, actions):
          self.execute_action(agent, action)

          # Check for enemies
          agentState, enemy = self.percept(agent)
          if enemy is not None:
            print(f"{agent} encountered an enemy!")
            if agent.performance * 2 <= enemy.power:
              print(f"{agent} has been captured by an enemy starship")
            else:
              # Subtract 10% performance
              agent.performance = math.ceil(agent.performance - agent.performance * 0.1)
              print(f"{agent} has activated defense mode")
    else:
        print("There is no one here who could work...")
  
  def is_done(self):
    done = not any(agent.alive for agent in self.agents)
    
    if done:
      # Find winner
      perf1 = self.agents[0].performance
      perf2 = self.agents[1].performance

      winner = None
      if perf1 > perf2:
        winner = 1
      elif perf2 > perf1:
        winner = 2
      
      if winner is None:
        print("Both agents ended with equal performance, it's a tie!")
      else:
        print(f"Agent {winner} has won!")

    return done