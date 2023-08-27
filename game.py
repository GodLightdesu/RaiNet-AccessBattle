from board import Board

# action logic
class Game: 
  # 记录已访问的位置
  visited = set()
  # 记录路径
  path = []
  # 记录所有路径
  all_paths = []
   
  def __init__(self):
    pass
  
  def select_piece(self, where):
    # [god, blue, yellow]
    selected_piece = [Board().god_board[where], Board().blue_board[where], Board().yellow_board[where]]
    return selected_piece
  
  def move_piece(self, start_square, end_square):
    print('move from: ' + start_square + ' to: ' + end_square)
    # select the piece
    piece = self.select_piece(start_square)
    # move piece
    Board().update_board(start_square, '-')
    for i in range(3):
      Board().update_board(end_square, piece[i])
      
  def check_blocked(self):
    pass
      
  def is_valid_move(self, position, FW_place, friend_pieces, enemy_pieces):
    # 检查移动是否在棋盘范围内
    file, rank = position[0], int(position[1])
    if file < 'a' or file > 'h' or rank < 0 or rank >= 9:
      return False
    # 检查移动是否为障碍物
    if (FW_place is not None and position in FW_place) or position in Board().BOUNDARY_POS:
      return False
    # 检查移动是否已经访问过
    if position in self.visited:
      return False
    # 检查移动是否为己方棋子
    if position in friend_pieces:
      return False
    # 检查移动是否为敌方棋子
    if position in enemy_pieces:
      # 取代敌方棋子的位置
      # enemy_pieces.remove(position)
      return False
    return True
  
  def dfs(self, position, FW_place, friend_pieces, enemy_pieces, step):
    # 将当前位置标记为已访问
    self.visited.add(position)
    # 添加当前位置到路径
    self.path.append(position)
    
    # 判断是否达到移动次数上限
    if len(self.path) == step + 1:
      # 将路径添加到所有路径列表中
      self.all_paths.append(self.path.copy())
    else:
      # 遍历所有可能的移动方向
      directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
      for dx, dy in directions:
        file = chr(ord(position[0]) + dx)
        rank = int(position[1]) + dy
        new_position = file + str(rank)
        if self.is_valid_move(new_position, FW_place, friend_pieces, enemy_pieces):
          self.dfs(new_position, FW_place, friend_pieces, enemy_pieces, step)
    
    # 回溯，将当前位置标记为未访问并从路径中移除
    self.visited.remove(position)
    self.path.pop()
  
  def is_start_and_end_in_paths(self, start_position, end_position, all_paths):
    for path in all_paths:
      if start_position in path and end_position in path:
        return True #valid move
    return False