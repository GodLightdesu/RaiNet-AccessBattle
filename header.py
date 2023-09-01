from human import Blue
from ai import Yellow
from board import Board
from game import Game

class Header:
  def __init__(self):
    self.blue = Blue()
    self.yellow = Yellow()
    self.board = Board()
    self.game = Game()