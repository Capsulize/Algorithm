import random
from typing import Tuple, List, Dict, Set
from collections import deque
from . import input_models as inputs
from . import output_models as outputs


def capsulize(num_of_shifts: int,
              employees: List[inputs.Employee],
              workspaces: List[inputs.Workspace]):
    shift_spaces = {
        shift_id: {workspace.identifier: outputs.Workspace(workspace.identifier, workspace.capacity, set()) for
                   workspace in workspaces} for shift_id in range(num_of_shifts)}

    groups = generate_employee_groups(employees)

    for group in groups:
        shift = assign_group_shift(group)

        for employee in group:
            shift_spaces[shift][employee.room_id].employee_ids.add(employee.identifier)


def generate_employee_groups(employees: List[inputs.Employee]) -> List[Set[inputs.Employee]]:
    groups = []
    employee_map = {employee.identifier: employee for employee in employees}

    for employee in employees:
        for dependency_id in employee.shift_dependencies:
            employee_map[dependency_id].shift_dependencies.add(employee.identifier)
        employee.has_group = False

    for employee in employees:
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
                if employee_map[dependency_id].has_group:
                    continue

                employee_queue.append(employee_map[dependency_id])

        groups.append(new_group)

    return groups


def assign_group_shift(group: Set[inputs.Employee]) -> int:
    possible_shifts = list(group)[0].shift_availability

    for employee in group:
        possible_shifts = possible_shifts & employee.shift_availability

    # TODO: find a smarter way to do this
    return list(possible_shifts)[random.randrange(0, len(possible_shifts))]
