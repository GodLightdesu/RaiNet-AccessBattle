from board import Board

class Yellow:
  def __init__(self, real_init):
    # self information
    self.name = "Yellow"
    self.link_ate = 0
    self.virus_ate = 0
    # skills
    self.skills = ['lb', 'fw', 'vc', '404']
    self.lb_no = 0
    self.fw_no = 0
    self.vc_no = 0
    self._404_no = 0
    self.lb_pos = None
    self.fw_pos = None
    self.skills_used = False
    # piece init
    self.real_init = real_init
    self.pos_init = ['h8', 'g8', 'f8', 'e7', 'd7', 'c8', 'b8', 'a8']
    self.virus_name = 'v'
    self.link_name = 'l'
    # virus
    self.virus = [{'no' : 0, 'name': self.virus_name, 'pos': None, 'lb': False, 'known': False, 'type' : 'virus'},
                  {'no' : 1, 'name': self.virus_name, 'pos': None, 'lb': False, 'known': False, 'type' : 'virus'},
                  {'no' : 2, 'name': self.virus_name, 'pos': None, 'lb': False, 'known': False, 'type' : 'virus'},
                  {'no' : 3, 'name': self.virus_name, 'pos': None, 'lb': False, 'known': False, 'type' : 'virus'}]
    # link
    self.link = [{'no' : 0, 'name': self.link_name, 'pos': None, 'lb': False, 'known': False, 'type' : 'link'},
                 {'no' : 1, 'name': self.link_name, 'pos': None, 'lb': False, 'known': False, 'type' : 'link'},
                 {'no' : 2, 'name': self.link_name, 'pos': None, 'lb': False, 'known': False, 'type' : 'link'},
                 {'no' : 3, 'name': self.link_name, 'pos': None, 'lb': False, 'known': False, 'type' : 'link'}]
    
    # team init
    v = 0
    l = 0
    # team_dict = dict(zip(self.pos_init, real_init))
    for i in range(8):
      if self.real_init[i] == self.virus_name:
        self.virus[v]['pos'] = self.pos_init[i]
        # print(self.virus[v]['name'], self.virus[v]['pos'])
        v += 1
      if self.real_init[i] == self.link_name:
        self.link[l]['pos'] = self.pos_init[i]
        # print(self.link[l]['name'], self.link[l]['pos'])
        l += 1
    for v in range(4):
      piece = self.virus[v]['pos']
      Board().god_board[piece] = self.virus[v]['name']
      Board().yellow_board[piece] = self.virus[v]['name']
      Board().blue_board[piece] = '?'
    for l in range(4):
      piece = self.link[l]['pos']
      Board().god_board[piece] = self.link[l]['name']
      Board().yellow_board[piece] = self.link[l]['name']
      Board().blue_board[piece] = '?'