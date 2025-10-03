from src.environmentClass import Environment
from src.locations import *
from src.task1.Task1Classes import *
from src.agentClass import Agent

import random

class HouseEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.things = []

    def percept(self, agent: Agent) -> list[Thing]:
        # All things in agent's location
        return self.list_things_at(agent.location)
  
    def list_things_at(self, location) -> list[Thing]:
        return [thing for thing in self.things if thing.location == location]
    
    def is_agent_alive(self, agent: Agent) -> bool:
        return agent.alive

    def update_agent_alive(self, agent: Agent):
        if agent.performance <= 0:
            agent.alive = False
            print("Agent {} is dead.".format(agent))

    def is_done(self):
        # If no live agents are found, or no things are on the house, end
        no_live_agents = not any(agent.is_alive() for agent in self.agents)
        no_things = len(self.things) == 0

        if (no_things):
            print('Cat has conquered the house!')

        return no_live_agents or no_things

    def execute_action(self, agent: Agent, action: str):
        if not self.is_agent_alive(agent):
            return

        if action == 'Right':
            # Move agent. Furthest it can move is room 5
            agent.location = min(agent.location + 1, 5)  
            agent.performance -= 1 # Incur energy cost

        elif action == 'Left':
            agent.location = max(agent.location - 1, 1)
            agent.performance -= 1

        elif action == 'Eat':
            # Check if mouse in same room
            mouse = self.find_in_room(agent.location, Mouse)
            if mouse and agent.performance >= 3:
                agent.performance += 10
                self.delete_thing(mouse)

        elif action == 'Drink':
            # Check if milk in same room
            milk = self.find_in_room(agent.location, Milk)
            if milk:
                agent.performance += 5
                self.delete_thing(milk)

        elif action == 'Fight':
            # Check if dog in same room
            dog = self.find_in_room(agent.location, Dog)
            if dog:
                if agent.performance >= 10:
                    # Win fight
                    agent.performance += 20
                    # Dog runs away
                    self.delete_thing(dog)
                else:
                    # Lose
                    agent.performance -= 10

        self.update_agent_alive(agent) # Check for signs of life

    def find_first_instance(self, things: list[Thing], thingClass=Thing):
        return next((thing for thing in things if isinstance(thing, thingClass)), None)

    def find_in_room(self, location: int, thingClass=Thing):
        things_in_room = self.list_things_at(location)
        return self.find_first_instance(things_in_room, thingClass)

    def add_thing(self, thing: Dog | Milk | Mouse | Agent, location=None):
        if thing in self.things or thing in self.agents:
            print("Can't add the same thing twice")
            return
        
        # Assign random loaction
        thing.location = location if location is not None else self.default_location(thing)
        print(f"Placed {thing} in room {thing.location}")

        if isinstance(thing, Agent):
            thing.performance = random.randint(1, 5)
            self.agents.append(thing)
            return
        
        # Thing is Dog, Mouse, or Milk
        self.things.append(thing)

        if isinstance(thing, Dog):
            # If mouse is already in room, move it
            mouse = self.find_in_room(thing.location, Mouse)
            if mouse is not None:
                self.move_mouse(mouse)

        elif isinstance(thing, Mouse):
            # If dog is already in room, move the mouse
            dog = self.find_in_room(thing.location, Dog)
            if dog is not None:
                self.move_mouse(thing)

            # If milk is already in room, mouse drinks it
            milk = self.find_in_room(thing.location, Milk)
            if milk is not None:
                self.delete_thing(milk)

        elif isinstance(thing, Milk):
            # If mouse is already in room, mouse drinks the milk
            mouse = self.find_in_room(thing.location, Mouse)
            if mouse is not None:
                self.delete_thing(thing)


    def move_mouse(self, mouse: Mouse):
        move_options = []
        if mouse.location != 1: # If not in leftmost room
            move_options.append(-1) # Can move left
        if mouse.location != 5: # If not in rightmost room
            move_options.append(1) # Can move left
        mouse.location += random.choice(move_options)

        print(f"Mouse moved to room {mouse.location}")

    def delete_thing(self, thing):
        if thing in self.agents:
            self.agents.remove(thing)
            print(f"{thing} was removed from the house")
        elif thing in self.things:
            self.things.remove(thing)
            print(f"{thing} was removed from the house")

    def default_location(self, thing):
        """Things start in any room at random."""
        return random.randint(1, 5)
    