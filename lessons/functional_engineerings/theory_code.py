import random


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


class Game:
    _symbols = ['A', 'B', 'C', 'D', 'E', 'F']
    _dimension = 8
    
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
    def fill_board_empty_cells(board: Board) -> Board:
        b = Game.clone_board(board)
        for row in range(board.size):
            for col in range(board.size):
                if b.cells[row][col].symbol == Element.EMPTY:
                    random_symbol = random.choice(Game._symbols)
                    b.cells[row][col] = Element(random_symbol)
        return b
        
    @staticmethod
    def initialize_game() -> BoardState:
        # Create empty board
        board = Board(Game._dimension)
        
        # Fill board with random symbols
        board = Game.fill_board_empty_cells(board)

        # TODO: Add check for initial combinations
        # This would require implementing combination detection logic
        # If combinations exist, refill those positions until no combinations exist
        
        
        # Create initial board state with score 0
        board_state = BoardState(board, 0)

        return board_state

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
        e = board.cells[x][y]
        board.cells[x][y] = board.cells[x1][y1]
        board.cells[x1][y1] = e
        
        return BoardState(board, bs.score)


def main():
    bs = Game.initialize_game()
    while(True):
        Game.draw(bs.board)
        bs = Game.read_move(bs)


if __name__ == "__main__":
    main()