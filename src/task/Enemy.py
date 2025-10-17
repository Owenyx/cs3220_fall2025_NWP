import random
import math

class Enemy:
  def __init__(self, location, nodeCount: int):
    powerFloor = math.floor(nodeCount * 0.1)
    powerCeil = math.ceil(nodeCount * 0.4)
    self.power = random.randint(powerFloor, powerCeil)

    self.location = location