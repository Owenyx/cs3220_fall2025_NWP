import random

class Food:
    def __init__(caloric_density, weight_min, weight_max):
        self.cal_density = caloric_density # Based on food type
        self.weight = random.randFloat(weight_min, weight_max)

    def get_calories(self):
        return self.cal_density * weight