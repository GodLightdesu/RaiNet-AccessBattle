board = [['' for _ in range(8)] for _ in range(8)]

class ChessPiece:
    def __init__(self, position, identity):
        self.position = position
        self.identity = identity
        self.is_flipped = False
        self.skill = None
    
    def move(self, new_position):
        # 檢查移動是否合法
        if self.is_valid_move(new_position):
            self.position = new_position

    def is_valid_move(self, new_position):
        # 檢查移動是否合法
        # 只能上下左右移動一格
        if abs(new_position[0] - self.position[0]) + abs(new_position[1] - self.position[1]) != 1:
            return False
        # 如果有LB技能，可以移動兩格
        if self.skill == 'LB':
            if abs(new_position[0] - self.position[0]) + abs(new_position[1] - self.position[1]) > 2:
                return False
        return True

    def be_eaten(self):
        # 棋子被吃掉
        self.position = None

    def flip(self):
        # 翻面
        self.is_flipped = True

    def use_skill(self, skill):
        # 使用技能
        self.skill = skill

    def remove_skill(self):
        # 移除技能
        self.skill = None
        
class Player:
    def __init__(self, identity):
        self.identity = identity
        self.pieces = []
        self.skills = ['LB', 'Wall', 'VC', '404']

    def add_piece(self, piece):
        # 添加棋子
        self.pieces.append(piece)

    def remove_piece(self, piece):
        # 移除棋子
        self.pieces.remove(piece)

    def has_won(self):
        # 判斷是否勝利
        l_count = 0
        v_count = 0
        for piece in self.pieces:
            if piece.identity == 'L' and piece.position[0] == 7:
                l_count += 1
            if piece.identity == 'V' and piece.position[0] == 0:
                v_count += 1
        return l_count == 4 or v_count == 4

    def use_skill(self, skill, piece=None, target=None):
        # 使用技能
        if skill == 'LB':
            # 添加LB技能到棋子上
            if piece.skill is None:
                piece.use_skill('LB')
        elif skill == 'Wall':
            # 添加Wall技能到棋子上
            if piece.skill is None:
                piece.use_skill('Wall')
        elif skill == 'VC':
            # 查毒技能
            target.flip()
        elif skill == '404':
            # 互換技能
            piece.position, target.position = target.position, piece.position
            
class Game:
    def __init__(self):
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.players = [Player('L'), Player('V')]

        # 初始化棋子
        self.init_pieces()

        # 遊戲開始
        self.current_player = self.players[0]
        self.turn = 1
        self.play()

    def init_pieces(self):
        # 初始化棋子
        for i in range(4):
            l_piece = ChessPiece((6, i), 'L')
            v_piece = ChessPiece((1, i), 'V')
            self.players[0].add_piece(l_piece)
            self.players[1].add_piece(v_piece)
            self.board[6][i] = l_piece
            self.board[1][i] = v_piece

    def play(self):
        # 遊戲循環
        while True:
            print(f'Turn {self.turn}: {self.current_player.identity}')

            # 顯示棋盤狀態
            self.display_board()

            # 玩家操作
            self.player_action()

            # 判斷勝負
            if self.current_player.has_won():
                print(f'{self.current_player.identity} Wins!')
                break

            # 換下一個玩家
            self.current_player = self.players[(self.players.index(self.current_player) + 1) % 2]
            self.turn += 1

    def player_action(self):
        # 玩家操作
        while True:
            action = input('Enter your action (move/use skill/end): ')
            if action == 'move':
                # 移動棋子
                piece_pos = tuple(map(int, input('Enter the piece position: ').split(',')))
                new_pos = tuple(map(int, input('Enter the new position: ').split(',')))
                piece = self.board[piece_pos[0]][piece_pos[1]]
                if piece is not None and piece.identity == self.current_player.identity:
                    piece.move(new_pos)
                    break
            elif action == 'use skill':
                # 使用技能
                skill = input('Enter the skill you want to use (LB/Wall/VC/404): ')
                if skill in self.current_player.skills:
                    if skill == 'VC':
                        target_pos = tuple(map(int, input('Enter the target position: ').split(',')))
                        target = self.board[target_pos[0]][target_pos[1]]
                        if target is not None and target.is_flipped:
                            self.current_player.use_skill(skill, target=target)
                            break
                    else:
                        piece_pos = tuple(map(int, input('Enter the piece position: ').split(',')))
                        piece = self.board[piece_pos[0]][piece_pos[1]]
                        if piece is not None and piece.identity == self.current_player.identity:
                            self.current_player.use_skill(skill, piece=piece)
                            break
            elif action == 'end':
                # 結束回合
                break

    def display_board(self):
        # 顯示棋盤狀態
        print('  0 1 2 3 4 5 6 7')
        for i in range(8):
            row_str = str(i) + ' '
            for j in range(8):
                if self.board[i][j] is None:
                    row_str += '. '
                else:
                    row_str += self.board[i][j].identity + ' '
            print(row_str)
            
game = Game()