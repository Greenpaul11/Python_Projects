import math
import random
import pygame
import common_variables
from common_variables import *
from pygame.locals import *

class Engine(object):
    def __init__(self):
        pass
    
    # convert square position to the row position
    def convert_to_X(self, index):
        point = index % 3
        return point 

    # convert square position to the column position    
    def convert_to_Y(self, index):
        point = index / 3
        point = math.floor(point)
        return point 

    # insert symbol into board  
    def update_board(self, board, index, symbol):
        board.pop(index)
        board.insert(index, symbol) 

    # check if there is a game winner 
    def check_winner(self, board, symbol):
        rowI = [i for i in board[0:3]]
        rowII = [i for i in board[3:6]]
        rowIII = [i for i in board[6:]]
        columnI = [i for i in board[0:9:3]]
        columnII = [i for i in board[1:9:3]]
        columnIII = [i for i in board[2:9:3]]
        diagonalI = [i for i in board[0:9:4]]
        diagonalII = [i for i in board[2:7:2]]
        
        # check symbol in the row
        if all([symbol == i for i in rowI]): 
            return [0, 1, 2]
        elif all([symbol == i for i in rowII]):
            return [3, 4, 5]
        elif all([symbol == i for i in rowIII]):
            return [6, 7, 8] 
        
        # check symbol in the column
        if all([symbol == i for i in columnI]):
            return [0, 3, 6]
        elif all([symbol == i for i in columnII]):
            return [1, 4, 7]
        elif all([symbol == i for i in columnIII]):
            return [2, 5, 8]
        
        # check symbol in the diagonal
        if all([symbol == i for i in diagonalI]):
            return [0, 4, 8]
        elif all([symbol == i for i in diagonalII]):
            return [2, 4, 6] 
        
        # check free square for the game
        if ' ' not in board:
            return []  
        return [] 
    
    # this function selects background image    
    def select_image(self):
        collection = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        random.shuffle(collection)
        num = random.choice(collection)
        direction = 'pictures/sky.jpg'
        list_direction = [i for i in direction]
        list_direction.insert(12, str(num))
        direction = ''.join(list_direction)
        return direction
        
    # check position of the cursor on the board and return
    # specified position of the move
    def transform_pixel(self, mouse_x, mouse_y, board):
        for count, value in enumerate(board):
            if value == ' ':
                point_X = (self.convert_to_X(count) * W_SPACE) + MARGIN_X
                point_Y = (self.convert_to_Y(count) * W_SPACE) + MARGIN_Y
                square = pygame.Rect(point_X, point_Y, W_SPACE, W_SPACE)
                if square.collidepoint(mouse_x, mouse_y):
                    return (point_X, point_Y, count)
        return (None, None, None)

    # stop or play music    
    def music(self, switch):
    	if switch == True:
    		pygame.mixer.music.unpause()
    	elif switch == False:
    		pygame.mixer.music.pause()
    
    # algorithm for artificial player    
    def minmax(self, position, depth, maximizingPlayer):
        if depth == 0 or abs(position.value) == 10000000:
            return position.value, position.position
            
        if maximizingPlayer:
            max_value = -100000
            index = None
            for i in range(len(position.children)):
                evalu, square = self.minmax(position.children[i], depth - 1, False)
                if evalu >= max_value:
                    index = square
                max_value = max(max_value, evalu) 
            return max_value, index
            
        else:
            min_value = 100000
            index = None
            for i in range(len(position.children)):
                evalu, square = self.minmax(position.children[i], depth - 1, True)
                if evalu <= min_value:
                    index = square
                min_value = min(min_value, evalu)
            return min_value, index
            

