# Author: <Pinzhi Huang>
# Assignment #6 - Battleship
# Date due: 2021-12-09
# I pledge that I have completed this assignment without
# collaborating with anyone else, in conformance with the
# NYU School of Engineering Policies and Procedures on
# Academic Misconduct.

import random

### DO NOT EDIT BELOW (with the exception of MAX_MISSES) ###

HIT_CHAR = 'x'
MISS_CHAR = 'o'
BLANK_CHAR = '.'
HORIZONTAL = 'h'
VERTICAL = 'v'
MAX_MISSES = 20
SHIP_SIZES = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}
NUM_ROWS = 10
NUM_COLS = 10
ROW_IDX = 0
COL_IDX = 1
MIN_ROW_LABEL = 'A'
MAX_ROW_LABEL = 'J'


def get_random_position():
    """Generates a random location on a board of NUM_ROWS x NUM_COLS."""

    row_choice = chr(
                    random.choice(
                        range(
                            ord(MIN_ROW_LABEL),
                            ord(MIN_ROW_LABEL) + NUM_ROWS
                        )
                    )
    )

    col_choice = random.randint(0, NUM_COLS - 1)

    return (row_choice, col_choice)


def play_battleship():
    """Controls flow of Battleship games including display of
    welcome and goodbye messages.

    :return: None
    """

    print("Let's Play Battleship!\n")

    game_over = False

    while not game_over:

        game = Game()
        game.display_board()

        while not game.is_complete():
            pos = game.get_guess()
            result = game.check_guess(pos)
            game.update_game(result, pos)
            game.display_board()

        game_over = end_program()

    print("Goodbye.")

### DO NOT EDIT ABOVE (with the exception of MAX_MISSES) ###


class Ship:

    def __init__(self, name, start_position, orientation):
        """Creates a new ship with the given name, placed at start_position in the
        provided orientation. The number of positions occupied by the ship is determined
        by looking up the name in the SHIP_SIZE dictionary.
        :param name: the name of the ship
        :param start_position: tuple representing the starting position of ship on the board
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return: None
        """
        self.name = name
        self.positions = {}
        self.sunk = False

        if orientation == VERTICAL:
            for i in range(SHIP_SIZES[self.name]):
                self.positions[(chr(ord(start_position[0])+i)), start_position[1]] = False
        else:
            for i in range(SHIP_SIZES[self.name]):
                self.positions[(start_position[0],start_position[1]+i)] = False



