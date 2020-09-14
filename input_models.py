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
class Employee:
    identifier: int
    home: Tuple[float, float]
    car_capacity: int
    shift_dependencies: List[int]
    capsule_dependencies: List[int]
    shift_availability: List[int]
