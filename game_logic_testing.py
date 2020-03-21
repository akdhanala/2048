# game_logic_testing.py
# Akhil Dhanala

"""
Executable module for testing gamelogic in terminal.
"""

# imports
import gamelogic


# functions
def _print_board(board: list):
    """Prints the board."""
    for row in board:
        print("|", end="")
        for point in row:
            print(f" {point} ", end="")
        print("|")
    
    partial_tail = 12 * "-"
    print(f" {partial_tail} ")


def _exec_action(game: gamelogic.GameLogic) -> gamelogic.GameLogic:
    """Executes a user inputted action."""
    # Action choices:
    #   - "<" is shift left
    #   - ">" is shift right
    #   - "^" is shift up
    #   - "v" is shift down
    actions = {
        "<": game.shift_left,
        ">": game.shift_right,
        "^": game.shift_up,
        "v": game.shift_down,
        "Q": game.quit_game
    }
    a = input()
    if a in actions:
        action = actions[a]
        action()
    return game

def run() -> None:
    """Runs 2048 in terminal."""
    game = gamelogic.GameLogic()
    running = True
    while running:
        _print_board(game.get_board("LIST"))
        try:
            game = _exec_action(game)
        except gamelogic.GameOverError:
            print("Game Over!")
            running = False

if __name__ == "__main__":
    run()