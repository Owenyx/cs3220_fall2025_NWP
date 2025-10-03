from src.environmentClass import Environment
from src.task2.Task2Classes import *

import random

class CatFriendlyHouse(Environment):
    def __init__(self):
        super().__init__()
        self.food = []
        self.status = {
            1: 'Unknown',
            2: 'Unknown'
        } # Both rooms initially unknown

    def percept(self, cat: Agent_Cat):
        # Sets status of room based on percept, and returns the agent's location and the room status
        status = self.get_room_status(cat.location)
        self.status[cat.location] = status
        return (cat.location, status)
    
    def get_room_status(self, location: int) -> str:
        food_in_room = self.get_food_at(location)

        if isinstance(food_in_room, Sausage):
            return "SausageHere"
        
        if isinstance(food_in_room, Milk):
            return "MilkHere"
        
        return "Empty"
  
    def get_food_at(self, location) -> Food | None:
        for food in self.food:
            if food.location == location:
                return food
            
        return None
    
    def get_status(self) -> str:
        room_things = map(self.get_food_at, range(1, 2))
        r1, r2 = list(room_things)
        
        # Add agent to corrosponding room
        cat = self.agents[0]
        if cat.location == 1:
            r1 = [r1, cat]
        else:
            r2 = [r2, cat]
        
        return f"| 1. {r1} | 2. {r2} |"
    
    def is_cat_alive(self, cat: Agent_Cat) -> bool:
        return cat.alive

    def update_cat_alive(self, cat: Agent_Cat):
        if cat.performance <= 0:
            cat.alive = False
            print("Cat is dead.")

    def is_done(self):
        # If no live agents are found, or no food is in the house, end
        no_live_agents = not any(agent.is_alive() for agent in self.agents)
        no_food = len(self.food) == 0

        if (no_food):
            print('Cat has ate all the food!')

        return no_live_agents or no_food

    def execute_action(self, cat: Agent_Cat, action: str):
        if not self.is_cat_alive(cat):
            return

        if action == 'Right':
            cat.location = 2  
            cat.performance -= 1 # Incur energy cost

        elif action == 'Left':
            cat.location = 1
            cat.performance -= 1

        elif action == 'Eat':
            if cat.eat(self.get_food_at(cat.location)):
                # Remove sausage from room if successful
                self.delete_thing(self.get_food_at(cat.location))

        elif action == 'Drink':
            if cat.drink(self.get_food_at(cat.location)):
                # Remove milk from room if successful
                self.delete_thing(self.get_food_at(cat.location))

        elif action == None:
            cat.performance = 0 # If no action stop the cat

        self.update_cat_alive(cat) # Check for signs of life

    def add_thing(self, thing: Agent_Cat | Milk | Sausage, location=None):
        if thing in self.food or thing in self.agents:
            print("Can't add the same thing twice")
            return
        
        # Assign random loaction
        thing.location = location if location is not None else self.default_location(thing)
        print(f"Placed {thing} in room {thing.location}")

        if isinstance(thing, Agent_Cat):
            thing.performance = 3
            self.agents.append(thing)
            return
        
        # Thing is Sausage or Milk
        self.food.append(thing)

    def delete_thing(self, thing):
        if thing in self.agents:
            self.agents.remove(thing)
            print(f"{thing} was removed from the house")
        elif thing in self.food:
            self.food.remove(thing)
            print(f"{thing} was removed from the house")

    def default_location(self, thing):
        """Things start in any room at random."""
        location = random.randint(1, 2)

        # If thing is food, and food is in the room selected, then place it in the other room
        if isinstance(thing, Food) and self.get_food_at(location) is not None:
            if location == 1:
                location = 2
            else:
                location = 1
        
        return location