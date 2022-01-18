from nose.tools import *
import sys
sys.path.append('/home/oldest/my_projects/TICTACTOE/tictactoe')
from tictactoe_game import *


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
		
def test_player():
	board = Board_Tic_Tac_Toe()
	player = ComputerPlayer('O', False)
	for move in range(4):
		player.computer_player(board.board)
	assert_equal(4, board.board.count('O'))
	
def test_game():
	board = Board_Tic_Tac_Toe()
	playerI = ComputerPlayer('O', False)
	playerII = ComputerPlayer('X', False)
	while ' ' in board.board and playerI.winner == False and playerII.winner == False:
		answer = playerI.computer_player(board.board)
		if board.winner_checker(answer, 'O'):
			playerI.winner = True
		if playerI.winner == False and ' ' in board.board:
			answer = playerII.computer_player(board.board)
			if board.winner_checker(answer, 'X'):
				playerII.winner = True
	
		
