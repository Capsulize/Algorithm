import itertools
from dataclasses import dataclass
from typing import Tuple, List, Set
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Car:
    owner_id: int
    capacity: int
    employee_ids: Set[int]

    def is_full(self) -> bool:
        return self.occupancy() >= self.capacity

    def occupancy(self) -> int:
        return len(self.employee_ids)


@dataclass_json
@dataclass
class Workspace:
    identifier: int
    max_capacity: int
    employee_ids: Set[int]

    def is_full(self) -> bool:
        return self.occupancy() >= self.max_capacity

    def occupancy(self) -> int:
        return len(self.employee_ids)

    def __hash__(self):
        return self.identifier


@dataclass_json
@dataclass
class Capsule:
    identifier: int
    workspaces: Set[Workspace]

    def employee_ids(self) -> List[int]:
        return list(itertools.chain.from_iterable([space.employee_ids for space in self.workspaces]))


@dataclass_json
@dataclass
class Shift:
    identifier: int
    capsules: List[Capsule]
    cars: List[Car]

    def employee_ids(self) -> List[int]:
        return list(itertools.chain.from_iterable([capsule.employee_ids() for capsule in self.capsules]))
