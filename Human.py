import numpy as np
from Player import Player, in_bounds
import socket

FORMAT = 'utf-8'
BOARD_SIZE = 10


class Human(Player):
    set1 = {5: 1, 4: 1, 3: 2, 2: 1}
    set2 = {4: 1, 3: 2, 2: 3, 1: 4}

    def __init__(self, conn: socket.socket = None):
        super().__init__()
        self.conn = conn
        if conn:
            self.input = self.__socket_input
            self.output = self.__socket_output
        else:
            self.input = self.__normal_input
            self.output = self.__normal_output

    def __normal_output(self, msg):
        print(msg)

    def __normal_input(self, msg):
        return input(msg)

    def __socket_output(self, msg):
        self.conn.send(bytes('0' + msg, FORMAT))

    def __socket_input(self, msg):
        self.conn.send(bytes('1' + msg, FORMAT))
        return self.conn.recv(128).decode(FORMAT)

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
            location = self.input("\nenter battleship point, direction and size: \n")
            if location.lower() == 'done':
                if self.battleships_set != Human.set1 and self.battleships_set != Human.set2:
                    self.battleships_set = {}
                    self.player_board = np.full((BOARD_SIZE, BOARD_SIZE), ' ')
                    self.available_places = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
                    self.output("incorrect board placement, please try place all battleships again\n")
                    continue
                break
            try:
                start_point, direction, battleship_size = location.split()
                battleship_size = int(battleship_size)
                start_x, start_y = start_point.split(',')
                start_x, start_y = int(start_x), int(start_y)
            except:
                self.output('please enter valid parameters')
                continue

            if not self.__legal(start_x, start_y, direction, battleship_size):
                self.output("incorrect placement, please try  again")
                continue

            self._place_battleship(direction, start_x, start_y, battleship_size)
            self.battleships_set[battleship_size] = self.battleships_set.get(battleship_size, 0) + 1
            self.output('\n' + str(self.player_board))
            if self.battleships_set == Human.set1 or self.battleships_set == Human.set2:
                return

    def print_boards(self):
        boards = 'player board:' + '\t' * 10 + 'opponent board:' + '\n'
        for r1, r2 in zip(self.player_board, self.opponent_board):
            boards += str(r1) + 3*'\t' + str(r2) + '\n'
        self.output(boards)

    def turn(self, opponent: Player):
        while True:
            self.print_boards()
            try:
                location = self.input("\nEnter place to shoot: ").split(',')
                location = (int(location[0]), int(location[1]))
            except:
                self.output('please enter a valid location\n')
                continue
            if location not in self.opponent_available_places:
                self.output('location already chosen\n')
                continue
            self.opponent_available_places.remove(location)
            result = opponent.hit(location)
            if result == 'sank':
                self.output('ship sank!')
                self.opponent_board[location] = 'X'
                opponent.output('Opponent hit your battleship!\n\n' + str(opponent.player_board)) \
                    if isinstance(opponent, Human) else None
                continue
            elif result == 'hit':
                self.opponent_board[location] = 'X'
                self.output('hit!\n')
                opponent.output('Opponent hit your battleship!\n\n' + str(opponent.player_board)) \
                    if isinstance(opponent, Human) else None
                continue
            elif result == 'miss':
                self.opponent_board[location] = 'M'
                self.output('missed!\n')
                opponent.output('Opponent missed!\n') if isinstance(opponent, Human) else None
            return result
