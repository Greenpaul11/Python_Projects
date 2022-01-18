import random
import math

class Board_Tic_Tac_Toe(object):
	
	def __init__(self):
		self.board = [' ' for i in range(9)]
		self.board_numbers = []
		
	def print_board(self):
		for row in [self.board[i * 3: (i +1) * 3] for i in range(3)]:
			print('| ' + ' | '.join(row) + ' |')
			
	def print_board_numbers(self):
		for count, value in enumerate(self.board):
			self.board_numbers.append(str(count))
			
		for row in [self.board_numbers[i * 3: (i + 1) * 3] for i in range(3)]:
			print('| ' + ' | '.join(row) + ' |')
			
	def winner_checker(self, answer, letter):
		# horizontal rules
		choice = math.floor(answer / 3)						
		check = self.board[choice * 3: (choice + 1) * 3]
		if all([item == letter for item in check]):
			print(f'Player {letter} Is A Winner')
			return True
		# vertical rules
		choice = answer % 3
		check = [self.board[choice + (i * 3)] for i in range(3)]
		if all([item == letter for item in check]):
			print(f'Player {letter} Is A Winner')
			return True
		#diagonal rule I
		choice = answer % 2
		check = [self.board[i] for i in [2, 4, 6]]
		if all([item == letter for item in check]):
			print(f'Player {letter} Is A Winner')
			return True
		#diagonal rule II
		choice = answer % 2
		check = [self.board[i] for i in [0, 4, 8]]	
		if all([item == letter for item in check]):
			print(f'Player {letter} Is A Winner')
			return True
		

class Player(object):
	
	def __init__(self, letter, winner):
		self.letter = letter
		self.winner = winner
		

class HumanoidPlayer(Player):
	
	def human_player(self, board):
		answer = int(input('> '))
		while answer not in [i for i in range(9)] or board[answer] != ' ':
			print('Wrong place Choose another')
			answer = int(input('> '))
		board.pop(answer)
		board.insert(answer, self.letter)
		return answer


class ComputerPlayer(Player):
	
	def computer_player(self, board):
		board_check = []
		for caunt, value in enumerate(board):
			board_check.append((caunt, value))	
		count, value = random.choice(board_check)
		while ' ' not in value:
			count, value = random.choice(board_check)
		board.pop(count)
		board.insert(count, self.letter)
		return count



def play_game(board, player_X, player_O):
	while player_X.winner == False:
		player_O.winner = False
		board.board = [' ' for i in range(9)]
		board.print_board_numbers()
		
		while ' ' in board.board and player_X.winner == False and player_O.winner == False:
			if player_X.winner == False and ' ' in board.board:
				print('Alien player move')
				answer = player_O.computer_player(board.board)
				board.print_board()
				if board.winner_checker(answer, 'O'):
					player_O.winner = True
				
			if player_O.winner == False and ' ' in board.board:
				print('Human player move')
				answer = player_X.human_player(board.board)
				board.print_board()
				if board.winner_checker(answer, 'X'):
					player_X.winner = True
				
		if ' ' not in board.board:
			print('No more place to game')	
			
def play_tictactoe():
	person = HumanoidPlayer('X', False)
	computer = ComputerPlayer('O', False)
	board = Board_Tic_Tac_Toe()
	play_game(board, person, computer)



	

