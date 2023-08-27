from board import Board
from blue import Blue
from yellow import Yellow
from game import Game
from rainet import Rainet

# game init
board = Board()
# blue = Blue()
# yellow = Yellow()
game = Game()

# team init
# blue_init = ['L', 'L', 'V', 'V', 'V', 'V', 'L', 'L']
# blue.team_init(blue_init)

# yellow_init = ['l', 'l', 'v', 'v', 'v', 'v', 'l', 'l']
# yellow.team_init(yellow_init)

# move test
# board.print_all_board()
# game.move_piece('a1', 'a2')
# board.print_all_board()
# result -> success

# 障碍物的位置
FW_place = []
# 起始位置
position = 'a1'
# 移动次数上限
step = 2
# 己方棋子的位置
friend_pieces = []
# 敌方棋子的位置
enemy_pieces = []
# 开始搜索
game.dfs(position, FW_place, friend_pieces, enemy_pieces, step)

# 打印所有路径
for path in game.all_paths:
	print(path)
 # graphic results
	for i in range(len(path)):
		alg = path[i]
		board.god_board[alg] = str(i)
		board.blue_board[alg] = str(i)
		board.yellow_board[alg] = str(i)
	board.print_all_board()
	for i in range(len(path)):
		alg = path[i]
		board.god_board[alg] = '-'
		board.blue_board[alg] = '-'
		board.yellow_board[alg] = '-'
 
start_position = 'a1'
end_position = 'a2'

valid_move = game.is_start_and_end_in_paths(start_position, end_position, game.all_paths)
print(valid_move)