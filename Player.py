import numpy as np
from abc import ABC, abstractmethod


class Player(ABC):
    set1 = {5: 1, 4: 1, 3: 2, 2: 1}
    set2 = {4: 1, 3: 2, 2: 3, 1: 4}

    def __init__(self):
        self.player_board = np.zeros((10, 10), dtype=int)
        self.opponent_board = np.zeros((10, 10), dtype=int)
        self.battleships_set = {}
        self.available_places = [(i, j) for i in range(10) for j in range(10)]

    def remove(self, x, y):
        try:
            self.available_places.remove((x, y))
        except:
            pass

    def remove_horizontal(self, x, start_y, size):
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

    def place_battleship(self, direction, start_x, start_y, battleship_size):
        if direction == 'horizontal':
            for y in range(start_y, start_y + battleship_size):
                self.player_board[start_x, y] = 1
            self.remove_horizontal(start_x, start_y, battleship_size)

        else:
            for x in range(start_x, start_x + battleship_size):
                self.player_board[x, start_y] = 1
            self.remove_vertical(start_x, start_y, battleship_size)

    @abstractmethod
    def place_battleships(self):
        pass
