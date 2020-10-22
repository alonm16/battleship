import numpy as np
import random
from Player import Player


class Computer(Player):
    set1 = {5: 1, 4: 1, 3: 2, 2: 1}
    set2 = {4: 1, 3: 2, 2: 3, 1: 4}

    def __init__(self):
        super().__init__()
        self.battleships_set = random.choice([Computer.set1, Computer.set2])

    def get_start_point(self, battleship_size, direction):
        problem = True
        horizontal_offset = 1 if direction == 'horizontal' else 0
        vertical_offset = 1 if direction == 'vertical' else 0
        start_x, start_y = None, None
        while problem:
            problem = False
            start_x, start_y = random.choice(self.available_places)
            for i in range(battleship_size):
                if not (start_x + i * vertical_offset, start_y + i * horizontal_offset) in self.available_places:
                    problem = True
        return start_x, start_y

    def place_battleships(self):
        for battleship_size in self.battleships_set.keys():
            while self.battleships_set[battleship_size] > 0:
                self.battleships_set[battleship_size] -= 1
                direction = random.choice(['vertical', 'horizontal'])
                start_x, start_y = self.get_start_point(battleship_size, direction)
                self.place_battleship(direction, start_x, start_y, battleship_size)
        print(self.player_board)
