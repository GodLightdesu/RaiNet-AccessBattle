import select
from turtle import position
from board import Board
from game import Game
from blue import Blue
from yellow import Yellow


# game logic
class Rainet:
  def __init__(self, blue_init, yellow_init) -> None:
    self.players = [Blue(blue_init), Yellow(yellow_init)]
    self.current_player = self.players[0]
    self.turn = 0
    self.end = False
    self.enemy = self.players[1]
    self.blue_checked_piece = None
    self.yellow_checked_piece = None
  
  def switch_player(self):
    self.turn += 1
    self.current_player = self.players[self.turn%2]
    self.enemy = self.players[self.turn%2 - 1]
    # self.print_game_info()
    
  def print_current_turn(self):
    print(f'Turn: {self.current_player.name}')
  
  def print_game_info(self):
    Board().print_all_board()
    # if self.current_player.name == 'Blue':
    #   print('--------------------------------------')
    #   Board().print_blue_board()
    #   print('--------------------------------------')
    # elif self.current_player.name == 'Yellow':
    #   print('--------------------------------------')
    #   Board().print_blue_board()
    #   print('--------------------------------------')
    self.print_current_turn()
    print('self info -> virus ate:', self.current_player.virus_ate, 'link ate:', self.current_player.link_ate, 
          'lb pos:', self.current_player.lb_pos, 'fw pos:', self.current_player.fw_pos)
    if self.current_player.checked_piece is not None:
      print('             checked enemy:', self.current_player.checked_piece['name'], self.current_player.checked_piece['pos'])
    print('enemy info -> virus ate:', self.enemy.virus_ate, 'link ate:', self.enemy.link_ate, 
          'lb pos:', self.enemy.lb_pos, 'fw pos:', self.enemy.fw_pos) 
    if self.enemy.checked_piece is not None:
      print('              checked enemy:', self.enemy.checked_piece['name'], self.enemy.checked_piece['pos'])
    
  def update_piece_pos(self, old, new):
    selected_piece = self.select_piece_info(old)
    selected_type = selected_piece['type']
    which = selected_piece['no']
    
    if selected_type == 'virus':
      if self.current_player.virus[which]['lb'] == True:
        self.current_player.lb_pos = new
      self.current_player.virus[which]['pos'] = new
    elif selected_type == 'link':
      if self.current_player.link[which]['lb'] == True:
        self.current_player.lb_pos = new
      self.current_player.link[which]['pos'] = new
      
    
  def select_piece_info(self, place):
    piece = None
    for v in range(4):
      places = self.current_player.virus[v]['pos']
      if places == place:
        piece = self.current_player.virus[v]
        # print(places, piece)
    for l in range(4):
      places = self.current_player.link[l]['pos']
      if places == place:
        piece = self.current_player.link[l]
        # print(places, piece)
    return piece
  
  def select_enemy_piece_info(self, place):
    piece = None
    for v in range(4):
      places = self.enemy.virus[v]['pos']
      if places == place:
        piece = self.enemy.virus[v]
        # print(places, piece)
    for l in range(4):
      places = self.enemy.link[l]['pos']
      if places == place:
        piece = self.enemy.link[l]
        # print(places, piece)
    return piece
  
  def get_friend_pieces_pos(self):
    friend_pieces_pos = []
    for v in range(4):
      friend_pieces_pos.append(self.current_player.virus[v]['pos'])
    for l in range(4):
      friend_pieces_pos.append(self.current_player.link[l]['pos'])
    return friend_pieces_pos
  
  def get_enemy_pieces_pos(self):
    enemy_pieces_pos = []
    for v in range(4):
      enemy_pieces_pos.append(self.enemy.virus[v]['pos'])
    for l in range(4):
      enemy_pieces_pos.append(self.enemy.link[l]['pos'])
    return enemy_pieces_pos
  
  def use_lb(self, place):
    lb_no = self.current_player.lb_no
    if place is not None and lb_no == 0:
      selected_piece = self.select_piece_info(place)
      # print(selected_piece)
      selected_type = selected_piece['type']
      which = selected_piece['no']
      if selected_type == 'virus':
        self.current_player.virus[which]['lb'] = True
      elif selected_type == 'link':
        self.current_player.link[which]['lb'] = True
      self.current_player.lb_pos = selected_piece['pos']
    elif lb_no == 1:
      place = self.current_player.lb_pos
      selected_piece = self.select_piece_info(place)
      selected_type = selected_piece['type']
      which = selected_piece['no']
      if selected_type == 'virus':
        self.current_player.virus[which]['lb'] = False
      elif selected_type == 'link':
        self.current_player.link[which]['lb'] = False
      self.current_player.lb_pos = None
      self.current_player.lb_no = 0
    
  def use_fw(self, place):
    fw_no = self.current_player.fw_no
    if place is not None and fw_no == 0:
      self.current_player.fw_pos = place
    elif fw_no == 1:
      self.current_player.fw_pos = None
      self.current_player.fw_no = 0

  def use_vc(self, place):
    selected_piece = self.select_enemy_piece_info(place)
    selected_type = selected_piece['type']
    which = selected_piece['no']
    if selected_type == 'virus':
      self.enemy.virus[which]['known'] = True
    elif selected_type == 'link':
      self.enemy.link[which]['known'] = True
    if self.current_player.name == 'Blue':
      # Board().blue_board[place] = Board().god_board[place]
      Board().blue_board[place] = selected_piece['name']
    elif self.current_player.name == 'Yellow':
      Board().yellow_board[place] = selected_piece['name']
    self.current_player.checked_piece = selected_piece
    self.current_player.vc_no = 1
  
  def use_404(self, piece1, piece2):
    selected_piece1 = self.select_enemy_piece_info(piece1)
    selected_piece2 = self.select_enemy_piece_info(piece2)
    which1 = selected_piece1['no']
    which2 = selected_piece2['no']
    if selected_piece1['known'] == True:
      pass
    elif selected_piece2['known'] == True:
      pass
  
  def play(self):
    while self.end == False:
      # check winner
      if self.current_player.link_ate == 4:
        print("You win")
        quit()
      elif self.current_player.virus_ate == 4:
        print("You lose")
        quit()
      # get game info
      # Fire wall的位置
      FW_place = self.enemy.fw_pos
      # 己方棋子的位置
      friend_pieces = self.get_friend_pieces_pos()
      # 敌方棋子的位置
      enemy_pieces = self.get_enemy_pieces_pos()
      # use skills
      # skills_used = False
      self.print_game_info()
      print('Do you want to use a skills? (y/n)', end=" ")
      use = input()
      while self.current_player.skills_used == False and (use == 'y' or use == 'Y'):
        print('Which skills you want to use (lb, fw, vc, 404, no)?', end=" ")
        skill = input()
        if skill == self.current_player.skills[0]:  # lb
          if self.current_player.lb_no == 0:
            print('Which piece you want to install lb?')
            print(str(friend_pieces), end=" ")
            which_lb = input()
            if which_lb in friend_pieces:
              self.use_lb(which_lb)
              # print(self.select_piece_info(which_lb))
              self.current_player.skills_used = True
          else:
            self.use_lb(None)
            print('removed lb')
            self.current_player.skills_used = True
        elif skill == self.current_player.skills[1]:  # fw
          if self.current_player.fw_no == 0:
            print('Which piece you want to install fw?', end=' ')
            where = input()
            if where not in Board().EXIT_POS and where not in Board().BOUNDARY_POS and where not in enemy_pieces:
              self.use_fw(where)
              self.current_player.skills_used = True
          else:
            self.use_fw(None)
            print('removed fw')
            self.current_player.skills_used = True
        elif skill == self.current_player.skills[2]:  # vc
          if self.current_player.vc_no == 0:
            place = 'a8'
            if place in enemy_pieces:
              self.use_vc(place)
              self.current_player.skills_used = True
          else:
            print('you already have used vc')
            continue
        elif skill == self.current_player.skills[3]:  # 404
          if self.current_player._404_no == 0:
            self.current_player.skills_used = True
          else:
            print('you already have used 404')
            continue
        elif skill == 'no':
          use = 'n'
      
      # switch_player
      if self.current_player.skills_used == True:
        self.current_player.skills_used = False
        # self.switch_player()
        continue
      
      # move piece
      while self.current_player.skills_used == False or (use != 'y' or use != 'Y'):
        # reset所有路径
        if len(Game().all_paths) != 0:
          Game().all_paths.clear()
        # select piece
        print('Which piece you want to move?', end=" ")
        position = input()

        selected_piece = self.select_piece_info(position)
        if selected_piece is not None:
          if selected_piece['lb'] == True:
            # 移动次数上限
            step = 2
          else:
            step = 1
          # 开始搜索
          Game().dfs(position, FW_place, friend_pieces, enemy_pieces, step)
          
          start_position = position
          # for path in Game().all_paths:
          #   print(path)
          print('where you want to move?', end=' ')
          print(Game().all_paths)
          end_position = input()

          valid_move = Game().is_start_and_end_in_paths(start_position, end_position, Game().all_paths)
          # print(valid_move)
          if valid_move == True:
            Game().move_piece(start_position, end_position)
            self.update_piece_pos(start_position, end_position)
            # self.switch_player()
            self.print_game_info()
            break
          else:
            print('invalid move')
            break