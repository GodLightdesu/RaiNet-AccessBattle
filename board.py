class Board:
  file_to_col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}                          # x
  rank_to_row = {'9': 0, '8' : 1, '7' : 2, '6' : 3, '5' : 4, '4' : 5, '3' : 6, '2' : 7, '1' : 8, '0' : 9} # y
  # board info
  XY = [
    ['a9', 'b9', 'c9', 'd9', 'e9', 'f9', 'g9', 'h9'],
    ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
    ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
    ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
    ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
    ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
    ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
    ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
    ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'],
    ['a0', 'b0', 'c0', 'd0', 'e0', 'f0', 'g0', 'h0']
  ]
  EXIT_POS = ['d0', 'e0', 'd9', 'e9']
  BOUNDARY_POS = ['a0', 'b0', 'c0', 'f0', 'g0', 'h0', 'a9', 'b9', 'c9', 'f9', 'g9', 'h9']
  # create boards
  god_board = {}
  blue_board = {}
  yellow_board = {}

  for i in range(len(XY)):
    for j in range(len(XY[i])):
      god_board[XY[i][j]] = '-'
      blue_board[XY[i][j]] = '-'
  
  for i in reversed(range(len(XY))):
    for j in reversed(range(len(XY[i]))):
      yellow_board[XY[i][j]] = '-'
      
  def __init__(self):
    for i in self.EXIT_POS:
      self.update_all_board(i, 'X')
    for i in self.BOUNDARY_POS:
      self.update_all_board(i, '$')
      
  def convert_xy_to_alg(self, x, y):
    alg = self.XY[y][x]
    return alg

  def convert_alg_to_xy(self, where):
    col, row = where[0], where[1]
    x, y = self.file_to_col[col], self.rank_to_row[row]
    return x, y
  
  def update_all_board(self, pos, change):
    self.god_board[pos] = change
    self.blue_board[pos] = change
    self.yellow_board[pos] = change
      
  def print_god_board(self):
    for i in range(len(self.XY)):
      print(9 - i, end=" ")
      for j in self.XY[i]:
        print(self.god_board[j], end=" ")
      print()
    print("  a b c d e f g h")
  
  def print_blue_board(self):
    for i in range(len(self.XY)):
      print(9 - i, end=" ")
      for j in self.XY[i]:
        print(self.blue_board[j], end=" ")
      print()
    print("  a b c d e f g h")

  def print_yellow_board(self):
    for i in list(reversed((range(len(self.XY))))):
      print(9 - i, end=" ")
      for j in reversed(self.XY[i]):
        print(self.yellow_board[j], end=" ")
        # print(j, end=" ")
      print()
    print("  h g f e d c b a")

  def print_all_board(self):
    # self.update_board()
    print('--------------------------------------')
    print('god view')
    self.print_god_board()
    print('--------------------------------------')
    print('blue view')
    self.print_blue_board()
    print('--------------------------------------')
    print('yellow view')
    self.print_yellow_board()
    print('--------------------------------------')