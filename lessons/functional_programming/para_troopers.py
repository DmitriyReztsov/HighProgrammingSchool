from functools import reduce

from pymonad.list import ListMonad
from pymonad.state import State
from pymonad.tools import curry


def initialize_area(n: int, m: int, reference: tuple[int, int], area_struct: ListMonad) -> ListMonad:
    """Initialize the area with tuple(index vertical, index horizontal, initial zero)."""
    if n == reference[0]:
        return area_struct

    cell = (n, m, 0)  # (vertical index, horizontal index, initial value)
    if m == reference[1] - 1:
        return initialize_area(n + 1, 0, reference, area_struct + ListMonad(cell))
    else:
        return initialize_area(n, m + 1, reference, area_struct + ListMonad(cell))


@curry(3)
def deployment(n: int, m: int, cell: tuple) -> tuple | None:
    if n == cell[0] and m == cell[1]:
        return (n, m, 1)  # Set initial value to 1 for the first deployment
    return cell


def collect_curried_deployments(dep_func_list: list, l: int, battalion: list[int]) -> list:
    if l == 0:
        return dep_func_list

    return collect_curried_deployments(
        dep_func_list + [deployment(battalion[0] - 1, battalion[1] - 1)], l - 1, battalion[2:]
    )


def conquer_cell(area: ListMonad, dep_func_list: list) -> ListMonad:
    if not dep_func_list:
        return area

    deployment_func = dep_func_list[0]
    new_area = area.map(deployment_func)
    return conquer_cell(new_area, dep_func_list[1:])


def battalion_move(area: list[tuple], battalion: list[int], reference: tuple[int, int]) -> list[tuple]:
    if not area:
        return battalion

    battalion_new = []
    if area[0][2] == 1:  # If the cell is conquered
        # step up
        if area[0][0] > 0:
            battalion_new += [(area[0][0] - 1, area[0][1])]
        # step down
        if area[0][0] < reference[0] - 1:
            battalion_new += [(area[0][0] + 1, area[0][1])]
        # step left
        if area[0][1] > 0:
            battalion_new += [(area[0][0], area[0][1] - 1)]
        # step right
        if area[0][1] < reference[1] - 1:
            battalion_new += [(area[0][0], area[0][1] + 1)]

    return battalion_move(area[1:], battalion + battalion_new, reference)


def collect_curried_moves(dep_func_list: list, battalion: list[tuple[int, int]]) -> list:
    if not battalion:
        return dep_func_list

    return collect_curried_moves(dep_func_list + [deployment(battalion[0][0], battalion[0][1])], battalion[1:])


@curry(2)
def change_area_state(moves_func_list: list, days_status: dict[str, int | bool]) -> State:
    def compute_new_state(area: ListMonad) -> tuple[int, ListMonad]:
        new_area_state = conquer_cell(area, moves_func_list)
        conquest_is_completed = reduce(lambda x, y: x and y, (new_area_state.map(lambda x: x[2] == 1)).value)
        days_status["days"] += 1
        days_status["status"] = conquest_is_completed
        return (days_status, new_area_state)

    return State(compute_new_state)


def next_day_move(conquered_area: ListMonad, days_status: dict[str, int | bool], reference: tuple[int, int]) -> int:
    battalion_next = battalion_move(conquered_area.value, [], reference)
    moves_func_list = collect_curried_moves([], battalion_next)
    area_state = State.insert(days_status)
    area_state = area_state.then(change_area_state(moves_func_list))
    area_state = area_state.run(conquered_area)

    if area_state[0]["status"]:
        return area_state[0]["days"]

    return next_day_move(area_state[1], area_state[0], reference)


def conquest_campaign(n: int, m: int, l: int, battalion: list[int]) -> int:
    area = initialize_area(0, 0, (n, m), ListMonad())
    dep_func_list = collect_curried_deployments([], l, battalion)
    conquered_area = conquer_cell(area, dep_func_list)

    conquest_is_completed = reduce(lambda x, y: x and y, (conquered_area.map(lambda x: x[2] == 1)).value)
    if conquest_is_completed:
        return 1

    return next_day_move(conquered_area, {"days": 1, "status": conquest_is_completed}, (n, m))


if __name__ == "__main__":
    days = conquest_campaign(n=3, m=4, l=2, battalion=[2, 2, 3, 4])
    print(days)
