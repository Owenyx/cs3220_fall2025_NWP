import random
from src.environmentProClass import environmentPro
from src.locations import *
from src.task3.Task3Classes import Student, ITStaff, OfficeManager



class CompanyEnvironment(environmentPro):
  def __init__(self):
    super().__init__()
    self.locations=[loc_A, loc_B, loc_C, loc_D]

  def default_location(self, thing):
    print("The item is starting in random location...")
    return random.choice(self.locations)

  def percept(self, agent):
    #return a list of things that are in our agent's location
    things = self.list_things_at(agent.location)
    return agent.location, things

  def execute_action(self, agent, action):
    #changes the state of the environment based on what the agent does.
    if self.is_agent_alive(agent):
      if action=='Go ahead':
        agent.location=self.locations[self.locations.index(agent.location)+1]
        agent.performance -= 1
        self.update_agent_alive(agent)
        print("The Agent decided to {} at location: {}".format(action,agent.location))
      elif action=='Give mail':
        items = self.list_things_at(agent.location, thingClass=OfficeManager)
        agent.performance += 3
        self.update_agent_alive(agent)
        print("The Agent decided to {} to {} at location: {}".format(action,items[0],agent.location))
        self.delete_thing(items[0])
      elif action=='Give donuts':
        items = self.list_things_at(agent.location, thingClass=ITStaff)
        agent.performance += 3
        self.update_agent_alive(agent)
        print("The Agent decided to {} to {} at location: {}".format(action,items[0],agent.location))
        self.delete_thing(items[0])
      elif action=='Give pizza':
        items = self.list_things_at(agent.location, thingClass=Student)
        agent.performance += 3
        self.update_agent_alive(agent)
        print("The Agent decided to {} to {} at location: {}".format(action,items[0],agent.location))
        self.delete_thing(items[0])
      elif action=='Stop':
        agent.alive=False
    
  def is_done(self):
    #no_items = not any(isinstance(thing, ITStaff) or isinstance(thing, OfficeManager) for thing in self.things)
    no_agents = not any(agent.is_alive() for agent in self.agents)
    #return no_agents or no_items
    return no_agents
  
  def get_status(self):
    room_things = map(self.list_things_at, self.locations)

    r1, r2, r3, r4 = list(room_things)
        
    # Add agent to corrosponding room
    agent = self.agents[0]
    if agent.location == 1:
      r1 = [r1, agent]
    elif agent.location == 2:
      r2 = [r2, agent]
    elif agent.location == 3:
      r3 = [r3, agent]
    else:
      r4 = [r4, agent]
        
    return f"| 1. {r1} | 2. {r2} | 3. {r3} | 4. {r4} |"