# game_ui.py
# Akhil Dhanala


"""
Module that implements the user interface behind 2048
using pygame.
"""


# imports
import pygame
import gamelogic
import typing


# type annotations
Size = typing.Tuple[int, int]
Point = typing.Tuple[int, int]


# constants
_DEBUG = False
X = 0
Y = 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (169, 169, 169)
LIGHT_GREY  = (211, 211, 211)


# class
class GameHandler(object):
    """Object to handle the game logic."""

    _FRAME_RATE = 7
    _INITIAL_SIZE = (600, 600)
    _NUMBERS = {}
    for power in range(1, 12):
        n = 2 ** power
        exec(f"_NUMBERS[{n}] = pygame.image.load('{n}.png')")
    
    def __init__(self) -> None:
        """Initializes the game handler object."""
        self._state = gamelogic.GameLogic()
        self._running = True
        self._white_space = pygame.image.load("white_space.png")
        self._frame_count = 0
    
    # methods
    def run(self) -> None:
        """Runs the game."""
        try:
            pygame.init()
            clock = pygame.time.Clock()
            self._initialize_display()
            while self._running:
                clock.tick(self._FRAME_RATE)
                self._draw_frame()
                self._handle_events()
                if _DEBUG and self._frame_count % self._FRAME_RATE == 0:
                    self._print_board()
                self._frame_count += 1
        finally:
            pygame.quit()
    
    def _print_board(self) -> None:
        """Prints board for debugging purposes."""
        for row in self._state.get_board("LIST"):
            print(row)
        print()
    
    def _initialize_display(self) -> None:
        """Initializes the display."""
        logo = pygame.image.load("2048.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("2048")
        self._resize_surface(self._INITIAL_SIZE)

    def _draw_frame(self) -> None:
        """Draw frame."""
        self._surface.fill((255, 215, 94))
        self._draw_nums()
        pygame.display.flip()
    
    def _draw_nums(self) -> None:
        """Draws the numbers from the board."""
        self._draw_gameboard()

        board = self._state.get_board("LIST")
        for y, row in enumerate(board):
            for x, num in enumerate(row):
                point = (x, y)
                self._draw_num(num, point)
        
        self._surface.blit(
            self._game_board_scaled,
            (self._board_x, self._board_y)
        )
    
    def _draw_gameboard(self) -> None:
        """Draws the gameboard."""
        display_width = self._surface.get_width()
        display_height = self._surface.get_height()
        self._board_width = int(((display_width * 0.9) // 4) * 4) 
        self._board_height = int(((display_height * 0.9) // 4) * 4)
        self._num_width = (self._board_width / 4) * 0.9
        self._num_height = (self._board_height / 4) * 0.9

        self._game_board_scaled = pygame.transform.scale(
            self._white_space, (self._board_width, self._board_height)
        )

        self._board_x = int(display_width * 0.05)
        self._board_y = int(display_height * 0.05)
        self._game_board_scaled.fill(GREY)

    def _draw_num(self, num: int, point: Point) -> None:
        """Draws the number on the number using the coordinate."""
        x_space = (self._board_width - (self._num_width * 4)) / 5
        y_space = (self._board_height - (self._num_height * 4)) / 5
        x = (self._num_width * point[X]) + x_space + (x_space * (point[X]))
        y = (self._num_height * point[Y]) + y_space + (y_space * (point[Y]))
        if num == 0:
            pygame.draw.rect(
                self._game_board_scaled, 
                LIGHT_GREY,
                pygame.Rect(
                    (x, y),
                    (self._num_width, self._num_height)
                )
            )
        else:
            number = self._NUMBERS[num]
            number_scaled = pygame.transform.scale(
                number, (int(self._num_width), int(self._num_height))
            )
            self._game_board_scaled.blit(
                number_scaled, (x, y)
            )

    def _resize_surface(self, size: Size) -> None:
        """Resizes the surface."""
        self._surface = pygame.display.set_mode(
            size,
            pygame.RESIZABLE
        )

    def _handle_events(self) -> None:
        """Handles the user events in the game."""
        for event in pygame.event.get():
            self._handle_event(event)
        self._handle_keys()
    
    def _handle_event(self, event: "pygame event") -> None:
        """Handles a single event in the game."""
        if event.type == pygame.QUIT:
                self._end_game()
        elif event.type == pygame.VIDEORESIZE:
            self._resize_surface(event.size)

    def _handle_keys(self) -> None:
        """Handles the keys pressed in the game."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self._state.shift_left()
        if keys[pygame.K_RIGHT]:
            self._state.shift_right()
        if keys[pygame.K_DOWN]:
            self._state.shift_down()
        if keys[pygame.K_UP]:
            self._state.shift_up()
    
    def _end_game(self) -> None:
        """Ends the game."""
        self._running = False


if __name__ == "__main__":
    GameHandler().run()
