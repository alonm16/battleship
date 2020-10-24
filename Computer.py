import random
from Player import Player, in_bounds

BOARD_SIZE = 10


class Computer(Player):
    set1 = {5: 1, 4: 1, 3: 2, 2: 1}
    set2 = {4: 1, 3: 2, 2: 3, 1: 4}

    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.last_hit = None
        self.battleships_set = random.choice([Computer.set1, Computer.set2])
        self.total_possible_hits = sum([key*self.battleships_set[key] for key in self.battleships_set.keys()])

    def get_start_point(self, battleship_size, direction):
        """chooses a location for placing a battleship randomly"""
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
                self._place_battleship(direction, start_x, start_y, battleship_size)

    def hard_mode(self):
        x, y = self.last_hit[0], self.last_hit[1]
        """if game mode is hard, ensures that the computer will continue to shoot a battleship it hit previously"""
        horizontal = [self.opponent_board[location] for location in (filter(in_bounds, [(x, y+1), (x, y-1)]))]
        adjacent_x = x
        if 'X' not in horizontal:
            while adjacent_x < BOARD_SIZE-1 and self.opponent_board[adjacent_x, y] == 'X':
                adjacent_x += 1
            if self.opponent_board[adjacent_x, y] == ' ':
                return adjacent_x, y
            adjacent_x = x
            while adjacent_x > 0 and self.opponent_board[adjacent_x, y] == 'X':
                adjacent_x -= 1
            if self.opponent_board[adjacent_x, y] == ' ':
                return adjacent_x, y

        adjacent_y = y
        while adjacent_y < BOARD_SIZE-1 and self.opponent_board[x, adjacent_y] == 'X':
            adjacent_y += 1
        if self.opponent_board[x, adjacent_y] == ' ':
            return x, adjacent_y
        adjacent_y = y
        while adjacent_y > 0 and self.opponent_board[x, adjacent_y] == 'X':
            adjacent_y -= 1
        if self.opponent_board[x, adjacent_y] == ' ':
            return x, adjacent_y

    def turn(self, opponent: Player):
        while True:
            if self.mode == 'hard' and self.last_hit:
                location = self.hard_mode()
            else:
                location = random.choice(self.opponent_available_places)
            self.opponent_available_places.remove(location)
            result = opponent.hit(location)
            if result == 'miss':
                self.opponent_board[location] = 'M'
                print('Opponent missed!\n')
                return result
            elif result == 'sank':
                self.last_hit = None
                self.opponent_board[location] = 'X'
                print('Opponent sank your battleship!\n')
                print(opponent.player_board)
            elif result == 'hit':
                self.last_hit = location
                self.opponent_board[location] = 'X'
                print('Opponent hit your battleship!\n')
                print(opponent.player_board)
            else:
                return result
