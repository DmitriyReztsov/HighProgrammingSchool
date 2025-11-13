from typing import Any, Callable, List, Iterable

import random
from dataclasses import dataclass
from enum import Enum, auto


class Element:
    EMPTY: str = "0"
    
    def __init__(self, symbol: str):
        self.symbol = symbol

    def is_empty(self) -> bool:
        return self.symbol == Element.EMPTY

    def equals(self, other: 'Element') -> bool:
        return self.symbol == other.symbol


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

@dataclass(frozen=True)
class Position:
    row: int
    col: int


@dataclass(frozen=True)
class Match:
    name: str                  # Name for identification
    origin: Position          # Absolute position of top-left corner
    width: int               # Rectangle width (in columns)
    height: int              # Rectangle height (in rows)
    pattern: List[Position]  # Relative positions inside rectangle

    def __post_init__(self):
        # Validate pattern positions are within bounds
        for pos in self.pattern:
            if (pos.row < 0 or pos.row >= self.height or 
                pos.col < 0 or pos.col >= self.width):
                raise ValueError("Relative position outside bounds")
        
        # Convert pattern to immutable tuple
        object.__setattr__(self, 'pattern', tuple(self.pattern))

    def get_absolute_positions(self) -> Iterable[Position]:
        """
        Returns absolute positions of the pattern on the board
        """
        origin_row = self.origin.row
        origin_col = self.origin.col
        
        return (
            Position(origin_row + rel_pos.row, origin_col + rel_pos.col)
            for rel_pos in self.pattern
        )


class Game:
    _symbols = ['A', 'B', 'C', 'D', 'E', 'F']
    _dimension = 8
    _randomizer = random.choice
    
    @staticmethod
    def draw(bs: BoardState, ask: bool = False) -> BoardState:
        board = bs.board
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
        user_input = input("Your turn: ")
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
    def find_matches(bs: BoardState, patterns: list[Match] = None) -> list[Match]:
        """
        Find all matches on the board based on provided patterns
        
        Args:
            bs: Current board state
            patterns: List of pattern templates to search for
            
        Returns:
            List of found matches with absolute positions
        """
        if patterns is None:
            patterns = Game.generate_level_matches(1)  # Default patterns
            
        found_matches = []
        board = bs.board

        for pattern in patterns:
            # Skip empty patterns
            if not pattern.pattern:
                continue

            # Search through all possible positions
            for row in range(board.size - pattern.height + 1):
                for col in range(board.size - pattern.width + 1):
                    candidate_origin = Position(row, col)
                    first_element = board.cells[row][col]

                    # Skip empty elements
                    if first_element.is_empty():
                        continue

                    is_valid = True

                    # Check all pattern positions
                    for rel_pos in pattern.pattern:
                        abs_row = row + rel_pos.row
                        abs_col = col + rel_pos.col

                        if (board.cells[abs_row][abs_col].is_empty() or
                            not board.cells[abs_row][abs_col].equals(first_element)):
                            is_valid = False
                            break

                    if is_valid:
                        found_matches.append(Match(
                            name=pattern.name,
                            origin=candidate_origin,
                            width=pattern.width,
                            height=pattern.height,
                            pattern=pattern.pattern
                        ))

        return found_matches
    
    @staticmethod
    def remove_matches(board_state: BoardState, matches: list[Match]) -> BoardState:
        """
        Remove matched elements from the board and calculate score
        
        Args:
            board_state: Current board state
            matches: List of matches to remove
            
        Returns:
            New BoardState with removed matches and updated score
        """
        if not matches:
            return board_state
            
        # Clone the board
        board = Game.clone_board(board_state.board)
        
        # Track removed elements for score
        removed_count = 0
        
        # Process all matches
        for match in matches:
            for position in match.get_absolute_positions():
                # Validate position is within bounds
                if (0 <= position.row < board.size and 
                    0 <= position.col < board.size):
                    board.cells[position.row][position.col] = Element(Element.EMPTY)
                    removed_count += 1
                    
        # Calculate new score (10 points per removed element)
        new_score = board_state.score + (removed_count * 10)
        
        return BoardState(board, new_score)

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
    def apply_gravity(board_state: BoardState) -> BoardState:
        """
        Apply gravity to make elements fall down into empty spaces
        
        Args:
            board_state: Current board state
            
        Returns:
            New BoardState with elements fallen down
        """
        board = Game.clone_board(board_state.board)
        
        # Process each column separately
        for col in range(board.size):
            # Find all non-empty elements in this column
            non_empty_elements = []
            
            # Collect all non-empty elements from top to bottom
            for row in range(board.size):
                if not board.cells[row][col].is_empty():
                    non_empty_elements.append(board.cells[row][col])
            
            # Calculate number of empty spaces at top
            empty_count = board.size - len(non_empty_elements)
            
            # Fill top rows with empty elements
            for row in range(empty_count):
                board.cells[row][col] = Element(Element.EMPTY)
                
            # Fill bottom rows with non-empty elements
            for row in range(empty_count, board.size):
                board.cells[row][col] = non_empty_elements[row - empty_count]
        
        return BoardState(board, board_state.score)

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
        matches = Game.find_matches(bs, Game.generate_level_matches())
        if not matches:
            return bs

        return Game.pipe(
            bs,
            lambda bs: Game.remove_matches(bs, matches),
            lambda bs: Game.draw(bs, DEBUG),
            lambda bs: Game.apply_gravity(bs),
            lambda bs: Game.draw(bs, DEBUG),
            lambda bs: Game.fill_empty_spaces(bs, randomizer=Game._randomizer),
            lambda bs: Game.draw(bs, DEBUG),
            Game.process_cascade
        )

    def pipe(value: Any, *funcs: Callable) -> Any:
        for f in funcs:
            value = f(value)
        return value

    @staticmethod
    def generate_level_matches(level: int) -> list[Match]:
        """
        Generate predefined match patterns for a given level
        
        Returns:
            List of Match patterns to check for
        """
        # Horizontal three-in-a-row pattern
        horizontal_match = Match(
            name="Horizontal three-in-a-row",
            origin=Position(0, 0),
            width=3,
            height=1,
            pattern=[
                Position(0, 0),
                Position(0, 1),
                Position(0, 2)
            ]
        )

        # Vertical three-in-a-row pattern
        vertical_match = Match(
            name="Vertical three-in-a-row",
            origin=Position(0, 0),
            width=1,
            height=3,
            pattern=[
                Position(0, 0),
                Position(1, 0),
                Position(2, 0)
            ]
        )

        return [horizontal_match, vertical_match]
    

def main():
    global DEBUG

    DEBUG = True
    bs = Game.initialize_game(Game._dimension)
    while True:
        Game.draw(bs)
        bs = Game.read_move(bs)
        bs = Game.process_cascade(bs)

if __name__ == "__main__":
    main()