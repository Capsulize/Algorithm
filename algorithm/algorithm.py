import random
import numpy
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
from collections import deque, namedtuple
from . import input_models as inputs
from . import output_models as outputs


def capsulize(num_of_shifts: int,
              max_carpool_distance: float,
              employees: List[inputs.Employee],
              workspaces: List[inputs.Workspace]):
    employee_map = {employee.identifier: employee for employee in employees}
    shift_spaces = {
        shift_id: {workspace.identifier: outputs.Workspace(workspace.identifier, workspace.capacity, set()) for
                   workspace in workspaces} for shift_id in range(num_of_shifts)}

    groups = generate_employee_groups(employee_map)

    for group in groups:
        shift = assign_group_shift(group)

        for employee in group:
            shift_spaces[shift][employee.room_id].employee_ids.add(employee.identifier)

    shifts = []

    for spaces in shift_spaces.values():
        occupied_spaces = [space for space in spaces if not space.is_empty()]
        capsules = generate_capsules(occupied_spaces, employee_map)
        shifts.append(outputs.Shift(len(shifts), capsules, []))

    for shift in shifts:
        employees = {employee_id: employee_map[employee_id] for employee_id in shift.employee_ids()}
        shift.cars = generate_shift_cars(employees, max_carpool_distance)

    return shifts


def generate_employee_groups(employees: Dict[int, inputs.Employee]) -> List[Set[inputs.Employee]]:
    groups = []

    for employee in employees.values():
        for dependency_id in employee.shift_dependencies:
            employees[dependency_id].shift_dependencies.add(employee.identifier)
        employee.has_group = False

    for employee in employees.values():
        if employee.has_group:
            continue

        new_group = set()
        employee_queue = deque([employee])

        while len(employee_queue) > 0:
            current_employee = employee_queue.popleft()

            if current_employee.has_group:
                continue

            new_group.add(current_employee)
            current_employee.has_group = True

            for dependency_id in current_employee.shift_dependencies:
                if not employees[dependency_id].has_group:
                    employee_queue.append(employees[dependency_id])

        groups.append(new_group)

    return groups


def assign_group_shift(group: Set[inputs.Employee]) -> int:
    possible_shifts = list(group)[0].shift_availability

    for employee in group:
        possible_shifts = possible_shifts & employee.shift_availability

    # TODO: find a smarter way to do this
    return list(possible_shifts)[random.randrange(0, len(possible_shifts))]


def generate_capsules(workspaces: Dict[int, outputs.Workspace],
                      employees: Dict[int, inputs.Employee]) -> List[outputs.Capsule]:
    capsules = []
    space_dependencies = {space_id: set() for space_id in workspaces.keys()}

    for space in workspaces.values():
        for employee_id in space.employee_ids:
            for dependency_employee_id in employees[employee_id].capsule_dependencies:
                if space.identifier is not employees[dependency_employee_id].room_id:
                    space_dependencies[space.identifier].add(employees[dependency_employee_id].room_id)
                    space_dependencies[employees[dependency_employee_id].room_id].add(space.identifier)

        space.has_capsule = False

    for space in workspaces.values():
        if space.has_capsule:
            continue

        new_capsule = outputs.Capsule(len(capsules), set())
        space_queue = deque([space])

        while len(space_queue) > 0:
            current_space = space_queue.popleft()

            if current_space.has_capsule:
                continue

            new_capsule.workspaces.add(current_space)
            current_space.has_capsule = True

            for space_dependency_id in space_dependencies[current_space.identifier]:
                if not workspaces[space_dependency_id].has_capsule:
                    space_queue.append(workspaces[space_dependency_id])

            capsules.append(new_capsule)

    return capsules


def rebalance_capsules(capsules: List[outputs.Capsule], employees: Dict[int, inputs.Employee]):
    pass


def calc_employee_capsule_priority(target_employee: inputs.Employee, employees: Dict[int, inputs.Employee]):
    reversed_dependencies = {employee_id: [] for employee_id in employees.keys()}
    employee_priorities = {employee_id: 0 for employee_id in employees.keys()}

    for employee in employees.values():
        for dependency_id in employee.capsule_dependencies:
            reversed_dependencies[dependency_id] = employee.identifier

    for employee_id in reversed_dependencies.keys():
        counted_ids = list()
        id_queue = deque([employee_id])

        while len(id_queue) > 0:
            current_id = id_queue.popleft()

            if current_id in counted_ids:
                continue

            employee_priorities[employee_id] += 1

            for dependency_id in employees.keys():
                if dependency_id not in counted_ids:
                    id_queue.append(dependency_id)


def generate_shift_cars(employees: Dict[int, inputs.Employee], max_carpool_distance: float) -> List[outputs.Car]:
    cars = [outputs.Car(employee.identifier, employee.car_capacity, set()) for employee in employees.values() if
            employee.is_driver()]

    def distance(source: Tuple[float, float], destination: Tuple[float, float]) -> float:
        return numpy.linalg.norm(
            [source_scalar - destination_scalar for source_scalar, destination_scalar in zip(source, destination)])

    for employee in employees.values():
        employee.possible_cars = deque()

        if employee.is_driver() > 0:
            continue

        for car in cars:
            if distance(employee.home_location, employees[car.owner_id].home_location) > max_carpool_distance:
                continue

            employee.possible_cars.append(car)

        employee.possible_cars = sorted(employee.possible_cars,
                                        key=lambda car: distance(employee.home_location,
                                                                 employees[car.owner_id].home_location))

    sorted_employees = sorted(employees.values(), key=lambda employee: len(employee.possible_cars))

    for employee in sorted_employees:
        for car in employee.possible_cars:
            if not car.is_full():
                car.employee_ids.append(employee.identifier)
                break

    return cars