class Buttons(object):
    def __init__(self):
    	# each header has its own size 
    	# when mouse cursor on it the size grows without
    	# changing the size of the rest of headers
        self.sizeI = 40
        self.sizeII = 40
        self.sizeIII = 40
        self.sizeIV = 17
        self.sizeV = 17
        self.sizeVI = 40
        self.title = 'Tic Tac Toe'
        self.headerI = 'Easy Mode'
        self.headerII = 'Normal Mode'
        self.headerIII = 'Hard Mode'
        self.headerIV = 'Exit'
        
    def draw_title(self, display):
        font = pygame.font.SysFont('ubuntu', 65)
        rend = font.render(self.title , True, CHALK)
        square = rend.get_rect()
        square.center = (W_WIDTH / 2, (W_HEIGHT / 2) - 180)
        display.blit(rend, square)
        
    def draw_headers(self, display):
        font = pygame.font.SysFont('ubuntu', self.sizeI)
        rend = font.render(self.headerI, True, CHALK)
        squareI = rend.get_rect()
        squareI.center = (W_WIDTH / 2 , (W_HEIGHT /2) - 70)
        display.blit(rend, squareI)
        
        font = pygame.font.SysFont('ubuntu', self.sizeII)
        rend = font.render(self.headerII, True, CHALK)
        squareII = rend.get_rect()
        squareII.center = (W_WIDTH / 2 , (W_HEIGHT /2) + 20)
        display.blit(rend, squareII)
        
        font = pygame.font.SysFont('ubuntu', self.sizeIII)
        rend = font.render(self.headerIII, True, CHALK)
        squareIII = rend.get_rect()
        squareIII.center = (W_WIDTH / 2 , (W_HEIGHT /2) + 110)
        display.blit(rend, squareIII)
        
        font = pygame.font.SysFont('ubuntu', self.sizeVI)
        rend = font.render(self.headerIV, True, CHALK)
        squareIV = rend.get_rect()
        squareIV.center = (W_WIDTH / 2 , (W_HEIGHT /2) + 200)
        display.blit(rend, squareIV)
        return squareI, squareII, squareIII, squareIV
    
    def draw_exit_icon(self, display):
    	font = pygame.font.SysFont('ubuntu', self.sizeV)
    	exit = font.render('EXIT', True, CHALK)
    	square = exit.get_rect()
    	square.center = (40, 560)
    	display.blit(exit, square)
    	return square
        
    def draw_sound_icon(self, sound, display):
    	if sound == True:
    		turn = 'ON'
    	else:
    		turn = 'OFF'
    	font = pygame.font.SysFont('ubuntu', 17)
    	text = font.render('SOUND', True, CHALK)
    	square = text.get_rect()
    	square.center = (690, 540)
    	display.blit(text, square)
    	font = pygame.font.SysFont('ubuntu', self.sizeIV)
    	textI = font.render(f' {turn} ', True, CHALK)
    	squareI = textI.get_rect()
    	squareI.center = (690, 560)
    	display.blit(textI, squareI)
    	return squareI
        
    # highlight square when cursor on it
    def highlight(self, square_X, square_Y, display):
        size = (W_SPACE, W_SPACE)
        square = pygame.Surface(size)
        square.set_alpha(100)
        pygame.draw.rect(square, HIGHLIGHT, (0, 0, W_SPACE, W_SPACE))
        display.blit(square,(square_X, square_Y)) 
        
    def draw_score_icon(self, playerI, playerII, lap, display):
        font = pygame.font.SysFont('ubuntu', 17)
        score = font.render('SCORE', True, CHALK)
        square = score.get_rect()
        square.center = (40, 40)
        display.blit(score, square)
        scoreI = font.render(f'{playerI.score} / {playerII.score}', True, CHALK)
        squareI = scoreI.get_rect()
        squareI.center = (40, 60)
        display.blit(scoreI, squareI)
        match = font.render('MATCH', True, CHALK)
        squareII = match.get_rect()
        squareII.center = (690, 40)
        display.blit(match, squareII)
        matchI = font.render(f'{lap} / 10', True, CHALK)
        squareIII = matchI.get_rect()
        squareIII.center = (690, 60)
        display.blit(matchI, squareIII)
    
    def draw_winner(self, playerI, playerII, display):
        font = pygame.font.SysFont('ubuntu', 65)
        if playerI.score > playerII.score:
            win = font.render('You Won', True, CHALK)
        elif playerI.score == playerII.score:
            win = font.render('Tie Tie Tie', True, CHALK)
        else:
            win = font.render('You Lost', True, CHALK)
        square = win.get_rect()
        square.center = (365, 300)
        display.blit(win, square)
    

        
        

            



        
            
        
        
        
        

        
