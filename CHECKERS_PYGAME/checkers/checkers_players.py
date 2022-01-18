import pygame
import math
import random
import copy
import checkers_settings
from pygame.locals import *
from checkers_settings import *

class Player(object):
    def __init__(self, checker, board, select, kind, choice, sound):
        # keeps chosen type of game in main menu
        self.choice = choice
        # if self.kind is True the player is a human
        # otherwise the player is a computer player
        self.kind = kind
        # stores data of each square of the board in form of lists in list
        self.board = board
        # self.checker stores the type of player's checker
        self.checker = checker
        # if checker reach the last opposite row of the board
        # checker become queen
        self.queen = None
        # opposite checker
        self.opposite = None
        self.opposite_queen = None
        # numI and numII represent move value if player moves down the board
        # each square increase its position number by 7 or 9 
        # if player moves up the board square number is decreased
        # by these numbers
        self.numI = None
        self.numII = None
        # stores all possible moves for player checker and queeen
        self.moves = {}
        # self.choosen stores square number
        # and data of transformed square number to pixel coordination 
        self.choosen = None
        # lock function
        self.lock = False
        # keep origin position while looping in functions
        self.position = None
        # sequence of ordered diagonaly squares
        # that numbers differ themselfs by number 7
        self.diagonalsI = {}
        # sequence of ordered diagonaly squares
        # that numbers differ themselfs by number 9
        self.diagonalsII = {}
        # sequence of squares that represents move of checker 
        self.items = None
        # change deep for minmax algorithm
        self.number = 0
        self.set_up_common()
        self.available_moves()
        
    
    def set_up_common(self):
        if self.checker == 'black':
            self.queen = 'black queen'
            self.opposite = 'white'
            self.opposite_queen = 'white queen'
            self.numI = 7
            self.numII = 9
        
        elif self.checker == 'white':
            self.queen = 'white queen'
            self.opposite = 'black'
            self.opposite_queen = 'black queen'
            self.numI = -7
            self.numII = -9
    
    
    def search_diagonals(self, board):
        # this function finds two types of sequence
        # one of them is sequence that numbers differ themselfs by number 7 
        # and in second one numbers differ by number 9
        # each sequence is grouped in lists 
        # that represent their diagonal position on the board
        self.diagonalsI = {}
        self.diagonalsII = {}
        for tile in board:
            sequenceI = tile[0] % 7
            if sequenceI not in self.diagonalsI.keys():
                self.diagonalsI.update({sequenceI: []})
                self.diagonalsI[sequenceI].append(tile)
            elif sequenceI in self.diagonalsI.keys():
                if tile not in self.diagonalsI[sequenceI]:
                    self.diagonalsI[sequenceI].append(tile)
            sequenceII = tile[0] % 9
            if sequenceII not in self.diagonalsII.keys():
                self.diagonalsII.update({sequenceII: []})
                self.diagonalsII[sequenceII].append(tile)
            elif sequenceII in self.diagonalsII.keys():
                if tile not in self.diagonalsII[sequenceII]:
                    self.diagonalsII[sequenceII].append(tile)
        # set squares of diagonal in correct order
        for each in self.diagonalsI:
            self.diagonalsI[each].sort()
        for each in self.diagonalsII:
            self.diagonalsII[each].sort() 


    def available_moves(self):
        self.moves = {}
        for each in self.board:
            if each[1] == self.checker:
                # keeps origin position inside functions
                self.position = each[0]
                self.search_checker_moves(self.board, each[0], [], True)
            elif each[1] == self.queen:
                self.position = each[0]
                self.search_queen_move_down(9, self.board, each, 0, [])
                self.search_queen_move_up(9, self.board, each, 0, [])
                self.search_queen_move_down(7, self.board, each, 0, [])
                self.search_queen_move_up(7, self.board, each, 0, [])
        # if artificial player choose checker with max beaten checkers
        if self.kind == False:
            # select checkers with moves that have highest
            # number of beaten checkers
            current = (None, [])
            # find moves with max beaten checkers
            new = []
            for checker in self.moves:
                for moves in self.moves[checker]:
                    wins = [i for i in moves if i[1] != None]
                    if len(wins) > len(current[1]):
                        new = []
                        current = (checker, moves)
                        new.append(current)
                    elif len(wins) == len(current[1]):
                        new.append((checker, moves))
            self.moves = {}        
            for move in new:
                if move[0] not in self.moves:
                    self.moves[move[0]] = [move[1]]
                elif move[0] in self.moves:
                    self.moves[move[0]].append(move[1])            
            

    def search_checker_moves(self, board, origin, remove, add):
        # finds all possible moves for checker
        # function checks each square in board
        # if number of the square is in checkI or II or III or IV and complay 
        # with all requirements for next square to move
        # the square is added to the self.moves
        checkI = (self.numI, (origin + self.numI)) 
        checkII = (self.numII, (origin + self.numII))
        checkIII = (-self.numI, (origin + (-self.numI))) 
        checkIV = (-self.numII, (origin + (-self.numII)))
       
        for countI, each in enumerate(board):
            if each[0] == checkI[1] and each[1] == None and remove == []:
                self.update_moves(self.position, [(each[0], None)])
            elif each[0] == checkII[1] and each[1] == None and remove == []:
                self.update_moves(self.position, [(each[0], None)])
            
            elif (each[0] == checkI[1] 
                    and (each[1] == self.opposite or each[1] == self.opposite_queen) 
                    and checkI[1] not in [i[1] for i in remove]):
                winI = (self.numI, (each[0] + self.numI))
                for countII, win_tile in enumerate(board):
                    if win_tile[0] == winI[1] and win_tile[1] == None:
                        add = False
                        removeI = [i for i in remove]
                        removeI.append((win_tile[0], each[0]))
                        check_board = copy.deepcopy(board)
                        check_board[countI][1] = None
                        check_board[countII][1] = self.checker
                        if self.search_checker_moves(check_board, winI[1], removeI, True):
                            self.update_moves(self.position, removeI)
                        
            elif (each[0] == checkII[1] 
                    and (each[1] == self.opposite or each[1] == self.opposite_queen) 
                    and checkII[1] not in [i[1] for i in remove]):
                winII = (self.numII, (each[0] + self.numII))
                for countII, win_tile in enumerate(board):
                    if win_tile[0] == winII[1] and win_tile[1] == None:
                        add = False
                        removeI = [i for i in remove]
                        removeI.append((win_tile[0], each[0]))
                        check_board = copy.deepcopy(board)
                        check_board[countI][1] = None
                        check_board[countII][1] = self.checker
                        if self.search_checker_moves(check_board, winII[1], removeI, True):
                            self.update_moves(self.position, removeI)
                        
            elif (each[0] == checkIII[1] 
                    and (each[1] == self.opposite or each[1] == self.opposite_queen) 
                    and checkIII[1] not in [i[1] for i in remove]):
                winIII = (-self.numI, (each[0] + (-self.numI)))
                for countII, win_tile in enumerate(board):
                    if win_tile[0] == winIII[1] and win_tile[1] == None:
                        add = False
                        removeI = [i for i in remove]
                        removeI.append((win_tile[0], each[0]))
                        check_board = copy.deepcopy(board)
                        check_board[countI][1] = None
                        check_board[countII][1] = self.checker
                        if self.search_checker_moves(check_board, winIII[1], removeI, True):
                            self.update_moves(self.position, removeI)
                        
            elif (each[0] == checkIV[1] 
                    and (each[1] == self.opposite or each[1] == self.opposite_queen) 
                    and checkIV[1] not in [i[1] for i in remove]):
                winIV = (-self.numII, (each[0] + (-self.numII)))
                for countII, win_tile in enumerate(board):
                    if win_tile[0] == winIV[1] and win_tile[1] == None:
                        add = False
                        removeI = [i for i in remove]
                        removeI.append((win_tile[0], each[0]))
                        check_board = copy.deepcopy(board)
                        check_board[countI][1] = None
                        check_board[countII][1] = self.checker
                        if self.search_checker_moves(check_board, winIV[1], removeI, True):
                            self.update_moves(self.position, removeI)
        
        if add == True:
            return True
        else:
            return False    
                    

    def search_queen_move_down(self, seq, board, origin, deep, update):
        # finds all possible moves for checker_queen
        # this function check diagonals where squares numbers differ themselfs by number 7
        self.search_diagonals(board)
        deep += 1
        # switch diagonals if function is running recursively
        if seq == 7:
            diag = self.diagonalsI
            nex = 9
        else:
            diag = self.diagonalsII
            nex = 7
        # transform value of origin position to diagonal key
        key = origin[0] % seq
        diagonals = diag[key]
        # start checking from next square after origin[0] position
        # start checking down moves
        start = diagonals.index(origin) + 1
        end = len(diagonals)
        lock = True
        add = False
        # if win move is founded skip one loop
        wait_loop = False
        current_move = None
        # stores moves from current function deep level
        current_moves = []
        
        for value in range(start, end):
            if wait_loop == False:
                if diagonals[value][1] == None:
                    current_move = (diagonals[value][0], None)
                    current_moves.append((diagonals[value][0], None))
                    update.append((diagonals[value][0], None))
               
                elif(diagonals[value][1] == self.opposite
                         or diagonals[value][1] == self.opposite_queen):
                    # check next square
                    next = value + 1
                    if next < end:
                        if diagonals[next][1] == None:
                            current_move = (diagonals[next][0], diagonals[value][0])
                            current_moves.append((diagonals[next][0], diagonals[value][0]))
                            update.append((diagonals[next][0], diagonals[value][0]))
                            add = True
                            wait_loop = True

                        elif diagonals[next][1] != None:
                            break
                    
                elif diagonals[value][1] == self.checker or diagonals[value][1] == self.queen:
                    break
                # if win move founded check other diagonals
                if add == True:
                    check_board = copy.deepcopy(board)
                    self.update_check_board(check_board, origin, current_moves)
                    next_winI = self.search_queen_move_down(nex, check_board,
                                                            [current_move[0], self.queen],
                                                            deep, [i for i in update])
                    # count number of beaten checkers in checked diagonals
                    # if number is unchanged update moves
                    winI = len([i for i in next_winI if i[1] != None])
                    next_winII = self.search_queen_move_up(nex, check_board,
                                                           [current_move[0], self.queen],
                                                           deep, [i for i in update])
                    winII = len([i for i in next_winII if i[1] != None])
                    count_update = len([i for i in update if i[1] != None])
                    if winI == count_update and winII == count_update:
                        lock = False

            else:
                wait_loop = False
        
        if lock == False:
            count_wins = 0
            for count, move in enumerate(update):
                if move[1] != None:
                    count_wins += 1
                if count_wins == count_update:
                    self.update_moves(self.position, update[:count + 1])
            
        elif deep == 1 and lock == True and update != []:
            for count, move in enumerate(update):
                self.update_moves(self.position, update[:count + 1])

        return update
        
        
    def search_queen_move_up(self, seq, board, origin, deep, update):
        self.search_diagonals(board)
        deep += 1
        if seq == 7:
            diag = self.diagonalsI
            nex = 9
        else:
            diag = self.diagonalsII
            nex = 7
        key = origin[0] % seq
        diagonals = diag[key]
        start = diagonals.index(origin) - 1
        end = -1
        add = False
        lock = True
        wait_loop = False
        current_move = None
        current_moves = []
        for value in range(start, end, -1):
            if wait_loop == False:
                if diagonals[value][1] == None:
                    current_move = (diagonals[value][0], None)
                    current_moves.append((diagonals[value][0], None))
                    update.append((diagonals[value][0], None))
                    
                elif (diagonals[value][1] == self.opposite
                      or diagonals[value][1] == self.opposite_queen):
                    next = value - 1
                    if next > end:
                        if diagonals[next][1] == None:
                            current_move = (diagonals[next][0], diagonals[value][0])
                            current_moves.append((diagonals[next][0], diagonals[value][0]))
                            update.append((diagonals[next][0], diagonals[value][0]))
                            add = True
                            wait_loop = True
                            
                        elif diagonals[next][1] != None:
                            break
                    
                elif diagonals[value][1] == self.checker or diagonals[value][1] == self.queen:
                    break

                if add == True:
                    check_board = copy.deepcopy(board)
                    self.update_check_board(check_board, origin, current_moves)
                    next_winI = self.search_queen_move_down(nex, check_board,
                                                            [current_move[0], self.queen],
                                                            deep, [i for i in update])
                   
                    winI = len([i for i in next_winI if i[1] != None])
                    next_winII = self.search_queen_move_up(nex, check_board,
                                                           [current_move[0], self.queen],
                                                           deep, [i for i in update])
                    winII = len([i for i in next_winII if i[1] != None])
                    count_update = len([i for i in update if i[1] != None])
                    if winI == count_update and winII == count_update:
                        lock = False

            else:
                wait_loop = False
        
        if lock == False:
            count_wins = 0
            for count, move in enumerate(update):
                if move[1] != None:
                    count_wins += 1
                if count_wins == count_update:
                    self.update_moves(self.position, update[:count + 1])
            
        elif deep == 1 and lock == True and update != []:
            for count, move in enumerate(update):
                self.update_moves(self.position, update[:count + 1])

        return update
        
   
    def update_moves(self, checker, remove):
        if checker not in self.moves.keys():
            self.moves.update({checker: []})
            self.moves[checker].append(remove)
        elif checker in self.moves.keys():
            if remove not in self.moves[checker]:
                self.moves[checker].append(remove)
            
    
    def point_checker(self, click, mouse_x, mouse_y, b_oard, display):
        # this function locks choosen checker if choosen checker has any possible move
        if self.lock == False and click == True:
            free_squares = self.moves.keys()
            for each in self.board:
                if each[1] == self.checker or each[1] == self.queen:
                    row = math.floor(each[0] / 8)
                    column = each[0] % 8
                    pixel_x, pixel_y = b_oard.convert_tile_to_pixel(column, row, SQUARE)
                    checker = pygame.Rect(pixel_x, pixel_y, SQUARE, SQUARE)
                    if (checker.collidepoint(mouse_x, mouse_y)
                            and click == True and each[0] in free_squares):
                        self.highlight_checker((pixel_x, pixel_y), display)
                        each = tuple(each)
                        self.choosen = (each, (pixel_x, pixel_y))
                        self.lock = True
                    
        elif self.lock == True:
            pixel_x, pixel_y = self.choosen[1]
            checker = pygame.Rect(pixel_x, pixel_y, SQUARE, SQUARE)
            if checker.collidepoint(mouse_x, mouse_y) and click == True:
                self.lock = False
            else:
                self.highlight_checker(self.choosen[1], display)
         
    
    def highlight_checker(self, position, display):
        size = (80, 80)
        surface = pygame.Surface(size)
        surface.set_colorkey(BLACK)
        surface.fill(BLACK)
        surface.set_alpha(70)
        pygame.draw.circle(surface, HIGHLIGHT, (40, 40), 36, 4)
        display.blit(surface, position)

    
    def artificial_move(self):
        if self.choice == 'Easy Artificial Player':
            self.number += 1
            if self.number % 3 == 0:
                depth = 1
            else:
                depth = 2
            tree = Tree(depth, 0, self.board, 0, self.moves, self.checker, None)
            value, data = self.minmax(tree, depth, False)
             # if opposite player has not any possible move
            if data == None:
                keys = self.moves.keys()
                keys = list(keys)
                checker = random.choice(keys)
                target = random.choice(self.moves[checker])
                find_checker = [i for i in self.board if i[0] == checker]
                origin = tuple(find_checker[0])
            else:
                origin, target = data
           
        elif self.choice == 'Normal Artificial Player':
            self.number += 1
            if self.number % 8 == 0:
                depth = 1
            else:
                depth = 2
            tree = Tree(depth, 0, self.board, 0, self.moves, self.checker, None)
            value, data = self.minmax(tree, depth, False)
            if data == None:
                keys = self.moves.keys()
                keys = list(keys)
                checker = random.choice(keys)
                target = random.choice(self.moves[checker])
                find_checker = [i for i in self.board if i[0] == checker]
                origin = tuple(find_checker[0])
            else:
                origin, target = data
            
        elif self.choice == 'Tough Artificial Player':
            depth = 2
            tree = Tree(depth, 0, self.board, 0, self.moves, self.checker, None)
            value, data = self.minmax(tree, depth, False)
            if data == None:
                keys = self.moves.keys()
                keys = list(keys)
                checker = random.choice(keys)
                target = random.choice(self.moves[checker])
                find_checker = [i for i in self.board if i[0] == checker]
                origin = tuple(find_checker[0])
            else:
                origin, target = data              
                
        return origin, target
    
    # minmax algorithm    
    def minmax(self, item, depth, maximaizingPlayer):
        if depth == 0:
            # item.data stores origin position and checker's number 
            return item.value, item.data 

        if maximaizingPlayer:
            max_value = -1000000000
            # keep data of move in 'index' while looping
            index = None
            for i in range(len(item.children)):
                evalu, square= self.minmax(item.children[i], depth - 1, False)
                if evalu >= max_value:
                    index = square
                max_value = max(max_value, evalu) 
            
            return max_value, index
        
        else:
            min_value = 1000000000
            index = None
            for i in range(len(item.children)):
                evalu, square = self.minmax(item.children[i], depth - 1, True)
                if evalu <= min_value:
                    index = square
                min_value = min(min_value, evalu)
            return min_value, index
        
        return min_value, index
    
    
    def human_move(self, click, mouse_x, mouse_y, b_oard, display):
        # if checker is choosen get available moves for this checker
        # from dictionary self.moves
        for items in self.moves:
            if items == self.choosen[0][0]:
                win_first = self.moves[self.choosen[0][0]]
        # if move is a win move insert last win square at the beginning of the list
        # if not insert None
        # this solution keeps choosing squares alongside checkers rules 
        # beat all possible checker in the move
        for items in win_first:
            current_win = None
            # for each possible move
            for item in items:
                if item[1] != None:
                    current_win = item
            items.insert(0, current_win)
                               
        for items in win_first:
            current_win = items.pop(0)
            if current_win == None:
                for move in items:
                    row = math.floor(move[0] / 8)
                    column = move[0] % 8
                    pixel_x, pixel_y = b_oard.convert_tile_to_pixel(column, row, SQUARE)
                    square = pygame.Rect(pixel_x, pixel_y, SQUARE, SQUARE)
                    if square.collidepoint(mouse_x, mouse_y) and click == True:
                        moves = [move]
                        self.items = moves
                        return True
                            
            elif current_win != None:
                # allow get square only after finding all possible win moves
                start = False
                for count, move in enumerate(items):
                    if move == current_win:
                        start = True
                    if start == True:
                        row = math.floor(move[0] / 8)
                        column = move[0] % 8
                        pixel_x, pixel_y = b_oard.convert_tile_to_pixel(column, row, SQUARE)
                        square = pygame.Rect(pixel_x, pixel_y, SQUARE, SQUARE)
                        if square.collidepoint(mouse_x, mouse_y) and click == True:
                            self.items = items[:count + 1]
                            return True
          
        return False

    
    def check_win_checkers(self):
        # if checker in queen square transform checker to queen checker
        if self.checker == 'white':
            win_square = [i for i in range(1, 8)]
            win_checker = 'white queen'
            
        elif self.checker == 'black':
            win_square = [i for i in range(56, 64)]
            win_checker = 'black queen'
            
        for each in self.board:
            if (each[0] in win_square
                    and each[1] == self.checker):
                each[1] = win_checker
                
    
    def update_check_board(self, check_board, origin, moves):
        last_move = moves.pop()
        for move in moves:    
            for each in check_board:
                if each[0] == move[1]:
                    each[1] = None
        
        for each in check_board:
            if each[0] == origin[0]:
                each[1] = None
            elif each[0] == last_move[0]:
                each[1] = origin[1]
            elif each[0] == last_move[1]:
                each[1] = None
        
        moves.append(last_move)
        
    
    def count_checkers(self, board):
        white = 0
        black = 0
        for each in board:
            if each[1] == 'white' or each[1] == 'white queen':
                white += 1
            elif each[1] == 'black' or each[1] == 'black queen':
                black += 1
        return str(white), str(black)
                    
                
