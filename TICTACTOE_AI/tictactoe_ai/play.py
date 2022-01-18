import random
import math
from sys import maxsize
import copy
import time

class Board_Tic_Tac_Toe(object):
    
    def __init__(self):
        self.board = [' ' for i in range(9)]
        self.board_numbers = [(count, value) for count, value in enumerate(self.board)]
    
    def list(self):
        return self.board   
        
    def print_board(self):
        for row in [self.board[i * 3: (i +1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
    
    def print_board_numbers(self):
        numbers = [str(count) for count, value in enumerate(self.board)]    
        for row in [numbers[i * 3: (i + 1) * 3] for i in range(3)]:
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
    
    def __init__(self, letter):
        self.letter = letter
        
    def human_player(self, board):
        answer = int(input('> '))
        while board[answer] != ' ':
            print('This place is already used. Choose another')
            answer = int(input('> '))
        board.pop(answer)
        board.insert(answer, self.letter)
        return answer

class Tree():
    def __init__(self, depth, player_N, board, num, position, value):
        
        self.depth = depth
        self.player_N = player_N
        self.value = value
        self.board = board
        self.children = []
        self.position = position
        self.num = num
        self.make_children()
        
    def make_children(self):
        if self.player_N == 1:
            letter = 'X'
            opposite_l = 'O'
        elif self.player_N == -1:
            letter = 'O'
            opposite_l = 'X'
        en_board = [count for count, value in enumerate(self.board) if value == ' ']
        
        if self.depth >= 0:
            for i in en_board:
                if self.num == 1:
                    self.position = i
                    self.value = 0
                check_board = [i for i in self.board]
                check_board.pop(i)
                check_board.insert(i, letter)
                self.value = self.true_value(i, check_board, letter, opposite_l)
                self.children.append(
                        Tree(self.depth - 1, 
                        -self.player_N, 
                        check_board,
                        0,
                        self.position,
                        self.value
                        ))
            
    def true_value(self, answer, board, letter, opposite_l):
        choice = math.floor(answer / 3)                 
        check = board[choice * 3: (choice + 1) * 3]
        if all([item == letter for item in check]):
            self.value += 10000000
        if check.count(letter) == 2 and check.count(' ') == 1:
            self.value += 500000
        if check.count(letter) == 1 and check.count(' ') == 2:
            self.value += 200000
        
        choice = answer % 3
        check = [board[choice + (i * 3)] for i in range(3)]
        if all([item == letter for item in check]):
            self.value += 10000000
        if check.count(letter) == 2 and check.count(' ') == 1:
            self.value += 500000
        if check.count(letter) == 1 and check.count(' ') == 2:
            self.value += 200000
        
        choice = answer % 2
        check = [board[i] for i in [2, 4, 6]]
        if all([item == letter for item in check]):
            self.value += 10000000
        if check.count(letter) == 2 and check.count(' ') == 1:
            self.value += 500000
        if check.count(letter) == 1 and check.count(' ') == 2:
            self.value += 200000
        
        choice = answer % 2
        check = [board[i] for i in [0, 4, 8]]   
        if all([item == letter for item in check]):
            self.value += 10000000
        if check.count(letter) == 2 and check.count(' ') == 1:
            self.value += 500000
        if check.count(letter) == 1 and check.count(' ') == 2:
            self.value += 200000 
        
        self.value = self.value * self.player_N

        return self.value
        
        
def minmax(position, depth, maximizingPlayer):
    if depth == 0 or abs(position.value) == 10000000:
        return position.value, position.position
        
    if maximizingPlayer:
        max_value = -maxsize
        index = None
        for i in range(len(position.children)):
            evalu, square= minmax(position.children[i], depth - 1, False)
            if evalu >= max_value:
                index = square
            max_value = max(max_value, evalu) 
        return max_value, index
        
    else:
        min_value = maxsize
        index = None
        for i in range(len(position.children)):
            evalu, square = minmax(position.children[i], depth - 1, True)
            if evalu <= min_value:
                index = square
            min_value = min(min_value, evalu)
        return min_value, index
        
    return min_value, index
        

def play_game(board, player_X):
    maximizingPlayer = False
    winner_X = False
    winner_O = False
    board.print_board_numbers()
    depth = 1
    player_N = -1
    states = [i for i in range(0,9)]
    
    while ' ' in board.board and winner_X == False and winner_O == False:
        if winner_O == False and ' ' in board.board:
            time.sleep(1)
            print('Human player move')
            answer = player_X.human_player(board.board)
            board.print_board()
            if board.winner_checker(answer, 'X'):
                winner_X = True
        
        if winner_X == False and ' ' in board.board:
            t = Tree(depth, player_N, board.list(), 1, None, 0)
            time.sleep(1)
            print('Alien player move')
            time.sleep(2)
            evalu,q  = minmax(t, t.depth, maximizingPlayer)
            board.board.pop(q)
            board.board.insert(q, 'O')
            board.print_board()
            if board.winner_checker(q, 'O'):
                winner_O = True     
        
        if ' ' not in board.board:
            print('No more place for play') 

def play_tictactoe_ai():            
	h = Player('X')
	b = Board_Tic_Tac_Toe()
	play_game(b, h)     
    

play_tictactoe_ai()



    

