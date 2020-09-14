from dataclasses import dataclass
from typing import Tuple, List
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Car:
    identifier: int
    owner_id: int
    employee_ids: List[int]


@dataclass_json
@dataclass
class Workspace:
    identifier: int
    employee_ids: List[int]


@dataclass_json
@dataclass
class Capsule:
    identifier: int
    workspaces: List[Workspace]


@dataclass_json
@dataclass
class Shift:
    identifier: int
    capsules: List[Capsule]
    cars: List[Car]


