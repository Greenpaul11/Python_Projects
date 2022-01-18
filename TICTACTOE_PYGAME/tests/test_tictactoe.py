import sys
sys.path.append('/home/oldest/my_projects/TICTACTOE_PYGAME/tictactoe_pygame')
from tictactoe_pygame.tictactoe_engine import *


def test_winner():
	eng = Engine()
	symbol = 'X'
	
	board = [i for i in range(6)]
	for i in range(3):
		board.append('X')
	
	assert eng.check_winner(board, symbol)
	
	board = [i for i in range(9)]
	board.pop(0)
	board.insert(0, symbol)
	board.pop(4)
	board.insert(4, symbol)
	board.pop(8)
	board.insert(8, symbol)
	
	assert eng.check_winner(board, symbol)
	
	board = [i for i in range(9)]
	board.pop(2)
	board.insert(2, symbol)
	board.pop(5)
	board.insert(5, symbol)
	board.pop(8)
	board.insert(8, symbol)

