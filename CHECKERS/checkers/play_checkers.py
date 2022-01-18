import sys
sys.path.append('/home/oldest/my_projects/CHECKERS/checkers')
from checkers_board import *
import random
import time

class Game(object):
    def __init__(self, board, playerI, playerII):
        self.board = board
        self.playerI = playerI
        self.playerII = playerII
        self.winner = None
        self.winner_symbol = None

    def available_moves(self, board, board_numbers, player, enemy, current_p):
        # create a list with available moves for specified player
        # playerI is moving it's checkers from the bottom of the board
        # playerII vice-versa
        # this is why to check available places you have to add/remove to the current
        # position's index number 9 and 11
        # if the position is occupied by another player the function will check
        # next squares if beat move is possible
        available_moves = {}
        if (current_p in board_numbers
                and board[board_numbers.index(current_p)] == player.symbol):
            square = board_numbers.index(current_p)
            if player.kind == True:
                numI = 9
                numII = 11
            # opposite player is moving it's checkers in opposite direction
            # this is why numI and numII has negative value
            elif player.kind == False:
                numI = -9
                numII = -11

            x = square - numI
            # this if statement is making sure 
            # that new index place is in range of index board
            if x > 0 and x < 100 and board[x] == '   ':
                available_moves.update({x: None})
            # if beat move is available the dictionary available_moves will store
            # the places which have to be changed(removing enemy checker 
            # from the board) after choosing this position
            elif x > 0 and x < 100 and board[x] == enemy.symbol:
                y = x - numI
                if x > 0 and x < 100 and board[y] == '   ':
                    available_moves.update({y: x})
               
            x = square - numII
            if x > 0 and x < 100 and board[x] == '   ':
                available_moves.update({x: None})
            elif x > 0 and x < 100 and board[x] == enemy.symbol:
                y = x - numII
                if x > 0 and x < 100 and board[y] == '   ':
                    available_moves.update({y: x})

            x = square + numI
            if x > 0 and x < 100 and board[x] == enemy.symbol:
                y = x + numI
                if x > 0 and x < 100 and board[y] == '   ':
                    available_moves.update({y: x})
               
            x = square + numII
            if x > 0 and x < 100 and board[x] == enemy.symbol:
               y = x + numII
               if x > 0 and x < 100 and board[y] == '   ':
                   available_moves.update({y: x})
        
        return available_moves    
                                    

    def check_square(self, player, enemy, board):
        if player.type == True:
            # first the player is choosing the checker that want to move
            print('Choose checker that you want to move')
            current_p = input('> ').upper()
            # function self.available_moves is checking
            # available moves for the checker in choosen position
            # if choosen checker has no possibility to move
            # player has to choose the other checker
            targets = self.available_moves(board.board,
                                           board.board_numbers,
                                           player, 
                                           enemy, 
                                           current_p)
            
            while current_p not in board.board_numbers or targets == {}:
                print('Type correct place') 
                current_p = input('> ').upper()
                targets = self.available_moves(board.board,
                                               board.board_numbers, 
                                               player, 
                                               enemy, 
                                               current_p)
            
            print(f'Current position {current_p}\nChoose new position for your checker')
            # now player is choosing new position for choosen checker
            new_target = input('> ').upper()
            # if new position exists in available_moves
            # function make_move appends checker to new position
            
            while (new_target not in board.board_numbers 
                    or board.board_numbers.index(new_target) not in targets):
                print(f'You can\'t move into this position\nCurrent position {current_p}')
                new_target = input('> ').upper()
            
        elif player.type == False:
            # arificial player is choosing randomly from list 'board_numbers'
            current_p = random.choice(board.board_numbers)
            targets = self.available_moves(board.board,
                                               board.board_numbers, 
                                               player, 
                                               enemy, 
                                               current_p)
            
            while current_p not in board.board_numbers or targets == {}:
                current_p = random.choice(board.board_numbers)
                targets = self.available_moves(board.board,
                                               board.board_numbers, 
                                               player, 
                                               enemy, 
                                               current_p)
            
            new_target = random.choice(board.board_numbers)
            
            while (new_target not in self.board.board_numbers 
                    or board.board_numbers.index(new_target) not in targets):
                new_target = random.choice(board.board_numbers)
               

        new_target = board.board_numbers.index(new_target)
        current_p = board.board_numbers.index(current_p)
        
        return current_p, new_target, targets
        

    def make_move(self, player_x, player_y, board):
        current_p, new_target, targets = self.check_square(player_x, player_y, self.board)
        board.board.pop(current_p)
        board.board.insert(current_p, '   ')
        board.board.pop(new_target)
        board.board.insert(new_target, player_x.symbol)
        # new place is stored in dictionary 'targets' in form of key
        # if this key has value other than 'None' this mean that
        # value is a place(index number of the place) with enemy checker
        # that has to be remove from the board
        check = targets.get(new_target)
        if check != None:
            board.board.pop(targets[new_target])
            board.board.insert(targets[new_target], '   ')
            print(f'CHECKER {player_y.symbol} REMOVED FROM THE GAME')


    def check_winner(self, board, player, enemy):
        # this function is checking if all existing player checkers
        # reach positions(enmey origin positions) 
        # from no more moves can be done
        # the player who has more checkers is winning
        valid_square = []
        for count, value in enumerate(board):
            if value == player.symbol and count not in enemy.position:
                valid_square.append(count)
        x = board.count(player.symbol)
        y = board.count(enemy.symbol)
       
        if valid_square == []:
            if x > y:
                print(f'{player.name} is a winner!')
                self.winner = True
                self.winner_symbol = player.symbol
            
            elif x == y:
                print('Tie Tie Tie!')
                self.winner = True
                self.winner_symbol = None
            
            elif y > x:
                print(f'{enemy.name} is a winner!')
                self.winner = True
                self.winner_symbol = enemy.symbol

    def play(self):
        # finally this function starts run the game 
        winner_symbol = None
        while self.winner == None:
            print(f'{self.playerI.name} MOVE')
            self.board.print_board(self.board.board)
            self.make_move(self.playerI, self.playerII, self.board)
            self.check_winner(self.board.board, self.playerII, self.playerI)
            if self.winner == None:
                print(f'{self.playerII.name} MOVE')
                self.make_move(self.playerII, self.playerI, self.board) 
                self.board.print_board(self.board.board)
                time.sleep(2)
                self.check_winner(self.board.board, self.playerI, self.playerII)
        return self.winner_symbol


def play_checkers():
    winner = None
    while winner != ' & ':
        bOaRd = Board()
        human = Player(' & ', True, 'HUMAN PLAYER', True)
        artificial = Player(' # ', False, 'ARTIFICIAL PLAYER', False)
        human.set_player(bOaRd.board)
        artificial.set_player(bOaRd.board)
        gAmE = Game(bOaRd, human, artificial) 
        winner = gAmE.play()           




    





