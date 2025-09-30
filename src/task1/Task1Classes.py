from src.thingClass import Thing

class Dog(Thing):
    def __init__(self):
        self.location = None

    def show_state(self):
        print(f'My location is {self.location}, woof woof')


class Mouse(Thing):
    def __init__(self):
        self.location = None

    def show_state(self):
        print(f'My location is {self.location}, squeak squeak')


class Milk(Thing):
    def __init__(self):
        self.location = None

    def show_state(self):
        print(f'My location is {self.location}, swish swosh')