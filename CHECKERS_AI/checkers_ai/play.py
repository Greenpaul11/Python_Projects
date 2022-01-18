from checkers_board import *
import random
import time
import copy
from sys import maxsize

class Game(object):
    def __init__(self, board, playerI, playerII):
        self.board = board
        self.playerI = playerI
        self.playerII = playerII
        self.winner = None
    
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
                                    
    def check_square(self, player, enemy, board, available_moves):
        if player.type == True:
            # first the player is choosing the checker that want to move
            print('Choose checker that you want to move')
            current_p = input('> ').upper()
            # function self.available_moves is checking
            # available moves for the checker in choosen position
            # if choosen checker has no possibility to move
            # player has to choose the other checker
            targets = available_moves(board.board,
                                      board.board_numbers,
                                      player, 
                                      enemy, 
                                      current_p)
            
            while current_p not in board.board_numbers or targets == {}:
                print('Type correct place') 
                current_p = input('> ').upper()
                targets = available_moves(board.board,
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
            
            new_target = board.board_numbers.index(new_target)
            current_p = board.board_numbers.index(current_p)
            
        elif player.type == False:
            g_ame = Game(self.board, self.playerI, self.playerII)
            if player.kind == True:
            	num = 1
            	maximax = True
            else:
            	num = -1
            	maximax = False
            tree = Tree(g_ame, 1, 0, board.board, num, 1, None)
            value, position = self.minmax(tree, tree.depth, maximax)
            current_p, new_target = position
            q = board.board_numbers[current_p]
            targets = available_moves(board.board,
                                      board.board_numbers,
                                      player, 
                                      enemy, 
                                      q)
        
        return current_p, new_target, targets
        
    
    def make_move(self, player_x, player_y, board):
        score = 0
        current_p, new_target, targets = self.check_square(player_x, 
                                                           player_y, 
                                                           self.board, 
                                                           self.available_moves)
        board.board.pop(current_p)
        board.board.insert(current_p, '   ')
        board.board.pop(new_target)
        board.board.insert(new_target, player_x.symbol)
        square = board.board_numbers[new_target]
        print(f'CHECKER {player_x.symbol} MOVED ON {square}') 
        # new place is stored in dictionary 'targets' in form of key
        # if this key has value other than 'None' this mean that
        # value is a place(index number of the place) with enemy checker
        # that has to be remove from the board
        check = targets.get(new_target)
        if check != None:
            board.board.pop(targets[new_target])
            board.board.insert(targets[new_target], '   ')
            print(f'CHECKER {player_y.symbol} REMOVED FROM THE GAME')
            score += 100
        
        return score
          
    
    def minmax(self, position, depth, maximaizingPlayer):
        # if set depth reach 0 level the value from the last child is returned
        # in this case each branch of the tree stores also the position value
        if depth == 0:
            return position.value, position.position 
        # if variable maximaizingPlayer is set to True    
        if maximaizingPlayer:
            # max_value is set to such big number becaus when the 'Tree' has
            # big depth the value of children can also reach enormous numbers
            max_value = -maxsize
            index = None
            # iterate through all children in the Tree
            for i in range(len(position.children)):
                # now minmax is called agian 
                # this function will end in this moment till it reach depth == 0
                # evalu is a value which is returned
                # square is a origin position from this value came
                evalu, square= self.minmax(position.children[i], depth - 1, False)
                # this if statment allows to change also 'position value' if 
                # max_value is changed
                if evalu >= max_value:
                    index = square
                max_value = max(max_value, evalu) 
            
            return max_value, index
        
        else:
            min_value = maxsize
            index = None
            for i in range(len(position.children)):
                evalu, square = self.minmax(position.children[i], depth - 1, True)
                if evalu <= min_value:
                    index = square
                min_value = min(min_value, evalu)
            return min_value, index
        
        return min_value, index
            
    
    def check_winner(self, board, player, enemy, state):
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
       
        if valid_square == [] and state == True:
            
            if x > y:
                print(f'{player.name} is a winner!')
                self.winner = True             
            
            elif x == y:
                print('Tie Tie Tie!')
                self.winner = True
            
            elif y > x:
                print(f'{enemy.name} is a winner!')
                self.winner = True
        
    
    def play(self):
        # finally this function starts run the game 
        while self.winner == None:
            print(f'{self.playerI.name} MOVE')
            self.board.print_board(self.board.board)
            self.make_move(self.playerI, self.playerII, self.board)
            self.check_winner(self.board.board, self.playerII, self.playerI, True)
            if self.winner == None:
                print(f'{self.playerII.name} MOVE')
                self.make_move(self.playerII, self.playerI, self.board) 
                self.board.print_board(self.board.board)
                time.sleep(2)
                self.check_winner(self.board.board, self.playerI, self.playerII, True)
            
            
class Tree(object):
    def __init__(self, game, depth, value, board, player_N, num, position):
        self.game = game
        self.depth = depth 
        self.value = value 
        self.board = board
        self.player_N = player_N
        self.children = []
        self.num = num
        self.position = position
        self.make_children()
        
    def check_move(self, player_x, player_y, count, move, board, moves):
        score = 0
        board.pop(count)
        board.insert(count, '   ')
        board.pop(move)
        board.insert(move, player_x.symbol)
        if moves[move] != None:
            board.pop(moves[move])
            board.insert(moves[move], '   ')
            # each beat move is giving 100 points
            score += 100 
        return score
        
    def make_children(self):
        if self.player_N == 1:
            player_x = self.game.playerI
            player_y = self.game.playerII
        elif self.player_N == -1:
            player_x = self.game.playerII
            player_y = self.game.playerI
            
        if self.depth >= 0:
            for count, checker in enumerate(self.board):
                # create copy of the board that allows to check
                # each possible move
                new_board = copy.copy(self.board) 
                if checker == player_x.symbol:
                    square = self.game.board.board_numbers[count]
                    moves = self.game.available_moves(new_board,
                                       self.game.board.board_numbers,
                                       player_x, 
                                       player_y, 
                                       square)
                    if moves != {}:
                        for move in moves:
                            copy_board = copy.copy(self.board)
                            # statment below is allowing to store 
                            # origin position of each possible move
                            if self.num == 1:
                                self.position = (count, move)
                                self.value = 0
                                value = self.check_move(player_x,
                                                        player_y,
                                                        count, 
                                                        move, 
                                                        copy_board, 
                                                        moves)
                                value = value * self.player_N
                                self.value = self.value + value
    
                            else:
                                value = self.check_move(player_x, 
                                                        player_y, 
                                                        count, 
                                                        move, 
                                                        copy_board, 
                                                        moves)
                                value = value * self.player_N
                                self.value = self.value + value
                                
                            self.game.check_winner(copy_board, player_x, player_y, False)
                            self.children.append(Tree(self.game, 
                                                      self.depth - 1,
                                                      self.value,
                                                      copy_board,
                                                      self.player_N * -1,
                                                      0,
                                                      self.position))



def play_checkers_ai():
    bOaRd = Board()
    human = Player(' & ', True, 'HUMAN PLAYER', True)
    artificial = Player(' # ', False, 'ARTIFICIAL PLAYER', False)
    human.set_player(bOaRd.board)
    artificial.set_player(bOaRd.board)               
    gAmE = Game(bOaRd, human, artificial)
    gAmE.play()

play_checkers_ai()

