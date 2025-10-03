import random
from src.agentClass import Agent

class Food:
    def __init__(self, caloric_density, weight_min, weight_max):
        self.cal_density = caloric_density # Based on food type
        # Random 2 decimal float between max and min for weight
        self.weight = random.randint(weight_min, weight_max) 

    def __repr__(self):
        """Return a string representation of this Thing (as script name or class name)"""
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def get_calories(self):
        return self.cal_density * self.weight
    
    def show_state(self):
        print('----------')
        print(f"I am a {self}")
        print(f"Weight: {self.weight}")
        print(f"Caloric Density: {self.cal_density}")
        print(f"Total Calories: {self.get_calories()}")
        print('----------')
    

class Milk(Food):
    def __init__(self):
        super().__init__(caloric_density=2, weight_min=4, weight_max=8)


class Sausage(Food):
    def __init__(self):
        super().__init__(caloric_density=4, weight_min=2, weight_max=6)


class Agent_Cat(Agent):
    def eat(self, food) -> bool:
        if isinstance(food, Sausage):
            self.performance += food.get_calories()
            return True # Success
        return False # Failed to eat
       
    def drink(self, food) -> bool:
        if isinstance(food, Milk):
            self.performance += food.get_calories()
            return True
        return False