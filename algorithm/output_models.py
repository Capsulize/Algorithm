from dataclasses import dataclass
from typing import Tuple, List, Set
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Car:
    identifier: int
    owner_id: int
    employee_ids: Set[int]


@dataclass_json
@dataclass
class Workspace:
    identifier: int
    max_capacity: int
    employee_ids: Set[int]

    def is_full(self):
        return self.occupancy() == self.max_capacity

    def occupancy(self):
        return len(self.employee_ids)


@dataclass_json
@dataclass
class Capsule:
    identifier: int
    workspaces: Set[Workspace]


@dataclass_json
@dataclass
class Shift:
    identifier: int
    capsules: List[Capsule]
    cars: List[Car]


