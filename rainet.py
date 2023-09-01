from board import Board
from game import Game
from human import Human
from ai import AI
import random
import sys

# game logic
class Rainet:
  def __init__(self, human_init, ai_init) -> None:
    self.players = [Human(human_init), AI(ai_init)]
    self.human = self.players[0]
    self.ai = self.players[1]
    self.turn = 0
    self.end = False
    self.human_checked_piece = None
    self.ai_checked_piece = None
    
  def human_move(self, start, end, ai_pieces):
    if end in ai_pieces:
      self.eat_ai_piece(end)
    # render move piece
    Game().move_piece(start, end)
    # update piece position
    self.human.update_piece_pos(start, end)
    if end in self.human.EXIT_POS:  # piece can exit
      # get exit piece info
      select_piece_info = self.human.select_piece_info(end)
      exit_piece = select_piece_info[0]
      which = select_piece_info[1]
      # update piece exit info
      if exit_piece['name'] == self.human.virus_name:
        self.human.virus_ate += 1
      elif exit_piece['name'] == self.human.link_name:
        self.human.link_ate += 1
      # del exit piece
      self.human.kill_piece(which)
      Board().update_all_board(end, 'X')
      
  def ai_move(self, start, end, human_pieces):
    if end in human_pieces:
      self.eat_human_piece(end)
    # render move piece
    Game().move_piece(start, end)
    # update piece position
    self.ai.update_piece_pos(start, end)
    if end in self.ai.EXIT_POS:  # piece can exit
      # get exit piece info
      exit_piece = self.ai.select_piece_info(end)[0]
      which = self.ai.select_piece_info(end)[1]
      # update piece exit info
      if exit_piece['name'] == self.ai.virus_name:
        self.ai.virus_ate += 1
      elif exit_piece['name'] == self.ai.link_name:
        self.ai.link_ate += 1
      # del exit piece
      self.ai.kill_piece(which)
      Board().update_all_board(end, 'X')
    
  def get_available_skill(self):
    skills = ['vc', '404']
    human_skills_available = []
    ai_skills_available = []
    for i in skills:
      # print(self.human.skills_used[i])
      if self.human.skills_used[i] == False:
        human_skills_available.append(i)
      if self.ai.skills_used[i] == False:
        ai_skills_available.append(i)
    return human_skills_available, ai_skills_available
  
  def print_game_info(self):
    available_skills = self.get_available_skill()
    Board().print_all_board()
    print('self info -> virus ate:', self.human.virus_ate, 'link ate:', self.human.link_ate, 
          'lb pos:', self.human.lb_pos, 'fw pos:', self.human.fw_pos)
    if self.human.checked_piece is not None:
      print('             checked ai:', self.human.checked_piece['name'], self.human.checked_piece['pos'])
    print('             skills can use without lb and fw:', available_skills[0])
    print('ai info -> virus ate:', self.ai.virus_ate, 'link ate:', self.ai.link_ate, 
          'lb pos:', self.ai.lb_pos, 'fw pos:', self.ai.fw_pos) 
    if self.ai.checked_piece is not None:
      print('              checked ai:', self.ai.checked_piece['name'], self.ai.checked_piece['pos'])
    print('              skills can use without lb and fw:', available_skills[1])
  
  def get_human_pieces_pos(self):
    human_pieces_pos = []
    for i in range(len(self.human.piece)):
      if self.human.piece[i]['pos'] is not None:
        human_pieces_pos.append(self.human.piece[i]['pos'])
    return human_pieces_pos
  
  def get_ai_pieces_pos(self):
    ai_pieces_pos = []
    for i in range(len(self.ai.piece)):
      if self.ai.piece[i]['pos'] is not None:
        ai_pieces_pos.append(self.ai.piece[i]['pos'])
    return ai_pieces_pos
  
  def eat_ai_piece(self, end):
    # get enemy piece info
    eat_piece = self.ai.select_piece_info(end)[0]
    which = self.ai.select_piece_info(end)[1]
    # update piece eaten info
    if eat_piece['name'] == self.ai.virus_name:
      self.human.virus_ate += 1
    elif eat_piece['name'] == self.ai.link_name:
      self.human.link_ate += 1
    # del eaten piece
    self.ai.kill_piece(which)
  
  def eat_human_piece(self, end):
    # get enemy piece info
    eat_piece_info = self.human.select_piece_info(end)
    eat_piece = eat_piece_info[0]
    which = eat_piece_info[1]
    # update piece eaten info
    if eat_piece['name'] == self.human.virus_name:
      self.ai.virus_ate += 1
    elif eat_piece['name'] == self.human.link_name:
      self.ai.link_ate += 1
    # del eaten piece
    self.human.kill_piece(which)
    
  def use_lb(self, place):
    pass
    # lb_used = self.current_player.skills_used['lb']
    # if place is not None and lb_used == False:
    #   selected_piece = self.select_piece_info(place)
    #   # print(selected_piece)
    #   which = selected_piece['no']
    #   # update skill info
    #   self.current_player.lb_pos = selected_piece['pos']
    #   self.current_player.piece[which]['lb'] = True
    #   self.current_player.skills_used['lb'] = True
    # elif lb_used == True:
    #   place = self.current_player.lb_pos
    #   selected_piece = self.select_piece_info(place)
    #   which = selected_piece['no']
    #   # update skill info
    #   self.current_player.lb_pos = None
    #   self.current_player.piece[which]['lb'] = False
    #   self.current_player.skills_used['lb'] = False
    
  def use_fw(self, place):
    pass
    # fw_no = self.current_player.skills_used['fw']
    # if place is not None and fw_no == False:
    #   self.current_player.fw_pos = place
    #   self.current_player.skills_used['fw'] = True
    # elif fw_no == True:
    #   self.current_player.fw_pos = None
    #   self.current_player.skills_used['fw'] = False

  def use_vc(self, place):
    pass
    # selected_piece = self.select_enemy_piece_info(place)
    # which = selected_piece['no']
    # self.enemy.piece[which]['known'] = True
    # if self.current_player.name == 'Blue':
    #   # Board().blue_board[place] = Board().god_board[place]
    #   Board().blue_board[place] = selected_piece['name']
    # elif self.current_player.name == 'Yellow':
    #   Board().yellow_board[place] = selected_piece['name']
    # self.current_player.checked_piece = selected_piece
    # self.current_player.skills_used['vc'] = True
  
  def use_404(self, piece1, piece2):
    pass
    # selected_piece1 = self.select_piece_info(piece1)
    # selected_piece2 = self.select_piece_info(piece2)
    # which1 = selected_piece1['no']
    # which2 = selected_piece2['no']
    # # swap piece pos
    # # print(self.current_player.piece[which1]['pos'], self.current_player.piece[which2]['pos'])
    # self.current_player.piece[which1]['pos'], self.current_player.piece[which2]['pos'] = self.current_player.piece[which2]['pos'], self.current_player.piece[which1]['pos']
    # # print(self.current_player.piece[which1]['pos'], self.current_player.piece[which2]['pos'])
    # Board().update_all_board(self.current_player.piece[which1]['pos'], self.current_player.piece[which1]['name'])
    # Board().update_all_board(self.current_player.piece[which2]['pos'], self.current_player.piece[which2]['name'])
    # if self.current_player.name == 'Blue':
    #   Board().yellow_board[piece1] = '?'
    #   Board().yellow_board[piece2] = '?'
    # elif self.current_player.name == 'Yellow':
    #   Board().blue_board[piece1] = '?'
    #   Board().blue_board[piece2] = '?'
    # # change piece to unknown
    # if selected_piece1['known'] == True:
    #   self.current_player.piece[which1]['known'] = False
    # elif selected_piece2['known'] == True:
    #   self.current_player.piece[which2]['known'] = False
    # # update skill stats
    # self.enemy.checked_piece = None
    # self.current_player.skills_used['404'] = True
    
  
  def play(self):      # without skills
    # game start
    human_action_end = False
    ai_action_end = False
    while self.end == False:      
      # Fire wall的位置
      human_fw_place = self.human.fw_pos
      ai_fw_place = self.ai.fw_pos
      # 己方棋子的位置
      human_pieces = self.get_human_pieces_pos()
      # 敌方棋子的位置
      ai_pieces = self.get_ai_pieces_pos()
      
      # human action:
      while human_action_end == False:
        ai_action_end = False
        self.print_game_info()
        print('Which piece you want to move?')
        print(human_pieces, end=' ')
        # start = input()
        start = random.choice(human_pieces)
        if start in human_pieces:
          selected_piece = self.human.select_piece_info(start)[0]
          # define 移动次数上限
          if selected_piece['lb'] == True:  
            step = 2
          else:
            step = 1
          # get all possible valid move
          all_path = Game().find_valid_paths(start, step, ai_fw_place, human_pieces, Board().human_exit)
          all_valid_move = Game().all_valid_moves(all_path)
          if start in all_valid_move:
            all_valid_move.remove(start)
            
          if len(all_valid_move) == 0:  # no valid move
            continue
          # get move target
          print('where you want to move?',all_valid_move , end=' ')
          # end = input()
          end = random.choice(all_valid_move)
          # check valid
          valid_move = Game().is_start_and_end_in_paths(all_path, start, end)
          # print(valid_move)
          if valid_move == True:
            # move piece
            self.human_move(start, end, ai_pieces)
            # end human turn
            human_action_end = True
      
      # check winner
      if self.human.link_ate == 4 or self.ai.virus_ate == 4:
        print("You win")
        quit()
      elif self.human.virus_ate == 4 or self.ai.link_ate == 4:
        print("You lose")
        quit()
        
      # Fire wall的位置
      human_fw_place = self.human.fw_pos
      ai_fw_place = self.ai.fw_pos
      # 己方棋子的位置
      human_pieces = self.get_human_pieces_pos()
      # 敌方棋子的位置
      ai_pieces = self.get_ai_pieces_pos()
        
      # ai action
      while ai_action_end == False:
        human_action_end = False
        ai_start = random.choice(ai_pieces)
        print(ai_pieces, ai_start)
        selected_piece = self.ai.select_piece_info(ai_start)[0]
        # define 移动次数上限
        if selected_piece['lb'] == True:
          step = 2
        else:
          step = 1
        # get all possible valid move
        all_path = Game().find_valid_paths(ai_start, step, human_fw_place, ai_pieces, Board().ai_exit)
        all_valid_move = Game().all_valid_moves(all_path)
        if ai_start in all_valid_move:
          all_valid_move.remove(ai_start)
        
        if len(all_valid_move) == 0:  # no valid move
          continue
          
        ai_end = random.choice(all_valid_move)
        # move piece
        self.ai_move(ai_start, ai_end, human_pieces)
        # end ai turn
        ai_action_end = True

      # check winner
      if self.human.link_ate == 4 or self.ai.virus_ate == 4:
        print("You win")
        quit()
      elif self.human.virus_ate == 4 or self.ai.link_ate == 4:
        print("You lose")
        quit()
        
  def play_(self):      # with skills
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
      # print(enemy_pieces)
      
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
        # select piece
        print('Which piece you want to move?', end=" ")
        # if self.current_player.name == 'Blue':
        #  position = input()
        # elif self.current_player.name == 'Yellow':
        position = random.choice(friend_pieces)

        selected_piece = self.select_piece_info(position)
        if selected_piece is not None:
          if selected_piece['lb'] == True:
            # 移动次数上限
            step = 2
          else:
            step = 1
          # 开始搜索
          all_path = Game().find_valid_paths(position, step, FW_place, friend_pieces, enemy_pieces)
          all_valid_move = Game().all_valid_moves(all_path)
          
          
          print('where you want to move?', end=' ')
          print(all_valid_move)
          # end_position = input()
          
          start_position = position
          end_position = random.choice(all_valid_move)

          valid_move = Game().is_start_and_end_in_paths(all_path, start_position, end_position)
          # print(valid_move)
          if valid_move == True:
            if end_position in enemy_pieces:
              end_piece = self.select_enemy_piece_info(end_position)
              which = end_piece['no']
              if end_piece['name'] == self.enemy.virus_name:
                self.current_player.virus_ate += 1
              elif end_piece['name'] == self.enemy.link_name:
                self.current_player.link_ate += 1
              del self.enemy.piece[which]
          
            Game().move_piece(start_position, end_position)
            self.update_piece_pos(start_position, end_position)
            self.switch_player()
            self.print_game_info()
            break
          else:
            print('invalid move')
            break