import numpy as np
from Player import Player


class Human(Player):
    set1 = {5: 1, 4: 1, 3: 2, 2: 1}
    set2 = {4: 1, 3: 2, 2: 3, 1: 4}

    def __init__(self):
        super().__init__()

    def __legal(self, location, direction, battleship_size):
        x, y = int(location[0]), int(location[1])
        if direction not in ['horizontal', 'vertical'] or not 0 <= x < 10 or not 0 <= y < 10 \
                or not 1 <= battleship_size <= 5:
            return False
        horizontal_offset = 1 if direction == 'horizontal' else 0
        vertical_offset = 1 if direction == 'vertical' else 0
        for i in range(battleship_size):
            if not (x + i * vertical_offset, y + i * horizontal_offset) in self.available_places:
                return False
        return True

    def place_battleships(self):
        while True:
            location = input("\nenter battleship point, direction and size: ")
            if location.lower() == 'done':
                if self.battleships_set != Human.set1 and self.battleships_set != Human.set2:
                    self.battleships_set = {}
                    self.player_board = np.zeros((10, 10), dtype=int)
                    print("incorrect board placement, please try place all battleships again\n")
                    continue
                break
            start_point, direction, battleship_size = location.split()
            start_x, start_y = start_point.split(',')
            battleship_size = int(battleship_size)
            if not self.__legal(start_point, direction, battleship_size):
                print("incorrect placement, please try  again\n")
                continue

            self.place_battleship(direction, start_x, start_y, battleship_size)
            self.battleships_set[battleship_size] = self.battleships_set.get(battleship_size, 0) + 1
            print(self.player_board)
