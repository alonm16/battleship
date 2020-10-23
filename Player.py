import numpy as np
from abc import ABC, abstractmethod


def in_bounds(location):
    x, y = location[0], location[1]
    return 0 <= x < 10 and 0 <= y < 10


class Player(ABC):

    def __init__(self):
        self.player_board = np.full((10, 10), ' ')
        self.opponent_board = np.full((10, 10), ' ')
        self.opponent_available_places = [(i, j) for i in range(10) for j in range(10)]
        self.battleships_set = {}
        self.available_places = [(i, j) for i in range(10) for j in range(10)]
        self.total_possible_hits = 0

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

    def _place_battleship(self, direction, start_x, start_y, battleship_size):
        if direction == 'horizontal':
            for y in range(start_y, start_y + battleship_size):
                self.player_board[start_x, y] = 'S'
            self.remove_horizontal(start_x, start_y, battleship_size)

        else:
            for x in range(start_x, start_x + battleship_size):
                self.player_board[x, start_y] = 'S'
            self.remove_vertical(start_x, start_y, battleship_size)

    @abstractmethod
    def place_battleships(self):
        pass

    @abstractmethod
    def turn(self, opponent):
        pass

    def check_drowned(self, x, y):
        adjacent = [(x-1, y), (x-1, y-1), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y), (x+1, y-1), (x+1, y+1)]
        adjacent = list(filter(in_bounds, adjacent))
        return all(self.player_board[location] != 'S' for location in adjacent)

    def hit(self, location):
        if self.player_board[location] == 'S':
            self.player_board[location] = 'X'
            self.total_possible_hits -= 1
            if self.check_drowned(location[0], location[1]):
                print('ship was drowned!')
            return 'win' if self.total_possible_hits == 0 else 'hit'
        return 'miss'

    def print_boards(self):
        print('player board:' + '\t' * 10 + 'opponent board:')
        for r1, r2 in zip(self.player_board, self.opponent_board):
            print(r1, end='\t' * 3)
            print(r2)
