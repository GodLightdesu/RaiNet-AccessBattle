from board import Board

# action logic
class Game: 
  directions_label = ['F', 'R', 'B', 'L']
  
  def select_piece(self, where):
    # [god, human, ai]
    selected_piece = [Board().god_board[where], Board().human_board[where], Board().ai_board[where]]
    return selected_piece
  
  def get_possible_moves(self, position):
    # F, R, B, L
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    moves = []
    for dx, dy in directions:
      file = chr(ord(position[0]) + dx)
      rank = int(position[1]) + dy
      new_position = file + str(rank)
      # if self.is_valid_move(new_position, FW_place, friend_pieces, enemy_pieces):
      moves.append(new_position)
    return moves # [F, R, B, L]

  def generate_move(self, start):
    moves = self.get_possible_moves(start)
    possible_moves = {
      'F': moves[0],
      'R': moves[1],
      'B': moves[2],
      'L': moves[3] 
    }
    return possible_moves

  def move_piece(self, start_square, end_square):
    print('move from: ' + start_square + ' to ' + end_square)
    # select the piece
    piece = self.select_piece(start_square)
    # move piece
    Board().update_all_board(start_square, '-')
    Board().god_board[end_square] = piece[0]
    Board().human_board[end_square] = piece[1]
    Board().ai_board[end_square] = piece[2]
      
      
  def is_valid_move(self, position, FW_place, friend_pieces, exit_pos):
    # 检查移动是否在棋盘范围内
    file, rank = position[0], int(position[1])
    if file < 'a' or file > 'h' or rank < 0 or rank > 9:
      return False
    # 检查移动是否为障碍物
    elif (FW_place is not None and position in FW_place):
      return False
    elif position in Board().BOUNDARY_POS:
      return False
    elif position in exit_pos:
      return False
    # 检查移动是否为己方棋子
    elif position in friend_pieces:
      return False
    else:
      return True


  def find_valid_paths(self, start_pos, num_moves, FW_place, friend_pieces, exit_pos):
    # 定义可移动的方向
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    valid_paths = []  # 用于存储合法路径的列表

    def dfs(path, pos, moves_left):
      if moves_left == 0:
        # 将找到的合法路径添加到列表中
        valid_paths.append(path)
        return
        
      for dx, dy in directions:
        file = chr(ord(pos[0]) + dx)
        rank = int(pos[1]) + dy
        next_pos = file + str(rank)
        # 递归调用DFS，继续搜索下一个位置
        if self.is_valid_move(next_pos, FW_place, friend_pieces, exit_pos) == True:
          dfs(path + [next_pos], next_pos, moves_left - 1)

    # 调用DFS函数，从起始位置开始搜索
    dfs([start_pos], start_pos, num_moves)
    
    return valid_paths
  
  def print_all_paths(self, paths):
    '''
    # 示例调用
    start_position = "c5"  # 起始位置
    num_moves = 2  # 可移动的次数
    paths = find_valid_paths(start_position, num_moves)
    '''
    # 打印找到的合法路径
    for path in paths:
      print(" -> ".join(path))
    
  def all_valid_moves(self, paths):
    '''
    # 示例调用
    start_position = "c5"  # 起始位置
    num_moves = 2  # 可移动的次数
    paths = find_valid_paths(start_position, num_moves)
    '''
    # 存储所有位置的集合
    positions = set()

    # 将找到的合法路径中的位置添加到集合中
    for path in paths:
      positions.update(path)
    valid_moves = list(positions)
    return valid_moves
  
  def is_start_and_end_in_paths(self, all_paths, start_position, end_position):
    for path in all_paths:
      # print(path, all_paths)
      if start_position in path and end_position in path:
        return True #valid move
    return False