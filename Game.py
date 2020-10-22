from Human import Human
from Computer import Computer
from Player import Player


class Game:
    def __init__(self):
        self.player0 = Human()
        self.player1 = Computer()
        self.turn = 0
        self.player1.place_battleships()
