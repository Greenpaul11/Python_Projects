import pygame
import time
import random
import tictactoe_engine
import common_variables
import tictactoe_players
from tictactoe_engine import *
from common_variables import *
from tictactoe_players import *
from pygame.locals import *

# set board for play
def play():
    global DISPLAY, board
    engine = Engine()
    buttons = Buttons()
    mouse_x = 0
    mouse_y = 0
    board = [' ' for i in range (9)]
    new_board = False
    click = False
    wait_loop = 180
    win = []
    start = True
    blink = [i for i in range(200)]
    round_end = False
    count_board = 1
    switch = True
    quit = False
    pygame.init()
    DISPLAY = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
    pygame.display.set_caption('tictactoe')
    clock = pygame.time.Clock()
    wall_image = pygame.image.load(engine.select_image())
    pygame.mixer.music.load('music/music.ogg')
    pygame.mixer.music.play(-1)
    
    while True:
        if start == True and wait_loop == 180:
            DISPLAY.blit(wall_image, (0, 0))
            buttons.draw_title(DISPLAY)
            squareI, squareII, squareIII, squareIV = buttons.draw_headers(DISPLAY)
        
        elif round_end == True and new_board == False and wait_loop < 180: 
            DISPLAY.blit(wall_image, (0, 0)) 
            buttons.draw_winner(playerI, playerII, DISPLAY)
            if wait_loop == 179:
                wall_image = pygame.image.load(engine.select_image())
                round_end = False   

        elif start == False:
            DISPLAY.blit(wall_image, (0, 0))
            pygame.draw.aaline(DISPLAY, CHALK, (MARGIN_X + W_SPACE, MARGIN_Y), 
                            (MARGIN_X + W_SPACE, W_HEIGHT - MARGIN_Y), 4)
            pygame.draw.aaline(DISPLAY, CHALK, (MARGIN_X + (2 * W_SPACE), MARGIN_Y), 
                            (W_WIDTH - MARGIN_X - W_SPACE, W_HEIGHT - MARGIN_Y), 4)
            pygame.draw.aaline(DISPLAY, CHALK, (MARGIN_X, MARGIN_Y + W_SPACE), 
                            (W_WIDTH - MARGIN_X, MARGIN_Y + W_SPACE), 4)
            pygame.draw.aaline(DISPLAY, CHALK, (MARGIN_X, W_HEIGHT - MARGIN_Y - W_SPACE), 
                            (W_WIDTH - MARGIN_X, W_HEIGHT - MARGIN_Y - W_SPACE), 4) 
            
            for count, value in enumerate(board):
                point_X = engine.convert_to_X(count)
                point_Y = engine.convert_to_Y(count)
                if value == 'X' and count not in win:
                    pygame.draw.line(DISPLAY, BROWN, 
                                    ((point_X * W_SPACE) + GAP + MARGIN_X,
                                     (point_Y * W_SPACE) + GAP + MARGIN_Y),
                                    ((point_X * W_SPACE) + W_SPACE - GAP + MARGIN_X,
                                     (point_Y * W_SPACE) + W_SPACE - GAP + MARGIN_Y),
                                    7)
                    pygame.draw.line(DISPLAY, BROWN,
                                    ((point_X * W_SPACE) + W_SPACE - GAP + MARGIN_X,
                                     (point_Y * W_SPACE) + GAP + MARGIN_Y),
                                    ((point_X * W_SPACE) + GAP + MARGIN_X,
                                     (point_Y * W_SPACE) + W_SPACE - GAP + MARGIN_Y),
                                    7)
                                    
                elif value == 'O' and count not in win:
                    pygame.draw.circle(DISPLAY, BROWN,
                                      ((point_X * W_SPACE) + HALF + MARGIN_X,
                                      (point_Y * W_SPACE) + HALF + MARGIN_Y), 
                                      HALF - GAP, 
                                      7)
                                      
                if (value == 'X' and count in win 
                        and (wait_loop in blink[0:20] 
                        or wait_loop in blink[40:60] 
                        or wait_loop in blink[80:100] 
                        or wait_loop in blink[120:140]
                        or wait_loop in blink[160:180])):
                    pygame.draw.line(DISPLAY, BROWN, 
                                    ((point_X * W_SPACE) + GAP + MARGIN_X,
                                     (point_Y * W_SPACE) + GAP + MARGIN_Y),
                                    ((point_X * W_SPACE) + W_SPACE - GAP + MARGIN_X,
                                     (point_Y * W_SPACE) + W_SPACE - GAP + MARGIN_Y),
                                    7)
                    pygame.draw.line(DISPLAY, BROWN,
                                    ((point_X * W_SPACE) + W_SPACE - GAP + MARGIN_X,
                                     (point_Y * W_SPACE) + GAP + MARGIN_Y),
                                    ((point_X * W_SPACE) + GAP + MARGIN_X,
                                     (point_Y * W_SPACE) + W_SPACE - GAP + MARGIN_Y),
                                    7)
                                    
                elif (value == 'O' and count in win
                        and (wait_loop in blink[0:20] 
                        or wait_loop in blink[40:60] 
                        or wait_loop in blink[80:100] 
                        or wait_loop in blink[120:140]
                        or wait_loop in blink[160:180])):
                    pygame.draw.circle(DISPLAY, BROWN,
                                      ((point_X * W_SPACE) + HALF + MARGIN_X,
                                      (point_Y * W_SPACE) + HALF + MARGIN_Y), 
                                      HALF - GAP, 
                                      7) 
        
        for event in pygame.event.get():
            if event.type == QUIT or quit:
                pygame.quit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                click = True
        
        # this variable prevents to display players move in the same time
        if wait_loop < 180:
            wait_loop += 1
        # create new board    
        if new_board == True and wait_loop == 180:
            count_board += 1
            board = [' ' for i in range(9)]
            new_board = False
            wait_loop = 0
            if count_board > 10:
                count_board = 0
                round_end = True
                start = True
                wait_loop = 0
            else:
                time.sleep(1)
        
        # check if sound button pressed
        sound = buttons.draw_sound_icon(switch, DISPLAY)
        if sound.collidepoint(mouse_x, mouse_y):
            if buttons.sizeIV <= 20:
                buttons.sizeIV += 1
        elif buttons.sizeIV <= 21 and buttons.sizeIV >= 18:
            buttons.sizeIV -= 1
        if sound.collidepoint(mouse_x, mouse_y) and click == True:
            if switch == True:
                switch = False
            else:
                switch = True
            engine.music(switch)
            click = False   
            
        if start == True :
            # draw bigger text if cursor on it
            # if cursor not on it come back to orginal size
            if squareI.collidepoint(mouse_x, mouse_y):
                if buttons.sizeI < 55:
                    buttons.sizeI += 1
            else:
                if buttons.sizeI > 40:
                    buttons.sizeI -= 1
            if squareII.collidepoint(mouse_x, mouse_y):
                if buttons.sizeII < 55:
                    buttons.sizeII += 1
            else:
                if buttons.sizeII > 40:
                    buttons.sizeII -= 1
            if squareIII.collidepoint(mouse_x, mouse_y):
                if buttons.sizeIII < 55:
                    buttons.sizeIII += 1
            else:
                if buttons.sizeIII > 40:
                    buttons.sizeIII -= 1
            if squareIV.collidepoint(mouse_x, mouse_y):
                if buttons.sizeVI < 55:
                    buttons.sizeVI += 1
            else:
                if buttons.sizeVI > 40:
                    buttons.sizeVI -= 1
            
            if squareI.collidepoint(mouse_x, mouse_y) and click == True:
                playerI = Player('X', True)
                playerII = Player('O', 'easy')
                start = False
                click = False
                current_player = playerI
            elif squareII.collidepoint(mouse_x, mouse_y) and click == True:
                playerI = Player('X', True)
                playerII = Player('O', 'normal')
                start = False
                click = False
                current_player = playerI
            elif squareIII.collidepoint(mouse_x, mouse_y) and click == True:
                playerI = Player('X', True)
                playerII = Player('O', 'hard')
                start = False
                click = False
                current_player = playerI
            elif squareIV.collidepoint(mouse_x, mouse_y) and click == True:
                quit = True                 
                
        elif start == False:
            square_X, square_Y, index = engine.transform_pixel(mouse_x, mouse_y, board)
            if square_X != None and square_Y != None :
                buttons.highlight(square_X, square_Y, DISPLAY)
            # human player move    
            if (click == True 
                    and square_X != None 
                    and square_Y != None 
                    and current_player.kind == True
                    and new_board == False):
                engine.update_board(board, index, current_player.symbol)
                current_player = playerII
                click = False
                wait_loop = 0
                win = engine.check_winner(board, playerI.symbol)
                if win != []:
                    playerI.score += 1
                    new_board = True
                    wait_loop = 0
                elif ' ' not in board:
                    new_board = True
                    wait_loop = 0
            # artificial  player move    
            elif (current_player.kind != True 
                    and wait_loop == 2
                    and new_board == False):
                choice = current_player.artificial_move(board, engine)
                engine.update_board(board, choice, current_player.symbol)
                current_player = playerI
                win = engine.check_winner(board, playerII.symbol)
                if win != []:
                    playerII.score += 1
                    new_board = True
                    wait_loop = 0
                elif ' ' not in board:
                    new_board = True
                    wait_loop = 0
                else:
                    time.sleep(1)

            buttons.draw_score_icon(playerI, playerII, count_board, DISPLAY)
            exit = buttons.draw_exit_icon(DISPLAY)
            if exit.collidepoint(mouse_x, mouse_y):
                if buttons.sizeV<= 20:
                    buttons.sizeV += 1
                if click == True:
                    new_board = True
                    wait_loop = 180
                    count_board = 11
                    click = False
            elif buttons.sizeV <= 21 and buttons.sizeV >= 18:
                buttons.sizeV -= 1
            
        pygame.display.update()
        clock.tick(FPS)  
                
play()

        
