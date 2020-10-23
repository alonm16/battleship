import random
from Player import Player, in_bounds


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

    def hard_mode(self, x, y):
        if 0 < x < 9 and self.opponent_board[(x+1, y)] == 'X' and self.opponent_board[(x-1, y)] == ' ':
            return x-1, y
        elif 0 < x < 9 and self.opponent_board[(x-1, y)] == 'X' and self.opponent_board[(x+1, y)] == ' ':
            return x+1, y
        elif 0 < y < 9 and self.opponent_board[(x, y+1)] == 'X' and self.opponent_board[(x, y-1)] == ' ':
            return x, y-1
        elif 0 < y < 9 and self.opponent_board[(x, y-1)] == 'X' and self.opponent_board[(x, y+1)] == ' ':
            return x, y+1
        moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        moves = list(filter(lambda location: in_bounds(location) and location in self.opponent_available_places, moves))
        return random.choice(moves)

    def turn(self, opponent: Player):
        while True:
            if self.mode == 'hard' and self.last_hit != None:
                location = self.hard_mode(self.last_hit[0], self.last_hit[1])
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
            elif result == 'hit':
                self.last_hit = location
                self.opponent_board[location] = 'X'
                print('Opponent hit your battleship!\n')
                print(opponent.player_board)
            else:
                return result

