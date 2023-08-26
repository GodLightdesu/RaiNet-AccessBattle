from board import Board

class Yellow():
  def __init__(self):
    # super().__init__()
    self.pos_init = ['h8', 'g8', 'f8', 'e7', 'd7', 'c8', 'b8', 'a8']
    self.link_ate = 0
    self.virus_ate = 0
    # piece name init
    self.virus_name = 'v'
    self.link_name = 'l'
    # virus
    self.virus = [{'name': self.virus_name, 'pos': None, 'lb': False, 'known': False},
                  {'name': self.virus_name, 'pos': None, 'lb': False, 'known': False},
                  {'name': self.virus_name, 'pos': None, 'lb': False, 'known': False},
                  {'name': self.virus_name, 'pos': None, 'lb': False, 'known': False}]
    # link
    self.link = [{'name': self.link_name, 'pos': None, 'lb': False, 'known': False},
                 {'name': self.link_name, 'pos': None, 'lb': False, 'known': False},
                 {'name': self.link_name, 'pos': None, 'lb': False, 'known': False},
                 {'name': self.link_name, 'pos': None, 'lb': False, 'known': False}]
  
  def team_init(self, real_init):
    v = 0
    l = 0
    # team_dict = dict(zip(self.pos_init, real_init))
    for i in range(8):
      if real_init[i] == self.virus_name:
        self.virus[v]['pos'] = self.pos_init[i]
        print(self.virus[v]['name'], self.virus[v]['pos'])
        v += 1
      if real_init[i] == self.link_name:
        self.link[l]['pos'] = self.pos_init[i]
        print(self.link[l]['name'], self.link[l]['pos'])
        l += 1
    for v in range(4):
      piece = self.virus[v]['pos']
      Board.god_board[piece] = self.virus[v]['name']
      Board.yellow_board[piece] = self.virus[v]['name']
      Board.blue_board[piece] = '?'
    for l in range(4):
      piece = self.link[l]['pos']
      Board.god_board[piece] = self.link[l]['name']
      Board.yellow_board[piece] = self.link[l]['name']
      Board.blue_board[piece] = '?'