class Game:

    ########## DO NOT EDIT #########
    
    _ship_types = ["carrier", "battleship", "cruiser", "submarine", "destroyer"]

    def __init__(self, max_misses=MAX_MISSES):
        """ Creates a new game with max_misses possible missed guesses.
        The board is initialized in this function and ships are randomly
        placed on the board.
        :param max_misses: maximum number of misses allowed before game ends
        """
        self.board = {}
        self.max_misses = max_misses
        self.guesses = []
        self.ships = []
        self.initialize_board()
        self.create_and_place_ships()



    def initialize_board(self):
        """Sets the board to it's initial state with each position occupied by
        a period ('.') string.
        :return: None
        """
        for i in range(NUM_COLS):
            row = chr(ord(MIN_ROW_LABEL)+i)
            lst = []
            for k in range(NUM_ROWS):
                lst.append(".")
            self.board[row] = lst

    def in_bounds(self, start_position, ship_size, orientation):
        """Checks that a ship requiring ship_size positions can be placed at start position.
        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return status: True if ship placement inside board boundary, False otherwise
    """
        if orientation == HORIZONTAL:
            if start_position[1]+ship_size <= NUM_ROWS:
                return True
            else:
                return False
        elif orientation == VERTICAL:
            if chr(ord(start_position[0])+ship_size) <= MAX_ROW_LABEL:
                return True
            else:
                return False


    def overlaps_ship(self, start_position, ship_size, orientation):
        """Checks for overlap between previously placed ships and a potential new ship
        placement requiring ship_size positions beginning at start_position in the
        given orientation.
        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return status: True if ship placement overlaps previously placed ship, False otherwise
        """

        lst1=[]
        if orientation == HORIZONTAL:
            for i in range(ship_size):
                lst1.append((start_position[0],start_position[1]+i))
        elif orientation == VERTICAL:
            for i in range(ship_size):
                lst1.append((chr(ord(start_position[0])+i),start_position[1]))
        for ship in self.ships:
            for pos in ship.positions:
                if pos in lst1:
                    return True
        return False

    def place_ship(self, start_position, ship_size):
        """Determines if placement is possible for ship requiring ship_size positions placed at
        start_position. Returns the orientation where placement is possible or None if no placement
        in either orientation is possible.
        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :return orientation: 'h' if horizontal placement possible, 'v' if vertical placement possible,
            None if no placement possible
        """
        if self.in_bounds(start_position, ship_size, HORIZONTAL):
            if not self.overlaps_ship(start_position, ship_size,HORIZONTAL):
                return "h"
        if self.in_bounds(start_position, ship_size, VERTICAL):
            if not self.overlaps_ship(start_position, ship_size, VERTICAL):
                return "v"
        return None

    def create_and_place_ships(self):
        """Instantiates ship objects with valid board placements.
        :return: None
        """
        _ship_types = ["carrier", "battleship", "cruiser", "submarine", "destroyer"]
        for i in _ship_types:
            position = get_random_position()
            orientation = self.place_ship(position, SHIP_SIZES[i])
            while not orientation == VERTICAL and not orientation == HORIZONTAL:
                position = get_random_position()
                orientation = self.place_ship(position, SHIP_SIZES[i])
            battleship = Ship(i,position,orientation)
            self.ships.append(battleship)

    def get_guess(self):
        """Prompts the user for a row and column to attack. The
        return value is a board position in (row, column) format
        :return position: a board position as a (row, column) tuple
        """
        get_row = input("Enter a row: ")
        while not ord(MIN_ROW_LABEL)-1 < ord(get_row) < ord(MAX_ROW_LABEL)+1:
            get_row = input("Enter a row: ")
        get_column = int(input("Enter a column: "))
        while not ROW_IDX <= int(get_column) < NUM_COLS:
            get_column = input("Enter a column: ")
        return (get_row,int(get_column))




    def check_guess(self, position):
        """Checks whether or not position is occupied by a ship. A hit is
        registered when position occupied by a ship and position not hit
        previously. A miss occurs otherwise.
        :param position: a (row,column) tuple guessed by user
        :return: guess_status: True when guess results in hit, False when guess results in miss
        """
        for i in self.ships:
            if position in i.positions and not i.positions[position]:
                i.positions[position] = True
                if all(i.positions.values()):
                    i.sunk = True
                    print("You sunk the {}!".format(i.name))
                return True
        return False


    def update_game(self, guess_status, position):
        """Updates the game by modifying the board with a hit or miss
        symbol based on guess_status of position.
        :param guess_status: True when position is a hit, False otherwise
        :param position:  a (row,column) tuple guessed by user
        :return: None
        """
        if guess_status:
            self.board[position[0]][position[1]] = HIT_CHAR
        else:
            if self.board[position[0]][position[1]] != HIT_CHAR:
                self.board[position[0]][position[1]] = MISS_CHAR
            self.guesses.append(position)

    def is_complete(self):
        """Checks to see if a Battleship game has ended. Returns True when the game is complete
        with a message indicating whether the game ended due to successfully sinking all ships
        or reaching the maximum number of guesses. Returns False when the game is not
        complete.
        :return: True on game completion, False otherwise
        """
        temp = 0
        for i in self.ships:
            if not i.sunk:
                temp += 1
        if len(self.guesses) < MAX_MISSES:
            if temp == 0:
                print("YOU WIN!")
                return True
            else:
                return False
        else:
            print("SORRY! NO GUESSES LEFT.")
            return True




    def display_board(self):
        """ Displays the current state of the board."""
        print()
        print("  " + ' '.join('{}'.format(i) for i in range(len(self.board))))
        for row_label in self.board.keys():
            print('{} '.format(row_label) + ' '.join(self.board[row_label]))
        print()




    ########## DO NOT EDIT #########


def end_program():
    """Prompts the user with "Play again (Y/N)?" The question is repeated
    until the user enters a valid response (Y/y/N/n). The function returns
    False if the user enters 'Y' or 'y' and returns True if the user enters
    'N' or 'n'.
    :return response: boolean indicating whether to end the program
    """
    again = input("Play again (Y/N)?")
    while again != "Y" and again != "y" and again != "N" and again != "n":
        again = input("Play again (Y/N)?")
    if again == "Y" or again == "y":
        return False
    else:
        return True


def main():
    """Executes one or more games of Battleship."""
    play_battleship()


if __name__ == "__main__":
    main()
