from datetime import time
from dataclasses import dataclass
from typing import Tuple, List
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Workspace:
    identifier: int
    capacity: int


@dataclass_json
@dataclass
class Shift:
    identifier: int
    start: Tuple[int, int]
    end: Tuple[int, int]

    @property
    def start_time(self):
        return time(hour=self.start[0], minute=self.start[1])

    @property
    def end_time(self):
        return time(hour=self.end[0], minute=self.end[1])


@dataclass_json
@dataclass
class Person:
    identifier: int
    home: Tuple[float, float]
    car_capacity: int
    shift_dependencies: List[int]
    capsule_dependencies: List[int]
    availability: List[int]
