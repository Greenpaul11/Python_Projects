import pygame
import math
import random
import copy
import checkers_settings
from pygame.locals import *
from checkers_settings import *

class Player(object):
    def __init__(self, checker, board, select, kind, choice):
        self.choice = choice
        # if self.kind is True the player is a human other ways the player is a computer
        self.kind = kind
        self.board = board
        # self.checker stores the image of player's checker
        self.checker = checker
        # if checker reach the last opposite row of the board checker become queen
        self.queen = None
        # opposite checker
        self.opposite = None
        self.opposite_queen = None
        # numI and numII represent move value if player moves down the board
        # each square increase its position number by 7 or 9 
        # if player moves up the board square number is decreased by these numbers
        self.numI = None
        self.numII = None
        # stores all possible moves for player checker and queeen
        self.moves = {}
        # self.choosen stores square number, checker data
        # and transformed square number to pixel coordination 
        self.choosen = None
        # lock function
        self.lock = False
        # keep origin position while looping in functions
        self.position = None
        # sequence of ordered diagonaly squares that numbers differ themselfs by number 7
        self.diagonalsI = {}
        # sequence of ordered diagonaly squares that numbers differ themselfs by number 9
        self.diagonalsII = {}
        self.time = 0
        self.set_up_common()
        self.available_moves()
        
    
    def set_up_common(self):
        if self.checker == self.board.black:
            self.queen = self.board.black_queen
            self.opposite = self.board.white
            self.opposite_queen = self.board.white_queen
            self.numI = 7
            self.numII = 9
        
        elif self.checker == self.board.white:
            self.queen = self.board.white_queen
            self.opposite = self.board.black
            self.opposite_queen = self.board.black_queen
            self.numI = -7
            self.numII = -9
    
    
    def search_diagonals(self, board):
        '''This function finds two types of sequence.
        One of them is sequence that numbers differ themselfs by number 7 
        and in second one numbers differ by number 9.
        Each sequence is grouped in lists 
        that represent their diagonal position on the board.'''
        
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
                
   
    def available_moves(self):
        self.moves = {}
        for each in self.board.board:
            if each[1] == self.checker:
                # self.position stores the value of the orginal position of the checker or queen
                self.position = each[0]
                self.search_checker_moves(self.board.board, each[0], [], True)
            elif each[1] == self.queen and each[1] != None:
                self.search_diagonals(self.board.board)
                self.position = each[0]
                self.search_queen_move_diagI(self.board.board, each, [None, []], False)
                self.search_queen_move_diagII(self.board.board, each, [None, []], False)
                
    
    def search_checker_moves(self, board, origin, remove, add):
        '''Finds all possible moves for checker.
        Function checks each square in board.
        If number of the square is in checkI or II or III or IV and complay 
        with all requirements for next square to move the square is added to the self.moves.'''
        
        checkI = (self.numI, (origin + self.numI)) 
        checkII = (self.numII, (origin + self.numII))
        checkIII = (-self.numI, (origin + (-self.numI))) 
        checkIV = (-self.numII, (origin + (-self.numII)))
       
        for countI, each in enumerate(board):
            if each[0] == checkI[1] and each[1] == None and remove == []:
                self.update_moves(self.position, each[0], [])
            elif each[0] == checkII[1] and each[1] == None and remove == []:
                self.update_moves(self.position, each[0], [])
            
            elif (each[0] == checkI[1]
                    and (each[1] == self.opposite or each[1] == self.opposite_queen) 
                    and checkI[1] not in remove):
                winI = (self.numI, (each[0] + self.numI))
                for countII, win_tile in enumerate(board):
                    if win_tile[0] == winI[1] and win_tile[1] == None:
                        add = False
                        removeI = [i for i in remove]
                        removeI.append(each[0])
                        check_board = copy.deepcopy(board)
                        check_board[countI][1] = None
                        check_board[countII][1] = self.checker
                        # if win move is founded function will run recursively until won't find any win move
                        if self.search_checker_moves(check_board, winI[1], removeI, True):
                            self.update_moves(self.position, winI[1], removeI)
                        
            elif (each[0] == checkII[1] 
                    and (each[1] == self.opposite or each[1] == self.opposite_queen) 
                    and checkII[1] not in remove):
                winII = (self.numII, (each[0] + self.numII))
                for countII, win_tile in enumerate(board):
                    if win_tile[0] == winII[1] and win_tile[1] == None:
                        add = False
                        removeI = [i for i in remove]
                        removeI.append(each[0])
                        check_board = copy.deepcopy(board)
                        check_board[countI][1] = None
                        check_board[countII][1] = self.checker
                        if self.search_checker_moves(check_board, winII[1], removeI, True):
                            self.update_moves(self.position, winII[1], removeI)
                        
            elif (each[0] == checkIII[1] 
                    and (each[1] == self.opposite or each[1] == self.opposite_queen) 
                    and checkIII[1] not in remove):
                winIII = (-self.numI, (each[0] + (-self.numI)))
                for countII, win_tile in enumerate(board):
                    if win_tile[0] == winIII[1] and win_tile[1] == None:
                        add = False
                        removeI = [i for i in remove]
                        removeI.append(each[0])
                        check_board = copy.deepcopy(board)
                        check_board[countI][1] = None
                        check_board[countII][1] = self.checker
                        if self.search_checker_moves(check_board, winIII[1], removeI, True):
                            self.update_moves(self.position, winIII[1], removeI)
                        
            elif (each[0] == checkIV[1] 
                    and (each[1] == self.opposite or each[1] == self.opposite_queen) 
                    and checkIV[1] not in remove):
                winIV = (-self.numII, (each[0] + (-self.numII)))
                for countII, win_tile in enumerate(board):
                    if win_tile[0] == winIV[1] and win_tile[1] == None:
                        add = False
                        removeI = [i for i in remove]
                        removeI.append(each[0])
                        check_board = copy.deepcopy(board)
                        check_board[countI][1] = None
                        check_board[countII][1] = self.checker
                        if self.search_checker_moves(check_board, winIV[1], removeI, True):
                            self.update_moves(self.position, winIV[1], removeI)
        
        if add == True:
            return True
        else:
            return False    
                    

    def search_queen_move_diagI(self, board, origin, current_win, search):
        '''Finds all possible moves for checker_queen.
        This function check diagonals where squares numbers differ themselfs by number 7.'''
        # transform value of origin position to diagonal key
        key = origin[0] % 7
        diagonals = self.diagonalsI[key]
        # start checking from next square after origin[0] position
        # start checking down moves
        start = diagonals.index(origin) + 1
        # check all squares in specified diagonal by key value
        end = len(diagonals)
        # stores opposite checkers added after win moves 
        remove = []
        # track win move
        add = False
        # keep value for new positions and removed checkers
        select = []
        # current win stores values for move done before current move
        if current_win != [None, []]:
            remove = current_win[1]
        # if win move is founded skip one loop
        wait_loop = False
        for value in range(start, end):
            if wait_loop == False:
                if diagonals[value][1] == None and add == False and remove == []:
                    select.append([diagonals[value][0], []])

                elif diagonals[value][1] == None and add == True: 
                    select.append([diagonals[value][0], [i for i in remove]])
            
                elif ((diagonals[value][1] == self.opposite or diagonals[value][1] == self.opposite_queen) 
                        and diagonals[value][0] not in remove):
                    # check next square
                    print(diagonals[value][0])
                    print(remove, 'remove')
                    next = value + 1
                    if next < end:
                        if diagonals[next][1] == None: 
                            if remove == []:
                                select = [[diagonals[next][0], [diagonals[value][0]]]]
                                remove = select[0][1]
                            else:
                                select = [[diagonals[next][0], remove]]
                                select[0][1].append(diagonals[value][0])
                                remove = select[0][1]
                            wait_loop = True
                            add = True
                            search = True
                        elif diagonals[next][1] != None:
                            break
                
                elif diagonals[value][1] == self.checker or diagonals[value][1] == self.queen:
                    break
            else:
                wait_loop = False
        
        for move in select:
            if move[1] != [] and add == True and search == True:
                # if win move is done function will run again with values from that move
                # if there is not any win move self.moves is updated
                check_board = copy.deepcopy(board)
                self.update_board(check_board, move, origin)
                if not self.search_queen_move_diagII(check_board, [move[0], None], move, False):
                    self.update_moves(self.position, move[0], move[1])
                
            elif move[1] == [] and current_win == [None, []]:
                self.update_moves(self.position, move[0], move[1])
            
        # start checking up moves
        start = diagonals.index(origin) - 1
        end = -1
        remove = []
        add =  False
        select = []
        if current_win != [None, []]:
            remove = current_win[1]
        wait_loop = False
        for value in range(start, end, -1):
            if wait_loop == False:
                if diagonals[value][1] == None and add == False and remove == []:
                    select.append([diagonals[value][0], []])

                elif diagonals[value][1] == None and add == True: 
                    select.append([diagonals[value][0], [i for i in remove]])
            
                elif ((diagonals[value][1] == self.opposite or diagonals[value][1] == self.opposite_queen) 
                        and diagonals[value][0] not in remove):
                    next = value - 1
                    if next > end:
                        if diagonals[next][1] == None: 
                            if remove == []:
                                select = [[diagonals[next][0], [diagonals[value][0]]]]
                                remove = select[0][1]
                            else:
                                select = [[diagonals[next][0], remove]]
                                select[0][1].append(diagonals[value][0])
                                remove = select[0][1]
                            wait_loop = True
                            add = True
                            search = True
                        elif diagonals[next][1] != None:
                            break
                
                elif diagonals[value][1] == self.checker or diagonals[value][1] == self.queen:
                    break
            else:
                wait_loop = False
        
        for move in select:
            if move[1] != [] and add == True and search == True:
                check_board = copy.deepcopy(board)
                self.update_board(check_board, move, origin)
                if not self.search_queen_move_diagII(check_board, [move[0], None], move, False):
                    self.update_moves(self.position, move[0], move[1])
                    
            elif move[1] == [] and current_win == [None, []]:
                self.update_moves(self.position, move[0], move[1])
        
        # if there is any win move function returns True
        if search == True:
            return True
        else:
            return False
            
            
    def search_queen_move_diagII(self, board, origin, current_win, search):
        '''Finds all possible moves for checker_queen.
        This function check diagonals where squares numbers differ themselfs by number 9.'''                
        
        key = origin[0] % 9
        diagonals = self.diagonalsII[key]
        start = diagonals.index(origin) + 1
        end = len(diagonals)
        remove = []
        add = False
        select = []     
        if current_win != [None, []]:
            remove = current_win[1]
        wait_loop = False
        for value in range(start, end):
            if wait_loop == False:
                if diagonals[value][1] == None and add == False and remove == []:
                    select.append([diagonals[value][0], []])

                elif diagonals[value][1] == None and add == True: 
                    select.append([diagonals[value][0], [i for i in remove]])
            
                elif ((diagonals[value][1] == self.opposite or diagonals[value][1] == self.opposite_queen) 
                        and diagonals[value][0] not in remove):
                    next = value + 1
                    if next < end:
                        if diagonals[next][1] == None: 
                            if remove == []:
                                select = [[diagonals[next][0], [diagonals[value][0]]]]
                                remove = select[0][1]
                            else:
                                select = [[diagonals[next][0], remove]]
                                select[0][1].append(diagonals[value][0])
                                remove = select[0][1]
                            wait_loop = True
                            add = True
                            search = True
                        elif diagonals[next][1] != None:
                            break
                
                elif diagonals[value][1] == self.checker or diagonals[value][1] == self.queen:
                    break
            else:
                wait_loop = False
        
        for move in select:
            if move[1] != [] and add == True and search == True:
                check_board = copy.deepcopy(board)
                self.update_board(check_board, move, origin)
                if not self.search_queen_move_diagI(check_board, [move[0], None], move, False):
                    self.update_moves(self.position, move[0], move[1])
                    
            elif move[1] == [] and current_win == [None, []]:
                self.update_moves(self.position, move[0], move[1])
        
        
    
        start = diagonals.index(origin) - 1
        end = -1
        remove = []
        add =  False
        select = []
        if current_win != [None, []]:
            remove = current_win[1]
        wait_loop = False
        for value in range(start, end, -1):
            if wait_loop == False:
                if diagonals[value][1] == None and add == False and remove == []:
                    select.append([diagonals[value][0], []])

                elif diagonals[value][1] == None and add == True: 
                    select.append([diagonals[value][0], [i for i in remove]])
            
                elif ((diagonals[value][1] == self.opposite or diagonals[value][1] == self.opposite_queen) 
                        and diagonals[value][0] not in remove):
                    next = value - 1
                    if next > end:
                        if diagonals[next][1] == None: 
                            if remove == []:
                                select = [[diagonals[next][0], [diagonals[value][0]]]]
                                remove = select[0][1]
                            else:
                                select = [[diagonals[next][0], remove]]
                                select[0][1].append(diagonals[value][0])
                                remove = select[0][1]
                            wait_loop = True
                            add = True
                            search = True
                        elif diagonals[next][1] != None:
                            break
                
                elif diagonals[value][1] == self.checker or diagonals[value][1] == self.queen:
                    break
            else:
                wait_loop = False
        
        for move in select:
            if move[1] != [] and add == True and search == True:
                check_board = copy.deepcopy(board)
                self.update_board(check_board, move, origin)
                if not self.search_queen_move_diagI(check_board, [move[0], None], move, False):
                    self.update_moves(self.position, move[0], move[1])
               
            elif move[1] == [] and current_win == [None, []]:
                self.update_moves(self.position, move[0], move[1])

        
        if search == True:
            return True
        else:
            return False
        
   
    def update_moves(self, checker, new_p, remove):
        if checker not in self.moves.keys():
            self.moves.update({checker: []})
            self.moves[checker].append([new_p, remove])
        elif checker in self.moves.keys():
            if [new_p, remove] not in self.moves[checker]:
                self.moves[checker].append([new_p, remove])
            
    
    def point_checker(self, click, mouse_x, mouse_y, display):
        '''This function locks choosen checker if choosen checker has any possible move.'''
        
        free_squares = self.moves.keys()
        if self.lock == False:
            for each in self.board.board:
                if each[1] == self.checker or each[1] == self.queen:
                    row = math.floor(each[0] / 8)
                    column = each[0] % 8
                    pixel_x, pixel_y = self.board.convert_tile_to_pixel(column, row, SQUARE)
                    checker = pygame.Rect(pixel_x, pixel_y, SQUARE, SQUARE)
                    if checker.collidepoint(mouse_x, mouse_y) and click == True and each[0] in free_squares:
                        self.highlight_checker((pixel_x, pixel_y), display)
                        self.choosen = ((each), (pixel_x, pixel_y))
                        self.lock = True
                    
        else:
            pixel_x, pixel_y = self.choosen[1]
            checker = pygame.Rect(pixel_x, pixel_y, SQUARE, SQUARE)
            if checker.collidepoint(mouse_x, mouse_y) and click == True:
                self.lock = False
            else:
                self.highlight_checker(self.choosen[1], display)
         
    
    def highlight_checker(self, position, display):
        '''This function marks choosen checker.'''
        size = (100, 100)
        surface = pygame.Surface(size)
        surface.set_colorkey(BLACK)
        surface.fill(BLACK)
        surface.set_alpha(70)
        pygame.draw.circle(surface, LIGHT_SQ, (50, 50), 44, 7)
        display.blit(surface, position)
        pygame.display.update()   
        
    
    def artificial_move(self):
        if self.choice == 'Easy Artificial Player':
            target = (None, [None, []])
            # find checker with best moves
            for checker in self.moves:
                for move in self.moves[checker]:
                    if len(move[1]) > len(target[1][1]):
                        target = (checker, move)
            if target[0] == None:
                checker = self.moves.keys()
                checker = random.choice(list(checker))
                move = random.choice(self.moves[checker])
                target = (checker, move)
            else:
                move = random.choice(target[1])
          	# get type of computer choice(checker or queen)
            for square in self.board.board:
            	if square[0] == target[0]:
            		checker = square[1]

            self.update_board(self.board.board, target[1], (target[0], checker))

            return True  
    
    
    def human_move(self, click, mouse_x, mouse_y, display):
        '''Keeps track if any possible move had been done by player.'''
        for each in self.moves:
            if each == self.choosen[0][0]:
                targets = self.moves[each]
     
        win_first = []
        current_win = [None, []]
        # choose moves with maximum win checkers
        for target in targets:
            if len(target[1]) > len(current_win[1]):
                current_win = target
                win_first = []
                win_first.append(target)
            elif len(target[1]) == len(current_win[1]):
                win_first.append(target)

        if win_first == []:
            win_first = targets
        print(win_first, 'win first')   
        for items in win_first:
            row = math.floor(items[0] / 8)
            column = items[0] % 8
            pixel_x, pixel_y = self.board.convert_tile_to_pixel(column, row, SQUARE)
            square = pygame.Rect(pixel_x, pixel_y, SQUARE, SQUARE)
            if square.collidepoint(mouse_x, mouse_y) and click == True:
                self.update_board(self.board.board, items, self.choosen[0]) 
                self.lock = False
                return True
                
    
    def update_board(self, board, items, origin):
        checker = origin[1]
        for each in board:
            if each[0] == origin[0]:
                each[1] = None
            elif each[0] == items[0]:
                each[1] = checker
            elif each[0] in items[1]:
                each[1] = None
            
        
    def check_win_checkers(self):
        '''If checker in queen square transform checker to queen checker.'''
        if self.checker == self.board.white:
            win_square = [i for i in range(1, 8)]
            win_checker = self.board.white_queen
            
        elif self.checker == self.board.black:
            win_square = [i for i in range(56, 64)]
            win_checker = self.board.black_queen
            
        for each in self.board.board:
            if (each[0] in win_square
                    and each[1] == self.checker):
                each[1] = win_checker
                        
                    

            
            
                
        
                
            
            
                     
            
        
            
    
        
        
