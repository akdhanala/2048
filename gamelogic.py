# gamelogic.py
# Akhil Dhanala

"""
Module that implements the game logic and mechanics
behind 2048.
"""


# imports
import typing
import random
from itertools import groupby


# type annotations
Point = typing.Tuple[int, int]


# constants
_ROWS = 4
_COLS = 4
_EMPTY = 0
_LEFT = "LEFT"
_RIGHT = "RIGHT"
_UP = "UP"
_DOWN = "DOWN"
_X = 0
_Y = 1


# classes
class GameOverError(Exception):
    """Raised when the game is over."""
    pass


class InvalidInputError(Exception):
    """Raised when an invalid argument is passed into a method/ function"""
    pass


class GameLogic(object):
    """Object that implements the game logic behind 2048."""

    def __init__(self) -> None:
        """Initializes the GameLogic object."""
        self._board = _create_board()

        # Initializes the board with 2 numbers.
        for x in range(2):
            self._insert_random()

        # Holds the points in the game board that
        # have already been shifted.
        self._shifted_points = []
    
    # methods
    def get_board(self, board_format: str) -> list or dict:
        """Safely returns the board in the specified format."""
        if board_format not in ["LIST", "DICT"]:
            raise InvalidInputError()
        if board_format == "LIST":
            board = []
            for y in range(_ROWS):
                row = []
                for x in range(_COLS):
                    point = (x, y)
                    row.append(self._board[point])
                board.append(row)
        else:
            board = self._board
        
        return board

    def shift_left(self) -> None:
        """Shifts the board to the left."""
        self._shifted_points = []
        board = self.get_board("LIST")
        for y in range(_ROWS):
            row = []
            for x in range(_COLS):
                point = (x, y)
                row.append(self._board[point])
            self._shift_row_left(y, row)
        if board != self.get_board("LIST"):
            self._insert_random()
        self._game_over_check()

    def shift_right(self) -> None:
        """Shifts the board to the right."""
        self._shifted_points = []
        board = self.get_board("LIST")
        for y in range(_ROWS):
            row = []
            for x in range(_COLS):
                point = (x, y)
                row.append(self._board[point])
            self._shift_row_right(y, row)
        if board != self.get_board("LIST"):
            self._insert_random()
        self._game_over_check()

    def shift_up(self) -> None:
        """Shifts the board to the up."""
        self._shifted_points = []
        board = self.get_board("LIST")
        for x in range(_COLS):
            # Goes column by column
            col = []
            for y in range(_ROWS):
                point = (x, y)
                col.append(self._board[point])
            self._shift_col_up(x, col)
        if board != self.get_board("LIST"):
            self._insert_random()
        self._game_over_check()

    def shift_down(self) -> None:
        """Shifts the board to the down."""
        self._shifted_points = []
        board = self.get_board("LIST")
        for x in range(_COLS):
            # Goes column by column
            col = []
            for y in range(_ROWS):
                point = (x, y)
                col.append(self._board[point])
            self._shift_col_down(x, col)
        if board != self.get_board("LIST"):
            self._insert_random()
        self._game_over_check()
    
    def quit_game(self) -> None:
        """Quits the game by raising a GameOverError."""
        raise GameOverError()
    
    def _shift_row_left(self, row_num: int, row: [int]) -> None:
        """Shifts the specified block to the left."""
        y = row_num
        row = [i for i in row if i != _EMPTY]
        listPairs = [list(g) for k, g in groupby(row)]
        newRow = []
        for pair in listPairs:
            num = pair[0]
            for i in range(len(pair) // 2):
                newRow.append(num * 2)
            for i in range(len(pair) % 2):
                newRow.append(num)
        for empty in range(4 - len(newRow)):
            newRow.append(_EMPTY)
        for x, number in enumerate(newRow):
            point = (x, y)
            self._board[point] = number

    def _shift_row_right(self, row_num: int, row: [int]) -> None:
        """Shifts the row to the right."""
        y = row_num
        row = [i for i in row if i != _EMPTY]
        listPairs = [list(g) for k, g in groupby(row)]
        newRow = []
        for pair in listPairs[::-1]:
            num = pair[0]
            for i in range(len(pair) // 2):
                newRow.insert(0, num * 2)
            for i in range(len(pair) % 2):
                newRow.insert(0, num)
        for empty in range(4 - len(newRow)):
            newRow.insert(0, _EMPTY)
        for x, number in enumerate(newRow):
            point = (x, y)
            self._board[point] = number

    def _shift_col_up(self, col_num: int, col: [int]) -> None:
        """Shifts the specified block to the up."""
        x = col_num
        col = [i for i in col if i != _EMPTY]
        listPairs = [list(g) for k, g in groupby(col)]
        newCol = []
        for pair in listPairs:
            num = pair[0]
            for i in range(len(pair) // 2):
                newCol.append(num * 2)
            for i in range(len(pair) % 2):
                newCol.append(num)
        for empty in range(4 - len(newCol)):
            newCol.append(_EMPTY)
        for y, number in enumerate(newCol):
            point = (x, y)
            self._board[point] = number

    def _shift_col_down(self, col_num: int, col: [int]) -> None:
        """Shifts the specified block to the down."""
        x = col_num
        col = [i for i in col if i != _EMPTY]
        listPairs = [list(g) for k, g in groupby(col)]
        newCol = []
        for pair in listPairs[::-1]:
            num = pair[0]
            for i in range(len(pair) // 2):
                newCol.insert(0, num * 2)
            for i in range(len(pair) % 2):
                newCol.insert(0, num)
        for empty in range(4 - len(newCol)):
            newCol.insert(0, _EMPTY)
        for y, number in enumerate(newCol):
            point = (x, y)
            self._board[point] = number

    def _insert_random(self) -> None:
        """Inserts 2 or 4 in a random empty spot."""
        new_num = random.choice([2, 4])
        listEmpty = [x for x in self._board if self._board[x] == _EMPTY]
        if len(listEmpty) > 0:
            point = random.choice(listEmpty)
            self._board[point] = new_num

    def _game_over_check(self) -> None:
        """Checks for game over."""
        if 0 in list(self._board.values()):
            # if there are any empty spaces, game over isn't
            # raised.
            return None

        
        for x in range(_COLS):
            for y in range(_ROWS):
                curr_point = (x, y)
                curr_val = self._board[curr_point]
                listPoints = [
                    (x - 1, y), # left
                    (x + 1, y), # right
                    (x, y - 1), # above
                    (x, y + 1) # below
                ]
                for point in listPoints:
                    if point in self._board and \
                        self._board[point] == curr_val:
                        # Game over isn't raised if the values around it are
                        # equal to it. 
                        return None
        
        # if function isn't ended earlier, error is raised.
        raise GameOverError()

# functions
def _create_board() -> {Point, int}:
    """Creates an empty game board for 2048."""
    board = {}
    for x in range(_COLS):
            for y in range(_ROWS):
                point = (x, y)
                board[point] = _EMPTY
    return board
