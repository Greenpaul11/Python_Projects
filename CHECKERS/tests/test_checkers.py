from nose.tools import *
import sys
sys.path.append('/home/oldest/my_projects/CHECKERS/checkers')
from checkers_game import *

def start():
	print('start')
	
def stop():
	print('stop')
	
@with_setup(start, stop)
def test_board():
	board = Board()
	for count, square in enumerate(board.board):
		if square == '   ':
			board.board.pop(count)
			board.board.insert(count, ' $ ')
	assert_equal(68, board.board.count(' $ '))
	assert_equal(2, board.board.count(' A '))
	playerI = Player(' @ ', True, 'Test_PlayerI', True)
	playerI.set_player(board.board)
	playerII = Player(' * ', False, 'Test_PlayerII', False)
	playerII.set_player(board.board)
	assert_equal(board.board.count(' @ '), board.board.count(' * '))
	assert 12 == board.board.count(' @ ')
	assert (board.board.count(' $ ') 
		    + board.board.count(' * ') 
		    + board.board.count(' @ ')
		    == 68)
		    
def test_game():
	board = Board()
	playerI = Player(' @ ', True, 'Test_PlayerI', False)
	playerI.set_player(board.board)
	playerII = Player(' * ', False, 'Test_PlayerII', False)
	playerII.set_player(board.board)
	free_sq = board.board.count('   ')
	game = Game(board, playerI, playerII)
	game.play()

	
	


		
