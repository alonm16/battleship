import numpy as np
from Player import Player, in_bounds


class Human(Player):
    set1 = {5: 1, 4: 1, 3: 2, 2: 1}
    set2 = {4: 1, 3: 2, 2: 3, 1: 4}

    def __init__(self):
        super().__init__()

    def __legal(self, x, y, direction, battleship_size):
        if direction not in ['horizontal', 'vertical'] or not in_bounds((x, y)) or not 1 <= battleship_size <= 5:
            return False
        horizontal_offset = 1 if direction == 'horizontal' else 0
        vertical_offset = 1 if direction == 'vertical' else 0
        for i in range(battleship_size):
            if not (x + i * vertical_offset, y + i * horizontal_offset) in self.available_places:
                return False
        return True

    def place_battleships(self):
        while True:
            location = input("\nenter battleship point, direction and size: \n")
            if location.lower() == 'done':
                if self.battleships_set != Human.set1 and self.battleships_set != Human.set2:
                    self.battleships_set = {}
                    self.player_board = np.full((10, 10), ' ')
                    self.available_places = [(i, j) for i in range(10) for j in range(10)]
                    print("incorrect board placement, please try place all battleships again\n")
                    continue
                break
            try:
                start_point, direction, battleship_size = location.split()
                battleship_size = int(battleship_size)
                start_x, start_y = start_point.split(',')
                start_x, start_y = int(start_x), int(start_y)
            except:
                print('please enter valid parameters')
                continue

            if not self.__legal(start_x, start_y, direction, battleship_size):
                print("incorrect placement, please try  again")
                continue

            self._place_battleship(direction, start_x, start_y, battleship_size)
            self.battleships_set[battleship_size] = self.battleships_set.get(battleship_size, 0) + 1
            print(self.player_board)

    def turn(self, opponent: Player):
        while True:
            self.print_boards()
            try:
                location = input("\nEnter place to shoot: ").split(',')
                location = (int(location[0]), int(location[1]))
            except:
                print('please enter a valid location\n')
                continue
            if location not in self.opponent_available_places:
                print('location already chosen\n')
                continue
            self.opponent_available_places.remove(location)
            result = opponent.hit(location)
            if result == 'sank':
                print('ship sank!')
                self.opponent_board[location] = 'X'
            elif result == 'hit' or result == 'sank':
                self.opponent_board[location] = 'X'
                print('hit!\n')
                continue
            elif result == 'miss':
                self.opponent_board[location] = 'M'
                print('missed!\n')
            return result
