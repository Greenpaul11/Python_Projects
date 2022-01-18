from nose.tools import *
import sys
sys.path.append('/home/oldest/my_projects/TICTACTOE_AI/tictactoe_ai')
from tictactoeAI_game import *


def start():
	print('start')
	
def stop():
	print('stop')
	
@with_setup(start, stop)
def test_board():
	board = Board_Tic_Tac_Toe()
	assert_equal(9, len(board.board))
	for count, square in enumerate(board.board):
		board.board.pop(count)
		board.board.insert(count, count)
	for square in board.board:
		assert square == board.board.index(square)
		


