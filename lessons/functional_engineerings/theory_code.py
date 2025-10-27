from typing import Callable

import random
from dataclasses import dataclass
from enum import Enum, auto


class Element:
    EMPTY: str = "0"
    
    def __init__(self, symbol: str):
        self.symbol = symbol


class Board:
    def __init__(self, size: int):
        self.size = size
        self.cells = []
        for _ in range(size):
            cells_line = []
            for _ in range(size):
                cells_line.append(self.set_cell_symbol())
            self.cells.append(cells_line)

    def set_cell_symbol(self, symbol: str = None):
        if not symbol:
            symbol = Element.EMPTY
        return Element(symbol)


class BoardState:
    def __init__(self, board: Board, score: int):
        self._board = board
        self._score = score

    @property
    def board(self):
        return self._board
    
    @property
    def score(self):
        return self._score
    
    def fill_empty_cells(self) -> "BoardState":
        return Game.fill_empty_spaces(self)
    
    def do_process_cascade(self) -> "BoardState":
        return Game.process_cascade(self)
    
    def pipe(self, func: Callable) -> "BoardState":
        return func(self)


class MatchDirection(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()

@dataclass
class Match:
    direction: MatchDirection
    row: int
    col: int
    length: int


class Game:
    _symbols = ['A', 'B', 'C', 'D', 'E', 'F']
    _dimension = 8
    _randomizer = random.choice
    
    @staticmethod
    def draw(board: Board) -> None:
        print("  0 1 2 3 4 5 6 7")
        for i in range(board.size):
            print(f"{i} ", end="")
            for j in range(board.size):
                print(f"{board.cells[i][j].symbol} ", end="")
            print()
        print()

    @staticmethod
    def clone_board(board) -> Board:
        b = Board(board.size)
        for row in range(board.size):
            for col in range(board.size):
                b.cells[row][col] = board.cells[row][col]
        return b
        
    @staticmethod
    def initialize_game(board_size: int) -> BoardState:
        return BoardState(Board(board_size), 0).pipe(BoardState.fill_empty_cells).pipe(BoardState.do_process_cascade)

    @staticmethod
    def read_move(bs: BoardState) -> BoardState:
        print(">")
        user_input = input()
        if user_input == "q":
            exit(0)
            
        board = Game.clone_board(bs.board)
        coords = user_input.split()
        x = int(coords[1])
        y = int(coords[0])
        x1 = int(coords[3])
        y1 = int(coords[2])
        
        # Swap elements
        e = board.cells[y][x]
        board.cells[y][x] = board.cells[y1][x1]
        board.cells[y1][x1] = e
        
        return BoardState(board, bs.score)

    @staticmethod
    def add_match_if_valid(matches: list[Match], row: int, col: int, 
                          length: int, direction: MatchDirection) -> None:
        # Only consider combinations of 3 or more elements
        if length >= 3:
            matches.append(Match(direction, row, col, length))

    @staticmethod
    def find_matches(board: Board) -> list[Match]:
        matches = []

        # Horizontal combinations
        for row in range(board.size):
            start_col = 0
            for col in range(1, board.size):
                # Skip empty cells at start of row
                if board.cells[row][start_col].symbol == Element.EMPTY:
                    start_col = col
                    continue

                # If current cell is empty, break current sequence
                if board.cells[row][col].symbol == Element.EMPTY:
                    Game.add_match_if_valid(matches, row, start_col, 
                                          col - start_col, MatchDirection.HORIZONTAL)
                    start_col = col + 1
                    continue

                # Check symbol matches for non-empty cells
                if board.cells[row][col].symbol != board.cells[row][start_col].symbol:
                    Game.add_match_if_valid(matches, row, start_col, 
                                          col - start_col, MatchDirection.HORIZONTAL)
                    start_col = col
                elif col == board.size - 1:
                    Game.add_match_if_valid(matches, row, start_col, 
                                          col - start_col + 1, MatchDirection.HORIZONTAL)

        # Vertical combinations
        for col in range(board.size):
            start_row = 0
            for row in range(1, board.size):
                # Skip empty cells at start of column
                if board.cells[start_row][col].symbol == Element.EMPTY:
                    start_row = row
                    continue

                # If current cell is empty, break current sequence
                if board.cells[row][col].symbol == Element.EMPTY:
                    Game.add_match_if_valid(matches, start_row, col, 
                                          row - start_row, MatchDirection.VERTICAL)
                    start_row = row + 1
                    continue

                # Check symbol matches for non-empty cells
                if board.cells[row][col].symbol != board.cells[start_row][col].symbol:
                    Game.add_match_if_valid(matches, start_row, col, 
                                          row - start_row, MatchDirection.VERTICAL)
                    start_row = row
                elif row == board.size - 1:
                    Game.add_match_if_valid(matches, start_row, col, 
                                          row - start_row + 1, MatchDirection.VERTICAL)

        return matches
    
    @staticmethod
    def remove_matches(current_state: BoardState, matches: list[Match]) -> BoardState:
        if not matches:
            return current_state

        # Step 1: Mark cells for removal
        marked_cells = Game.mark_cells_for_removal(current_state.board, matches)

        # Step 2: Apply gravity
        gravity_applied_cells = Game.apply_gravity(marked_cells, current_state.board.size)

        # Step 3: Calculate score
        removed_count = sum(match.length for match in matches)
        new_score = current_state.score + Game.calculate_score(removed_count)

        # Create new board with updated cells
        new_board = Board(current_state.board.size)
        new_board.cells = gravity_applied_cells

        # Return NEW state
        return BoardState(new_board, new_score)

    @staticmethod
    def mark_cells_for_removal(board: Board, matches: list[Match]) -> list[list[Element]]:
        # Create a deep copy of the board cells
        new_cells = []
        for row in board.cells:
            new_row = []
            for cell in row:
                new_row.append(Element(cell.symbol))
            new_cells.append(new_row)

        # Mark matched cells as empty
        for match in matches:
            for i in range(match.length):
                row = match.row if match.direction == MatchDirection.HORIZONTAL else match.row + i
                col = match.col + i if match.direction == MatchDirection.HORIZONTAL else match.col
                new_cells[row][col] = Element(Element.EMPTY)

        return new_cells

    @staticmethod
    def apply_gravity(cells: list[list[Element]], size: int) -> list[list[Element]]:
        # Initialize new empty cells
        new_cells = []
        for _ in range(size):
            row = []
            for _ in range(size):
                row.append(Element(Element.EMPTY))
            new_cells.append(row)

        # Apply gravity column by column
        for col in range(size):
            new_row = size - 1
            for row in range(size - 1, -1, -1):
                if cells[row][col].symbol != Element.EMPTY:
                    new_cells[new_row][col] = cells[row][col]
                    new_row -= 1

        return new_cells

    @staticmethod
    def calculate_score(removed_count: int) -> int:
        # Basic scoring system: 10 points per element
        return removed_count * 10

    @staticmethod
    def fill_empty_spaces(current_state: BoardState, randomizer: Callable = None) -> BoardState:
        if not current_state.board.cells:
            return current_state
        
        if not randomizer:
            randomizer = Game._randomizer

        # Create a deep copy of the board cells
        new_cells = []
        for row in current_state.board.cells:
            new_row = []
            for cell in row:
                new_row.append(Element(cell.symbol))
            new_cells.append(new_row)

        # Fill empty cells with random symbols
        for row in range(current_state.board.size):
            for col in range(current_state.board.size):
                if new_cells[row][col].symbol == Element.EMPTY:
                    random_symbol = randomizer(Game._symbols)
                    new_cells[row][col] = Element(random_symbol)

        # Create new board with filled cells
        new_board = Board(current_state.board.size)
        new_board.cells = new_cells

        return BoardState(new_board, current_state.score)
    
    def process_cascade(bs: BoardState) -> BoardState:
        matches = Game.find_matches(bs.board)
        if not matches:
            return bs
        new_bs = Game.remove_matches(bs, matches)
        return (
            new_bs.pipe(lambda bs: Game.fill_empty_spaces(bs, randomizer=Game._randomizer))
            .pipe(lambda nbs: Game.process_cascade(nbs))
        )


def main():
    bs = Game.initialize_game(Game._dimension)
    while True:
        Game.draw(bs.board)
        bs = Game.read_move(bs)
        bs = Game.process_cascade(bs)

if __name__ == "__main__":
    main()