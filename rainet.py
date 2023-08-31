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
    
  def get_available_skill(self):
    skills = ['vc', '404']
    current_player_skills_available = []
    enemy_skills_available = []
    for i in skills:
      print(self.current_player.skills_used[i])
      if self.current_player.skills_used[i] == False:
        current_player_skills_available.append(i)
      if self.enemy.skills_used[i] == False:
        enemy_skills_available.append(i)
    return current_player_skills_available, enemy_skills_available
  
  def print_game_info(self):
    abailable_skills = self.get_available_skill()
    Board().print_all_board()
    self.print_current_turn()
    print('self info -> virus ate:', self.current_player.virus_ate, 'link ate:', self.current_player.link_ate, 
          'lb pos:', self.current_player.lb_pos, 'fw pos:', self.current_player.fw_pos)
    if self.current_player.checked_piece is not None:
      print('             checked enemy:', self.current_player.checked_piece['name'], self.current_player.checked_piece['pos'])
    print('             skills can use without lb and fw:', abailable_skills[0])
    print('enemy info -> virus ate:', self.enemy.virus_ate, 'link ate:', self.enemy.link_ate, 
          'lb pos:', self.enemy.lb_pos, 'fw pos:', self.enemy.fw_pos) 
    if self.enemy.checked_piece is not None:
      print('              checked enemy:', self.enemy.checked_piece['name'], self.enemy.checked_piece['pos'])
    print('              skills can use without lb and fw:', abailable_skills[1])
    
  def update_piece_pos(self, old, new):
    selected_piece = self.select_piece_info(old)
    # selected_type = selected_piece['type']
    which = selected_piece['no']
    if self.current_player.piece[which]['lb'] == True:
      self.current_player.lb_pos = new
    self.current_player.piece[which]['pos'] = new

  def select_piece_info(self, place):
    piece = None
    for i in range(8):
      if self.current_player.piece[i]['pos'] == place:
        piece = self.current_player.piece[i]
    return piece
  
  def select_enemy_piece_info(self, place):
    piece = None
    for i in range(8):
      if self.enemy.piece[i]['pos'] == place:
        piece = self.enemy.piece[i]
    return piece
  
  def get_friend_pieces_pos(self):
    friend_pieces_pos = []
    for i in range(8):
      friend_pieces_pos.append(self.current_player.piece[i]['pos'])
    return friend_pieces_pos
  
  def get_enemy_pieces_pos(self):
    enemy_pieces_pos = []
    for i in range(8):
      enemy_pieces_pos.append(self.enemy.piece[i]['pos'])
    return enemy_pieces_pos
  
  def use_lb(self, place):
    lb_used = self.current_player.skills_used['lb']
    if place is not None and lb_used == False:
      selected_piece = self.select_piece_info(place)
      # print(selected_piece)
      which = selected_piece['no']
      # update skill info
      self.current_player.lb_pos = selected_piece['pos']
      self.current_player.piece[which]['lb'] = True
      self.current_player.skills_used['lb'] = True
    elif lb_used == True:
      place = self.current_player.lb_pos
      selected_piece = self.select_piece_info(place)
      which = selected_piece['no']
      # update skill info
      self.current_player.lb_pos = None
      self.current_player.piece[which]['lb'] = False
      self.current_player.skills_used['lb'] = False
    
  def use_fw(self, place):
    fw_no = self.current_player.skills_used['fw']
    if place is not None and fw_no == False:
      self.current_player.fw_pos = place
      self.current_player.skills_used['fw'] = True
    elif fw_no == True:
      self.current_player.fw_pos = None
      self.current_player.skills_used['fw'] = False

  def use_vc(self, place):
    selected_piece = self.select_enemy_piece_info(place)
    which = selected_piece['no']
    self.enemy.piece[which]['known'] = True
    if self.current_player.name == 'Blue':
      # Board().blue_board[place] = Board().god_board[place]
      Board().blue_board[place] = selected_piece['name']
    elif self.current_player.name == 'Yellow':
      Board().yellow_board[place] = selected_piece['name']
    self.current_player.checked_piece = selected_piece
    self.current_player.skills_used['vc'] = True
  
  def use_404(self, piece1, piece2):
    selected_piece1 = self.select_piece_info(piece1)
    selected_piece2 = self.select_piece_info(piece2)
    which1 = selected_piece1['no']
    which2 = selected_piece2['no']
    # swap piece pos
    # print(self.current_player.piece[which1]['pos'], self.current_player.piece[which2]['pos'])
    self.current_player.piece[which1]['pos'], self.current_player.piece[which2]['pos'] = self.current_player.piece[which2]['pos'], self.current_player.piece[which1]['pos']
    # print(self.current_player.piece[which1]['pos'], self.current_player.piece[which2]['pos'])
    Board().update_all_board(self.current_player.piece[which1]['pos'], self.current_player.piece[which1]['name'])
    Board().update_all_board(self.current_player.piece[which2]['pos'], self.current_player.piece[which2]['name'])
    if self.current_player.name == 'Blue':
      Board().yellow_board[piece1] = '?'
      Board().yellow_board[piece2] = '?'
    elif self.current_player.name == 'Yellow':
      Board().blue_board[piece1] = '?'
      Board().blue_board[piece2] = '?'
    # change piece to unknown
    if selected_piece1['known'] == True:
      self.current_player.piece[which1]['known'] = False
    elif selected_piece2['known'] == True:
      self.current_player.piece[which2]['known'] = False
    # update skill stats
    self.enemy.checked_piece = None
    self.current_player.skills_used['404'] = True
    
  
  def play(self):
    while self.end == False:
      # check winner
      if self.current_player.link_ate == 4:
        print("You win")
        quit()
      elif self.current_player.virus_ate == 4:
        print("You lose")
        quit()
      # Fire wall的位置
      FW_place = self.enemy.fw_pos
      # 己方棋子的位置
      friend_pieces = self.get_friend_pieces_pos()
      # 敌方棋子的位置
      enemy_pieces = self.get_enemy_pieces_pos()
      print(enemy_pieces)
      # game start
      self.print_game_info()
      print('Do you want to use a skills? (y/n)', end=" ")
      use = input()
      while self.current_player.skill_used == False and (use == 'y' or use == 'Y'):
        print('Which skills you want to use (lb, fw, vc, 404, no)?', end=" ")
        skill = input()
        if skill == self.current_player.skills[0]:  # lb
          if self.current_player.skills_used['lb'] == False:
            print('Which piece you want to install lb?')
            print(str(friend_pieces), end=" ")
            which_lb = input()
            if which_lb in friend_pieces:
              self.use_lb(which_lb)
              # print(self.select_piece_info(which_lb))
              self.current_player.skill_used = True
          else:
            self.use_lb(None)
            print('removed lb')
            self.current_player.skill_used = True
        elif skill == self.current_player.skills[1]:  # fw
          if self.current_player.skills_used['fw'] == False:
            print('Which piece you want to install fw?', end=' ')
            where = input()
            if where not in Board().EXIT_POS and where not in Board().BOUNDARY_POS and where not in enemy_pieces:
              self.use_fw(where)
              self.current_player.skill_used = True
          else:
            self.use_fw(None)
            print('removed fw')
            self.current_player.skill_used = True
        elif skill == self.current_player.skills[2]:  # vc
          if self.current_player.skills_used['vc'] == False:
            print('Which enemy piece you want to install vc?', end=' ')
            where = input()
            if where in enemy_pieces:
              self.use_vc(where)
              self.current_player.skill_used = True
          else:
            print('you already have used vc')
            continue
        elif skill == self.current_player.skills[3]:  # 404
          if self.current_player.skills_used['404'] == False:
            # print('Which two piece you want to install 404 (e.g. d4, d5)?', end=' ')
            lst = []
            for i in range(2):
              print('Which two piece you want to install 404 (e.g. d4, enter, d5)?', end=' ')
              ele = input()
              # adding the element
              lst.append(ele)
            # where = input()
            piece1, piece2 = lst[0], lst[1]
            if piece1 in friend_pieces and piece2 in friend_pieces:
              self.use_404(piece1, piece2)
              self.current_player.skill_used = True
          else:
            print('you already have used 404')
            continue
        elif skill == 'no':
          use = 'n'
      
      # switch_player
      if self.current_player.skill_used == True:
        self.current_player.skill_used = False
        self.switch_player()
        continue
      
      # move piece
      while self.current_player.skill_used == False or (use != 'y' or use != 'Y'):
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
            if end_position in enemy_pieces:
              end_piece = self.select_enemy_piece_info(end_position)
              if end_piece['name'] == self.enemy.virus_name:
                self.current_player.virus_ate += 1
              elif end_piece['name'] == self.enemy.link_name:
                self.current_player.link_ate += 1
          
            Game().move_piece(start_position, end_position)
            self.update_piece_pos(start_position, end_position)
            self.switch_player()
            self.print_game_info()
            break
          else:
            print('invalid move')
            break