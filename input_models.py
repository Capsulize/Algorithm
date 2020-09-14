from datetime import time
from .model import Model


class InputModel(Model):
    pass


class Workspace(InputModel):
    def __init__(self, identifier: int = 0, capacity: int = 0):
        super().__init__(identifier)
        self.capacity = capacity


class Person(InputModel):
    def __init__(self, identifier: int = 0, home_location: (float, float) = (0, 0), car_capacity: int = 0,
                 shift_dependencies: list = None, capsule_dependencies: list = None, shift_availability: list = None,
                 workspace_id: int = 0):
        super().__init__(identifier)
        self.home = home_location
        self.car_capacity = car_capacity
        self.shift_dependencies = shift_dependencies or []
        self.capsule_dependencies = capsule_dependencies or []
        self.availability = shift_availability
        self.workspace = workspace_id


class Shift:
    def __init__(self, identifier: int = 0, start_time: time = None, end_time: time = None):
        super().__init__(identifier)
        self.start = start_time
        self.end = end_time
