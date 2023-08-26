from board import Board
from blue import Blue
from yellow import Yellow
from game import Game
from rainet import Rainet

# game init
board = Board()
blue = Blue()
yellow = Yellow()
game = Game()

# team init
blue_init = ['L', 'L', 'V', 'V', 'V', 'V', 'L', 'L']
blue.team_init(blue_init)

yellow_init = ['l', 'l', 'v', 'v', 'v', 'v', 'l', 'l']
yellow.team_init(yellow_init)

# move test
# board.print_all_board()
# game.move_piece('a1', 'a2')
# board.print_all_board()
# result -> success