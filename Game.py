from Human import Human
from Computer import Computer


class Game:
    def __init__(self):
        self.player0 = Human()
        self.player1 = Computer()

    def play(self):
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
