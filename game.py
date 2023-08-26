from board import Board

# action logic
class Game():
  def __init__(self) -> None:
    pass
  
  def select_piece(self, where):
    # [god, blue, yellow]
    selected_piece = [Board.god_board[where], Board.blue_board[where], Board.yellow_board[where]]
    return selected_piece
  
  def move_piece(self, start_square, end_square):
    print('move from: ' + start_square + ' to: ' + end_square)
    # select the piece
    piece = self.select_piece(start_square)
    # move piece
    Board().update_board(start_square, '-')
    for i in range(3):
      Board().update_board(end_square, piece[i])
      
  def check_move(self, start_square, end_square):
    pass