from nose.tools import *
import sys
sys.path.append('/home/oldest/my_projects/CHECKERS_PYGAME/checkers')
from checkers_board import *
from checkers_players import *

def test_board():
    board = Board()
    white_checkers = [i for i in board.board if i[1] == 'white']
    assert_equal(12, len(white_checkers))
    black_checkers = [i for i in board.board if i[1] == 'black']
    assert_equal(12, len(black_checkers))
    
    playerI = Player(board.white, board, 'Play Against Human Player', True)
    playerII = Player(board.black, board, 'Play Against Human Player', True)
    
    playerI.available_moves()
    assert playerI.moves[40] == [[33, []]]
    assert playerI.moves[44] == [[35, []], [37, []]]
    assert playerI.moves[46] == [[37, []], [39, []]]

    playerII.available_moves()
    assert playerII.moves[17] == [[24, []], [26, []]]
    assert playerII.moves[23] == [[30, []]]
    assert playerII.moves[21] == [[28, []], [30, []]]

    playerI.choosen = ([40, 'white'], None)
    playerI.update_board(board.board, [33, []], playerI.choosen[0])
    playerI.choosen = ([46, 'white'], None)
    playerI.update_board(board.board, [37, []], playerI.choosen[0])

    playerII.choosen = ([17, 'black'], None)
    playerII.update_board(board.board, [24, []], playerII.choosen[0])
    playerII.choosen = ([23, 'black'], None)
    playerII.update_board(board.board, [30, []], playerII.choosen[0])
    

    for square in board.board:
        if square[0] == 40:
            assert square[1] == None
        elif square[0] == 46:
            assert square[1] == None
        elif square[0] == 17:
            assert square[1] == None
        elif square[0] == 23:
            assert square[1] == None
        elif square[0] == 37:
            assert square[1] == 'white'
        elif square[0] == 30:
            assert square[1] == 'black'

    playerI.available_moves()
    win = playerI.moves[37]
    playerI.choosen = ([37, 'white'], None)
    playerI.update_board(board.board, win[1], playerI.choosen[0])
    for square in board.board:
        if square[0] == 23:
            assert square[1] == 'white'
            
def test_queen_moves():
    board = Board()
    playerI = Player(board.white, board, 'Play Against Human Player', True)
    playerII = Player(board.black, board, 'Play Against Human Player', True)
    for square in board.board:
        if square[1] != None:
            square[1] = None
    
    white = [14, 28, 44, 46, 12, 10]
    black_queen = 7
    for square in board.board:
        if square[0] in white:
            square[1] = 'white'
        elif square[0] == black_queen:
            square[1] = 'black queen'
            
    playerII.available_moves()
    win = playerII.moves[7]
    win[0][1].sort()
    white.sort()
    assert win[0][1] == white
    
    playerII.update_board(board.board, win[0], [7, 'black queen'])
    for square in board.board:
        if square[1] == 'white':
            raise ValueError
    
    
        
