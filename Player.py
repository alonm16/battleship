import numpy as np
from abc import ABC, abstractmethod

BOARD_SIZE = 10


def in_bounds(location):
    """
    checks whether the location is in bounds of the board
    :param location: location on the board chosen by player
    :return: Boolean according to the location being in the bounds
    """
    x, y = location[0], location[1]
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE


class Player(ABC):

    def __init__(self):
        """
        player_board: the board of the player
        opponent_board: board that represents the knowledge of the current player on the opponents board
        available_places: places where the player can place his battleships
        opponent_available_places: places left to attack the opponent
        """
        self.player_board = np.full((BOARD_SIZE, BOARD_SIZE), ' ')
        self.opponent_board = np.full((BOARD_SIZE, BOARD_SIZE), ' ')
        self.opponent_available_places = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
        self.battleships_set = {}
        self.available_places = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
        self.total_possible_hits = 0
        self.ships_position = []

    def remove(self, x, y):
        try:
            self.available_places.remove((x, y))
        except:
            pass

    def remove_horizontal(self, x, start_y, size):
        """
        removes places that are not available anymore to place another battleships after a ship was placed horizontally
        :param x: row of the battleship
        :param start_y: most left y value for the ship
        :param size: size of the battleship
        """
        self.remove(x, start_y-1)
        self.remove(x-1, start_y-1)
        self.remove(x+1, start_y-1)
        self.remove(x, start_y + size)
        self.remove(x - 1, start_y + size)
        self.remove(x + 1, start_y + size)
        for y in range(start_y, start_y + size):
            self.remove(x, y)
            self.remove(x-1, y)
            self.remove(x+1, y)

    def remove_vertical(self, start_x, y, size):
        self.remove(start_x-1, y)
        self.remove(start_x - 1, y - 1)
        self.remove(start_x - 1, y + 1)
        self.remove(start_x + size, y)
        self.remove(start_x + size, y-1)
        self.remove(start_x + size, y + 1)
        for x in range(start_x, start_x + size):
            self.remove(x, y)
            self.remove(x, y+1)
            self.remove(x, y-1)

    def _place_battleship(self, direction, start_x, start_y, battleship_size):
        """
        placing battleship on the board
        :param direction: horizontal/vertical
        :param start_x: most left x value
        :param start_y: most upper y value
        :param battleship_size: size of battleship
        """
        battleship_location = []
        if direction == 'horizontal':
            for y in range(start_y, start_y + battleship_size):
                self.player_board[start_x, y] = 'S'
                battleship_location.append((start_x, y))
            self.remove_horizontal(start_x, start_y, battleship_size)

        else:
            for x in range(start_x, start_x + battleship_size):
                self.player_board[x, start_y] = 'S'
                battleship_location.append((x, start_y))
            self.remove_vertical(start_x, start_y, battleship_size)
        self.ships_position.append(battleship_location)

    @abstractmethod
    def place_battleships(self):
        """
        receives all battleships places from player
        """
        pass

    @abstractmethod
    def turn(self, opponent):
        """
        executes the turn of the player
        :param opponent: the opponent player object, for updating its board and knowing if the current player hit him
        """
        pass

    def check_drowned(self, location):
        for ship_position in self.ships_position:
            if location in ship_position:
                return all(self.player_board[pos] == 'X' for pos in ship_position)
        return False

    def hit(self, location):
        """
        checks if the opponent hit the player
        :param location: location to hit ship
        :return: 'win' - all battleships sank
                 'hit' if ship was hit but not sank
                 'miss' no ship was hit
        """
        if self.player_board[location] == 'S':
            self.player_board[location] = 'X'
            self.total_possible_hits -= 1
            if self.check_drowned(location):
                return 'win' if self.total_possible_hits == 0 else 'sank'
            return 'win' if self.total_possible_hits == 0 else 'hit'
        return 'miss'
