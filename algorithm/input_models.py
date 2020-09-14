from datetime import time
from dataclasses import dataclass
from typing import Tuple, Set
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Workspace:
    identifier: int
    capacity: int


@dataclass_json
@dataclass
class Employee:
    identifier: int
    room_id: int
    home_location: Tuple[float, float]
    car_capacity: int
    shift_dependencies: Set[int]
    capsule_dependencies: Set[int]
    shift_availability: Set[int]
