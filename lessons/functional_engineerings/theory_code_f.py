import random
from enum import Enum
from functools import partial
from typing import Any, Callable, List, TypedDict, cast


# runtime helper — словарь с точечной нотацией
class DotDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )

    def __setattr__(self, key, value):
        self[key] = value


# Enum для типизации
class MatchDirection(str, Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


# TypedDict только для статической типизации
class ElementTD(TypedDict):
    EMPTY: str = "0"
    symbol: str


class BoardTD(TypedDict):
    size: int
    cells: List[List[ElementTD]]


class BoardStateTD(TypedDict):
    board: BoardTD
    score: int


class MatchTD(TypedDict):
    direction: MatchDirection
    row: int
    col: int
    length: int


# runtime factory возвращает DotDict, но мы явно приводим его к TypedDict для типизации
def create_element(symbol: str | None = None) -> ElementTD:
    if symbol is None:
        symbol = ElementTD.EMPTY
    elem = DotDict(EMPTY=ElementTD.EMPTY, symbol=symbol)
    return cast(ElementTD, elem)


def create_board(s: int) -> BoardTD:
    board = DotDict(size=s, cells=[])
    for _ in range(s):
        row = []
        for _ in range(s):
            row.append(create_element())
        board["cells"].append(row)
    return cast(BoardTD, board)


def create_board_state(board: BoardTD, score: int = 0) -> BoardStateTD:
    return cast(BoardStateTD, DotDict(board=board, score=score))


def create_match(direction: str, row: int, col: int, length: int) -> MatchTD:
    return cast(MatchTD, DotDict(direction=direction, row=row, col=col, length=length))


# вспомогательные функции utils
def pipe(value: Any, *funcs: Callable) -> Any:
    for f in funcs:
        value = f(value)
    return value


# игровые функции
def initialize_game(board_size: int) -> BoardStateTD:
    return pipe(
        create_board(board_size),
        lambda b: create_board_state(b),
        lambda bs: fill_empty_spaces(bs),
        lambda bs: process_cascade(bs),
    )


def draw(bs: BoardStateTD, ask: bool = False) -> BoardStateTD:
    board: BoardTD = bs.board
    print("  0 1 2 3 4 5 6 7")
    for i in range(board.size):
        print(f"{i} ", end="")
        for j in range(board.size):
            print(f"{board.cells[i][j].symbol} ", end="")
        print()
    print()
    if ask:
        input()
    return bs


def clone_board(board: BoardTD) -> BoardTD:
    b: BoardTD = create_board(board.size)
    for row in range(board.size):
        for col in range(board.size):
            b.cells[row][col] = board.cells[row][col]
    return b


def read_move(bs: BoardStateTD) -> BoardStateTD:
    print(">")
    user_input = input("Your turn: ")
    if user_input == "q":
        exit(0)

    board = clone_board(bs.board)
    coords = user_input.split()
    x = int(coords[1])
    y = int(coords[0])
    x1 = int(coords[3])
    y1 = int(coords[2])

    # Swap elements
    e = board.cells[y][x]
    board.cells[y][x] = board.cells[y1][x1]
    board.cells[y1][x1] = e

    return create_board_state(board, bs.score)


def add_match_if_valid(
    matches: list[MatchTD], row: int, col: int, length: int, direction: MatchDirection
) -> None:
    # Only consider combinations of 3 or more elements
    if length >= 3:
        matches.append(create_match(direction, row, col, length))


def find_matches(board: BoardTD) -> list[MatchTD]:
    """
    Find all matches on the board based on provided patterns

    Args:
        bs: Current board state
        patterns: List of pattern templates to search for

    Returns:
        List of found matches with absolute positions
    """

    matches = []

    # Horizontal combinations
    for row in range(board.size):
        start_col = 0
        for col in range(1, board.size):
            # Skip empty cells at start of row
            if board.cells[row][start_col].symbol == ElementTD.EMPTY:
                start_col = col
                continue

            # If current cell is empty, break current sequence
            if board.cells[row][col].symbol == ElementTD.EMPTY:
                add_match_if_valid(
                    matches, row, start_col, col - start_col, MatchDirection.HORIZONTAL
                )
                start_col = col + 1
                continue

            # Check symbol matches for non-empty cells
            if board.cells[row][col].symbol != board.cells[row][start_col].symbol:
                add_match_if_valid(
                    matches, row, start_col, col - start_col, MatchDirection.HORIZONTAL
                )
                start_col = col
            elif col == board.size - 1:
                add_match_if_valid(
                    matches,
                    row,
                    start_col,
                    col - start_col + 1,
                    MatchDirection.HORIZONTAL,
                )

    # Vertical combinations
    for col in range(board.size):
        start_row = 0
        for row in range(1, board.size):
            # Skip empty cells at start of column
            if board.cells[start_row][col].symbol == ElementTD.EMPTY:
                start_row = row
                continue

            # If current cell is empty, break current sequence
            if board.cells[row][col].symbol == ElementTD.EMPTY:
                add_match_if_valid(
                    matches, start_row, col, row - start_row, MatchDirection.VERTICAL
                )
                start_row = row + 1
                continue

            # Check symbol matches for non-empty cells
            if board.cells[row][col].symbol != board.cells[start_row][col].symbol:
                add_match_if_valid(
                    matches, start_row, col, row - start_row, MatchDirection.VERTICAL
                )
                start_row = row
            elif row == board.size - 1:
                add_match_if_valid(
                    matches,
                    start_row,
                    col,
                    row - start_row + 1,
                    MatchDirection.VERTICAL,
                )

    return matches


def remove_matches(current_state: BoardStateTD, matches: list[MatchTD]) -> BoardStateTD:
    if not matches:
        return current_state

    # Step 1: Mark cells for removal
    marked_cells = mark_cells_for_removal(current_state.board, matches)

    # Step 2: Apply gravity
    gravity_applied_cells = apply_gravity(marked_cells, current_state.board.size)

    # Step 3: Calculate score
    removed_count = sum(match.length for match in matches)
    new_score = current_state.score + calculate_score(removed_count)

    # Create new board with updated cells
    new_board = create_board(current_state.board.size)
    new_board.cells = gravity_applied_cells

    # Return NEW state
    return create_board_state(new_board, new_score)


def mark_cells_for_removal(
    board: BoardTD, matches: list[MatchTD]
) -> list[list[ElementTD]]:
    # Create a deep copy of the board cells
    new_cells = []
    for row in board.cells:
        new_row = []
        for cell in row:
            new_row.append(create_element(cell.symbol))
        new_cells.append(new_row)

    # Mark matched cells as empty
    for match in matches:
        for i in range(match.length):
            row = (
                match.row
                if match.direction == MatchDirection.HORIZONTAL
                else match.row + i
            )
            col = (
                match.col + i
                if match.direction == MatchDirection.HORIZONTAL
                else match.col
            )
            new_cells[row][col] = create_element(ElementTD.EMPTY)

    return new_cells


def apply_gravity(cells: list[list[ElementTD]], size: int) -> list[list[ElementTD]]:
    # Initialize new empty cells
    new_cells = []
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append(create_element(ElementTD.EMPTY))
        new_cells.append(row)

    # Apply gravity column by column
    for col in range(size):
        new_row = size - 1
        for row in range(size - 1, -1, -1):
            if cells[row][col].symbol != ElementTD.EMPTY:
                new_cells[new_row][col] = cells[row][col]
                new_row -= 1

    return new_cells


def calculate_score(removed_count: int) -> int:
    # Basic scoring system: 10 points per element
    return removed_count * 10


def fill_empty_spaces(current_state: BoardStateTD) -> BoardStateTD:
    if not current_state.board.cells:
        return current_state

    # Create a deep copy of the board cells
    new_cells = []
    for row in current_state.board.cells:
        new_row = []
        for cell in row:
            new_row.append(create_element(cell.symbol))
        new_cells.append(new_row)

    # Fill empty cells with random symbols
    for row in range(current_state.board.size):
        for col in range(current_state.board.size):
            if new_cells[row][col].symbol == ElementTD.EMPTY:
                random_symbol = random.choice(symbols_choice)
                new_cells[row][col] = create_element(random_symbol)

    # Create new board with filled cells
    new_board = create_board(current_state.board.size)
    new_board.cells = new_cells

    return create_board_state(new_board, current_state.score)


def process_cascade(bs: BoardStateTD) -> BoardStateTD:
    new_bs = pipe(bs.board, find_matches, partial(remove_matches, bs))
    if new_bs == bs:
        return new_bs
    
    return pipe(new_bs, fill_empty_spaces, process_cascade)


def game_engine():
    global DEBUG
    global symbols_choice

    DEBUG = True
    symbols_choice = ["A", "B", "C", "D", "E", "F"]
    board_size = 8

    bs = initialize_game(board_size)
    while True:
        draw(bs)
        bs = read_move(bs)
        bs = process_cascade(bs)


if __name__ == "__main__":
    game_engine()
