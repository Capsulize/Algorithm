import random
from typing import List, Dict, Set
from collections import deque
from . import input_models as inputs
from . import output_models as outputs


def capsulize(num_of_shifts: int,
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
        capsules = generate_capsules(spaces, employee_map)
        shifts.append(outputs.Shift(len(shifts), capsules, []))

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
    space_dependencies = {space_id: [] for space_id in workspaces.keys()}

    for space in workspaces.values():
        for employee_id in space.employee_ids:
            for dependency_employee_id in employees[employee_id].capsule_dependencies:
                space_dependencies[space.identifier].append(employees[dependency_employee_id].room_id)
                space_dependencies[employees[dependency_employee_id].room_id].append(space.identifier)

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

