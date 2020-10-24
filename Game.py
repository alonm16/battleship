from Human import Human
from Computer import Computer
import socket
import numpy

FORMAT = 'utf-8'


class Game:
    def __init__(self):
        self.player0 = Human()
        self.player1 = None

    def play(self):
        mode = input('Choose game mode (easy/hard): ').lower()
        while mode not in ['easy', 'hard']:
            mode = input('please enter a valid input: ')
        self.player1 = Computer(mode)

        self.player0.place_battleships()
        self.player1.place_battleships()
        while True:
            result = self.player0.turn(self.player1)
            if result == 'win':
                print('player 0 has won!')
                return

            result = self.player1.turn(self.player0)
            if result == 'win':
                print('player 1 has won!')
                return

    def multiplayer(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(), 1234))
        server.listen(1)
        conn, addr = server.accept()
        self.player1 = Human()

        conn.send(bytes('1' + 'hello', FORMAT))
        conn.send(bytes('0' + 'hello', FORMAT))


