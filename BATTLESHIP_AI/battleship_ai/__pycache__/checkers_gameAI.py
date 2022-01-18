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
                                    
    def check_square(self, player, board):
        if player.kind == True:
            # first the player is choosing the checker that want to move
            print('Choose checker that you want to move')
            current_p = input('> ').upper()
            # function self.available_moves is checking
            # available moves for the checker in choosen position
            # if choosen checker has no possibility to move
            # player has to choose the other checker
            targets = self.available_moves(board.board,
                                           board.board_numbers,
                                           self.playerI, 
                                           self.playerII, 
                                           current_p)
            while current_p not in board.board_numbers or targets == {}:
                print('Type correct place') 
                current_p = input('> ').upper()
                targets = self.available_moves(board.board,
                                               board.board_numbers, 
                                               self.playerI, 
                                               self.playerII, 
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
            
        elif player.kind == False:
            tree = Tree(1, 0, board.board, -1, 1, None)
            value, position = self.minmax(tree, tree.depth, False)
            current_p, new_target = position
            q = board.board_numbers[current_p]
            targets = self.available_moves(board.board,
                                           board.board_numbers,
                                           self.playerII, 
                                           self.playerI, 
                                           q)
        return current_p, new_target, targets
        
    def make_move(self, player_x, player_y, board):
        score = 0
        current_p, new_target, targets = self.check_square(player_x, self.board)
        board.board.pop(current_p)
        board.board.insert(current_p, '   ')
        board.board.pop(new_target)
        board.board.insert(new_target, player_x.symbol)
        # new place is stored in dictionary 'targets' in form of key
        # if this key has value other than 'None' this mean that
        # value is a place(index number of the place) with enemy checker
        # that has to be remove from the board
        if targets[new_target] != None:
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
                quit()
            elif x == y:
                print('Tie Tie Tie!')
                quit()
            elif y > x:
                print(f'{enemy.name} is a winner!')
                quit()
        
    def play(self):
        # finally this function starts run the game 
        while True:
            print(f'{human.name} MOVE')
            bOaRd.print_board(bOaRd.board)
            self.make_move(self.playerI, self.playerII, self.board)
            self.check_winner(self.board.board, self.playerII, self.playerI, True)
            print(f'{artificial.name} MOVE')
            self.make_move(self.playerII, self.playerI, self.board) 
            bOaRd.print_board(bOaRd.board)
            time.sleep(2)
            self.check_winner(self.board.board, self.playerI, self.playerII, True)
            
            
class Tree(object):
    def __init__(self, depth, value, board, player_N, num, position):
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
            player_x = human
            player_y = artificial
        elif self.player_N == -1:
            player_x = artificial
            player_y = human
            
        if self.depth >= 0:
            for count, checker in enumerate(self.board):
                # create copy of the board that allows to check
                # each possible move
                new_board = copy.copy(self.board) 
                if checker == player_x.symbol:
                    square = bOaRd.board_numbers[count]
                    moves = gAmE.available_moves(new_board,
                                                 bOaRd.board_numbers,
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
                                
                            gAmE.check_winner(copy_board, player_x, player_y, False)
                            self.children.append(Tree(self.depth - 1,
                                              self.value,
                                              copy_board,
                                              self.player_N * -1,
                                              0,
                                              self.position))


bOaRd = Board()
human = Player(' & ', True, 'HUMAN PLAYER')
artificial = Player(' # ', False, 'ARTIFICIAL PLAYER')
human.set_player(bOaRd.board)
artificial.set_player(bOaRd.board)               
gAmE = Game(bOaRd, human, artificial)
gAmE.play()


