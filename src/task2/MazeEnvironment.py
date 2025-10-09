from src.environmentClass import Environment
from src.task1.BoatProblemSolvingAgent import BoatProblemSolvingAgent


class RiverEnvironment(Environment):
  def __init__(self, boat_graph):
    super().__init__()
    self.status = boat_graph
    

  def percept(self, agent):
    # Returns the agent's state
    return agent.state

  def is_agent_alive(self, agent: BoatProblemSolvingAgent):
    return agent.alive

  def update_agent_alive(self, agent: BoatProblemSolvingAgent):
    if agent.performance <= 0:
      agent.alive = False
      print("Agent {} is dead.".format(agent))
      return

    if agent.state == agent.goal or len(agent.seq)==0: # If goal is reached
      agent.alive = False
      if len(agent.seq)==0:
        print("Agent reached all goals")
      else:
        print(f"Agent reached the goal: {agent.goal}")
      

  def execute_action(self, agent: BoatProblemSolvingAgent, action: str):
    '''Check if agent alive, if so, execute action'''
    if self.is_agent_alive(agent):
        """
        Change agent's location -> agent's state;
        Track performance.
        -1 for each move.
        """
        agent.state = agent.update_state(agent.state, action)
        agent.performance -= 1
        print(f"Agent in {agent.state} with performance = {agent.performance}")
        self.update_agent_alive(agent)

  def step(self):
    if not self.is_done():
        actions = []
        for agent in self.agents:
          if agent.alive:
            # With agent.state because for PS Agent we don't need to percive
            action=agent.seq.pop(0)
            print("Agent decided to do {}.".format(action))
            actions.append(action)
          else:
            actions.append("")
            
        for (agent, action) in zip(self.agents, actions):
          self.execute_action(agent, action)
    else:
        print("There is no one here who could work...")
    