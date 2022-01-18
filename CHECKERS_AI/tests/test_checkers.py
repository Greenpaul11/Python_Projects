from nose.tools import *
import sys
sys.path.append('/home/oldest/my_projects/CHECKERS_AI/checkers_ai')
from checkers_gameAI import *

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
		    
def test_available_moves():
	board = Board()
	playerI = Player(' @ ', True, 'Test_PlayerI', True)
	playerI.set_player(board.board)
	playerII = Player(' * ', False, 'Test_PlayerII', False)
	playerII.set_player(board.board)
	game = Game(board, playerI, playerII)
	checkers = {'6B': ['5A', '5C'], '6D': ['5C', '5E'], '6F': ['5E', '5G'], '6H': ['5G']}
	for checker in checkers:
		moves = game.available_moves(board.board, 
							 board.board_numbers, 
							 playerI, playerII, 
							 checker)
		for move in moves:
			assert board.board[move] in checker
			
def test_game():
	bOaRd = Board()
	human = Player(' @ ', True, 'Test_PlayerI', False)
	human.set_player(bOaRd.board)
	artificial = Player(' * ', False, 'Test_PlayerII', False)
	artificial.set_player(bOaRd.board)
	gAmE = Game(bOaRd, human, artificial)
	gAmE.play()
	
	
	


		
