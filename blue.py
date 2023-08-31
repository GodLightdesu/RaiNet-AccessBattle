from board import Board

class Blue:
  def __init__(self, real_init):
    # self information
    self.name = "Blue"
    self.link_ate = 0
    self.virus_ate = 0
    # skills
    self.skills = ['lb', 'fw', 'vc', '404']
    self.skills_used = {'lb': False, 'fw': False, 'vc': False, '404': False}
    self.lb_no = 0
    self.fw_no = 0
    self.vc_no = 0
    self._404_no = 0
    self.lb_pos = None
    self.fw_pos = None
    self.checked_piece = None
    self.skill_used = False
    # piece init
    self.pos_init = ['a1', 'b1', 'c1', 'd2', 'e2', 'f1', 'g1', 'h1']
    self.virus_name = 'V'
    self.link_name = 'L'
    self.unkown = '?'
    self.real_init = real_init
    # pieces
    self.piece = [{'no' : 0, 'name': self.unkown, 'pos': self.pos_init[0], 'lb': False, 'known': False},
                  {'no' : 1, 'name': self.unkown, 'pos': self.pos_init[1], 'lb': False, 'known': False},
                  {'no' : 2, 'name': self.unkown, 'pos': self.pos_init[2], 'lb': False, 'known': False},
                  {'no' : 3, 'name': self.unkown, 'pos': self.pos_init[3], 'lb': False, 'known': False},
                  {'no' : 4, 'name': self.unkown, 'pos': self.pos_init[4], 'lb': False, 'known': False},
                  {'no' : 5, 'name': self.unkown, 'pos': self.pos_init[5], 'lb': False, 'known': False},
                  {'no' : 6, 'name': self.unkown, 'pos': self.pos_init[6], 'lb': False, 'known': False},
                  {'no' : 7, 'name': self.unkown, 'pos': self.pos_init[7], 'lb': False, 'known': False}]
    
    self.init_dict = dict(zip(self.pos_init, self.real_init))
    # print(self.init_dict, len(self.init_dict))
    which = 0
    for i in range(8):
      if self.piece[which]['pos'] == self.pos_init[i]:
        self.piece[which]['name'] = self.init_dict[self.pos_init[i]]
        which += 1
        
    for i in range(8):
      piece = self.piece[i]['pos']
      Board().god_board[piece] = self.piece[i]['name']
      Board().blue_board[piece] = self.piece[i]['name']
      Board.yellow_board[piece] = '?'