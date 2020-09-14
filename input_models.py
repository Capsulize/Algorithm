from datetime import time


class InputModel:
    def __init__(self, identifier: int = 0):
        self.id = identifier


class Room(InputModel):
    def __init__(self, identifier: int = 0, capacity: int = 0):
        super().__init__(identifier)
        self.capacity = capacity


class Person(InputModel):
    def __init__(self, identifier: int = 0, home_location: (float, float) = (0, 0), car_capacity: int = 0,
                 dependencies: list = None, availability: list = None):
        super().__init__(identifier)
        self.home = home_location
        self.car_capacity = car_capacity
        self.dependencies = dependencies or []
        self.availability = availability


class Shift:
    def __init__(self, identifier: int = 0, start_time: time = None, end_time: time = None):
        super().__init__(identifier)
        self.start = start_time
        self.end = end_time