class Tree(object):
    def __init__(self, depth, value, board, num, moves, checker, data):
        self.depth = depth 
        self.value = value 
        self.board = board
        self.moves = moves
        self.checker = checker
        self.children = []
        self.num = num
        self.data = data
        self.make_children()
        
        
    def make_children(self):
        if self.depth >= 0:
            for checker in self.moves:
                #print(self.value, 'hahahahahahaahah')
                for move in self.moves[checker]:
                    # create copy of the board
                    copy_board = copy.deepcopy(self.board)
                    # get origin data (position, type of checker) from move
                    origin = [i for i in self.board if i[0] == checker]
                    # keep data in origin unchangeable - transform list to tuple
                    origin = tuple(origin[0])
                    self.checker = origin[1]
                    # keep origin of the move in self.data
                    if self.num == 0:
                        self.data = (origin, move)
                        
                    if self.checker == 'white':
                        # create new player object for testing next moves
                        test_player = Player('black', copy_board, None, False, None, None)
                        # update board to check value of the move
                        test_player.update_check_board(test_player.board, origin, move)
                        # get value of move
                        white, black = test_player.count_checkers(test_player.board)
                        value = (100 * int(white)) - (100 * int(black)) 
                        # check if there is a new queen
                        test_player.check_win_checkers()
                    else:
                        test_player = Player('white', copy_board, None, False, None, None)
                        test_player.update_check_board(test_player.board, origin, move)
                        white, black = test_player.count_checkers(test_player.board)
                        value = (100 * int(white)) - (100 * int(black))
                        test_player.check_win_checkers()
                    # check next moves    
                    test_player.available_moves()
                    self.children.append(Tree(self.depth - 1,
                                              value,
                                              test_player.board,
                                              self.num + 1,
                                              test_player.moves,
                                              test_player.checker,
                                              self.data))
                
                    
                
        
            
            
                
        
                
            
            
                     
            
        
            
    
        
        
