import pygame
import math
import checkers_settings
from checkers_settings import *
from pygame.locals import *


class Board(object):
    def __init__(self):
        self.background = pygame.image.load('graphic/plankI.jpg')
        # if first_time is True the white squares are drawn in slow motion
        self.first_time = True
        # second_time allows to draw frame of the board faster than tiles
        self.second_time = True
        # stores data of each square of the board in form of lists in list
        self.board = self.make_board()
        self.update = False
        # keeps values that are used to animate checker move
        self.step = None
        # keeps data of board tiles that has to be updated 
        self.move = None
        self.wait = False
        # keeps proper order of jobs for updating function 
        self.count = 0
        # the square from checker start it's move
        self.origin = None
        size = int((8 * SQUARE) + (2 * FRAME_SQUARE))
        # create surface object for displaying squares
        # in this way program does not have to calculate
        # over and over position for each square
        self.surf = pygame.Surface((size, size))
        self.surf.set_alpha(80)
        self.surf.set_colorkey([0, 0, 0])
        # load images of checkers and queens
        self.white = pygame.image.load('graphic/white_checker.png')
        self.black = pygame.image.load('graphic/black_checker.png')
        self.white_queen = pygame.image.load('graphic/white_checker_win.png')
        self.black_queen = pygame.image.load('graphic/black_checker_win.png')
        self.checker_copy = None
        # change alpha of image
        self.alpha = 240

    def make_board(self):
        # list board stores the lists with number position of each tile
        # and type of the checker on it
        # if the tile is free the second item of the list is 'None'
        # the game board has 64 squares but 'board list' has only half of it
        # because players can move only on tiles that have the same color
        board = []
        for row in range(ROWS):
            for column in range(COLUMNS):
                if row % 2 == 1:
                    square = (8 * row) + column
                    if square % 2 == 0 and square <= 23:
                        board.append([square, 'black'])
                    elif square % 2 == 0 and square >= 40:
                        board.append([square, 'white'])
                    elif square % 2 == 0 and square > 23 and square < 40:
                        board.append([square, None])
                
                elif row % 2 == 0:
                    square = (8 * row) + column
                    if square % 2 == 1 and square <= 23:
                        board.append([square, 'black'])
                    elif square % 2 == 1 and square >= 40:
                        board.append([square, 'white'])
                    elif square % 2 == 1 and square > 23 and square < 40:
                        board.append([square, None])
        return board
        

    def draw_squares(self, display):
        # first function animates creation of the board
        # than image of tiles is stored in self.surf
        if self.second_time == True:
            self.draw_frame(display)
            self.first_time = False
            for row in range(ROWS):
                for column in range(COLUMNS):
                    if (row + column) % 2 != 0:
                        pixel_x = FRAME_SQUARE + (column * SQUARE)
                        pixel_y = FRAME_SQUARE + (row * SQUARE)
                        self.draw_tile(display, pixel_x, pixel_y,
                                       SQUARE, LIGHT_SQ)
            self.second_time = False
        else:
            display.blit(self.surf,
                         (MARGIN_X - FRAME_SQUARE, MARGIN_Y - FRAME_SQUARE))

    
    def draw_tile(self, display, pixel_x, pixel_y, square, color):
        pygame.draw.rect(self.surf, color, (pixel_x, pixel_y, square, square))
        if self.first_time == True:
            display.blit(self.background, (0, 0))
            display.blit(self.surf,
                         (MARGIN_X - FRAME_SQUARE, MARGIN_Y - FRAME_SQUARE))
            pygame.time.wait(2)
            pygame.display.update()
        elif self.second_time == True:
            display.blit(self.background, (0, 0))
            display.blit(self.surf,
                         (MARGIN_X - FRAME_SQUARE, MARGIN_Y - FRAME_SQUARE))
            pygame.time.wait(50)
            pygame.display.update()
    

    def draw_frame(self, display):
        # smalltile is the number of rectangel that has to be drawn
        # to cover length or height of the board
        smalltile = int(((COLUMNS * SQUARE) + FRAME_SQUARE) / FRAME_SQUARE)
        for each in range(smalltile):
            pixel_x = each * FRAME_SQUARE
            pixel_y = 0
            self.draw_tile(display, pixel_x, pixel_y, FRAME_SQUARE, BLACK)
            
        for each in range(smalltile):
            pixel_x = FRAME_SQUARE + (8 * SQUARE)
            pixel_y = each * FRAME_SQUARE
            self.draw_tile(display, pixel_x, pixel_y, FRAME_SQUARE, BLACK)
            
        for each in range(smalltile, -1, -1):
            pixel_x = each * FRAME_SQUARE
            pixel_y = (8 * SQUARE) + FRAME_SQUARE
            self.draw_tile(display, pixel_x, pixel_y, FRAME_SQUARE, BLACK)
            
        for each in range(smalltile, -2, -1):
            pixel_x = 0
            pixel_y = each * FRAME_SQUARE
            self.draw_tile(display, pixel_x, pixel_y, FRAME_SQUARE, BLACK)
            

    def draw_checkers(self, display):
        for each in self.board:
            if each[1] != None:
                if each[1] == 'white':
                    checker = self.white
                elif each[1] == 'black':
                    checker = self.black
                elif each[1] == 'white queen':
                    checker = self.white_queen
                elif each[1] == 'black queen':
                    checker = self.black_queen
                elif each[1] == 'copy':
                    checker = self.checker_copy
       
                row = math.floor(each[0] / 8)
                column = each[0] % 8
                pixel_x, pixel_y = self.convert_tile_to_pixel(column,
                                                              row, SQUARE)
                display.blit(checker, (pixel_x, pixel_y))
        
                
    def draw_margin_checkers(self, display):
        squareI = self.white.get_rect()
        squareI.center = (MARGIN_X / 2, MARGIN_Y - 10)
        display.blit(self.white, squareI)
        squareII = self.black.get_rect()
        squareII.center = (MARGIN_X + 640 + (MARGIN_X / 2), MARGIN_Y - 10)
        display.blit(self.black, squareII)
 

    def convert_tile_to_pixel(self, column, row, square):
        pixel_x = MARGIN_X + (column * square)
        pixel_y = MARGIN_Y + (row * square)
        return pixel_x, pixel_y                
                
    def update_board(self, moves, sound, display):
        if self.step == None:
            move = moves[0]
            # transform position number of square to pixel position 
            row = math.floor(self.origin[0] / 8)
            column = self.origin[0] % 8
            # current pixel position of checker 
            column_o, row_o = self.convert_tile_to_pixel(column,
                                                         row, SQUARE)
            
            row = math.floor(move[0] / 8)
            column = move[0] % 8
            # pixel position of target square
            column_m, row_m = self.convert_tile_to_pixel(column,
                                                         row, SQUARE)
            # if there is a win move set pixel position of the beaten checker
            if move[1] != None:
                row = math.floor(move[1] / 8)
                column = move[1] % 8
                column_r, row_r = self.convert_tile_to_pixel(column,
                                                         row, SQUARE)
                # set pixel step for loop when beating
                step_x = (column_r - column_o) / 10
                step_y = (row_r - row_o) / 10
                # set collision point of both checkers
                collision = [column_o + (step_x * 4), row_o + (step_y * 4)]
            else:
                step_x = None
                step_y = None
                column_r = None
                row_r = None
                collision = None
            
            # set pixel step for loop when free move
            step_xI = (column_m - column_o) / 40
            step_yI = (row_m - row_o) / 40
            
            if self.origin[1] == 'white':
                checker = (self.white, 'white')
            elif self.origin[1] == 'black':
                checker = (self.black, 'black')
            elif self.origin[1] == 'white queen':
                checker = (self.white_queen, 'white queen')
            elif self.origin[1] == 'black queen':
                checker = (self.black_queen, 'black queen')
            self.move = [checker, move[0], move[1]]
            self.step = [step_x, step_y, step_xI, step_yI, [column_o, row_o],
                         [column_m, row_m], [column_r, row_r], collision]
            # start checker move
            for each in self.board:
                if each[0] == self.origin[0]:
                    each[1] = None
                elif each[0] == move[1]:
                    if each[1] == 'white':
                        self.checker_copy = self.white.copy()
                    elif each[1] == 'black':
                        self.checker_copy = self.black.copy()
                    elif each[1] == 'white queen':
                        self.checker_copy = self.white_queen.copy()
                    elif each[1] == 'black queen':
                        self.checker_copy = self.black_queen.copy()
                        
            
        elif self.step != None:
            if (self.move[2] != None and self.step[4] != self.step[6]
                    and self.step[7] == None):
                self.step[4][0] += self.step[0]
                self.step[4][1] += self.step[1]
                # make vanish checker
                self.alpha -= 40
                self.checker_copy.set_alpha(self.alpha)
                display.blit(self.move[0][0],(self.step[4][0], self.step[4][1]))
                # if checker is on the position of opposite checker
                if self.move[2] != None and self.step[4] == self.step[6]:
                    # remove checker completly from the board
                    for each in self.board:
                        if each[0] == self.move[2]:
                            each[1] = None
                    self.alpha = 240
                    self.move[2] = None
                    sound.play_click()
                
            elif self.step[4] != self.step[5]:
                self.step[4][0] += self.step[2]
                self.step[4][1] += self.step[3]
                # if checker reach collision point
                if self.step[7] == self.step[4]:
                    self.step[7] = None
                    for each in self.board:
                        if each[0] == self.move[2]:
                            each[1] = 'copy'
                    
                display.blit(self.move[0][0],(self.step[4][0], self.step[4][1]))    
                # if checker reach it's target position 
                if self.step[4] == self.step[5]:
                    for each in self.board:
                        if each[0] == self.move[1]:
                            each[1] = self.move[0][1]
                    self.origin = (self.move[1], self.origin[1])
                    self.move = None
                    self.step = None
                    moves.pop(0)
            
    
    
            
                

    
        
        
               
            

    
                
        
        
