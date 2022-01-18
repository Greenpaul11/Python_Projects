import pygame
import checkers_settings
import checkers_board
import checkers_engine
import checkers_players
from checkers_players import *
from checkers_engine import *
from checkers_settings import *
from pygame.locals import *
from checkers_board import *

def main():
    game = True
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')
    imageI = pygame.image.load('graphic/plankI.jpg')
    engine = Engine()
    main_menu = True
    choose_checker = False
    buttons = Buttons()
    click = False
    mouse_x = 0
    mouse_y = 0
    choice = None
    play = False
    exit = False
    end = False
    loop_time = 0
    switch_player = 1
    start = False
 
    
    while game == True:
        if main_menu == True:
            DISPLAY.blit(imageI, (0, 0))
            buttons.draw_main_menu(DISPLAY)
            
        elif choose_checker == True:
            DISPLAY.blit(imageI, (0, 0))
            white_square, black_square = buttons.draw_choose_checker(DISPLAY)
            back_square, sound_square = buttons.draw_margin_buttons(DISPLAY) 
            
        elif play == True:
            DISPLAY.blit(imageI, (0, 0))
            board.draw_squares(DISPLAY)
            board.draw_checkers(DISPLAY)
            board.draw_margin_checkers(DISPLAY)
            white_checker, black_checker = playerI.count_checkers(board.board)
            buttons.draw_under_checker(DISPLAY, white_checker, black_checker)
            back_square, sound_square = buttons.draw_margin_buttons(DISPLAY)

        elif end == True and loop_time == 2:
            DISPLAY.blit(imageI, (0, 0))
        
        for event in pygame.event.get():
            if event.type == QUIT or exit:
                pygame.quit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                click = True    
                
        if loop_time < 2:
            loop_time += 1
        if loop_time == 2:
            start = True
        
        if main_menu == True:
            # this variable store choosen option in main menu
            if choice == None:
                choice = buttons.main_buttons(DISPLAY, mouse_x, mouse_y,
                                              click, engine)
            # the header with Sound option inform if sound is On or Off
            # if user click on it the sound is switched 
            elif choice == 'Sound On':
                engine.sound(choice)
                buttons.headerV[1] = 'Sound Off'
                buttons.sound_icon[1] = 'Sound Off'
                engine.pause_music()
                choice = None
                click = False
            elif choice == 'Sound Off':
                engine.sound(choice)
                buttons.headerV[1] = 'Sound On'
                buttons.sound_icon[1] = 'Sound On'
                engine.pause_music()
                choice = None
                click = False
            elif choice == 'Exit':
                exit = True
            else:
                main_menu = False
                choose_checker = True
                click = False
                loop_time = 0
        
        elif choose_checker == True:
            if white_square.collidepoint(mouse_x, mouse_y):
                buttons.highlight_checker(DISPLAY, white_square)
                if click == True:
                    engine.play_click()
                    click = False
                    pygame.time.wait(100)
                    choose_checker = False
                    if choice == 'Second Human Player':
                        kind = True
                    else:
                        kind = False
                    board = Board()
                    playerI = Player('white', board.board, choice, True, choice, engine)
                    playerII = Player('black', board.board, choice, kind, choice, engine)
                    play = True

            elif black_square.collidepoint(mouse_x, mouse_y):
                buttons.highlight_checker(DISPLAY, black_square)
                if click == True:
                    engine.play_click()
                    click = False        
                    pygame.time.wait(100)
                    choose_checker = False
                    if choice == 'Second Human Player':
                        kind = True
                    else:
                        kind = False
                    board = Board()
                    playerI = Player('black', board.board, choice, True, choice, engine)
                    playerII = Player('white', board.board, choice, kind, choice, engine)
                    play = True
        
        
        if (choose_checker == True or play == True) and loop_time == 2:
            if back_square.collidepoint(mouse_x, mouse_y):
                if click == True :
                    choose_checker = False
                    play = False
                    main_menu = True
                    choice = None
                    click = False
                    pygame.time.wait(100)
                if buttons.back_icon[0] < 38:
                    buttons.back_icon[0] += 1
            else:
                if buttons.back_icon[0] > 25:
                    buttons.back_icon[0] -= 1
            
            if sound_square.collidepoint(mouse_x, mouse_y):
                if click == True:
                    if buttons.sound_icon[1] == 'Sound On':
                        buttons.headerV[1] = 'Sound Off'
                        buttons.sound_icon[1] = 'Sound Off'
                        engine.sound('Sound On')
                        engine.pause_music()
                    elif buttons.sound_icon[1] == 'Sound Off':
                        buttons.headerV[1] = 'Sound On'
                        buttons.sound_icon[1] = 'Sound On'
                        engine.sound('Sound Off')
                        engine.pause_music()
                    click = False
                if buttons.sound_icon[0] < 38:
                    buttons.sound_icon[0] += 1
            else:
                if buttons.sound_icon[0] > 25:
                    buttons.sound_icon[0] -= 1
                    
        
        if play == True and end == False and start == True:
            if switch_player == 1 and playerI.kind == True:
                if playerI.lock == True and click == True:
                   if playerI.human_move(click, mouse_x, mouse_y, board, DISPLAY):
                        click = False
                        board.update = True
                        playerI.lock = False
                        board.origin = playerI.choosen[0]
                        
                if board.update == True:
                    board.update_board(playerI.items, engine, DISPLAY)
                    if playerI.items == []:
                        board.update = False
                        switch_player = 2
                        loop_time = 0
                        playerI.check_win_checkers()
                        random.shuffle(board.board)
                        playerII.available_moves()
                        if playerII.moves == {}:
                            end = True
                            winner = playerI.checker
                            engine.count = 240
                            loop_time = 0
                            
                playerI.point_checker(click, mouse_x, mouse_y, board, DISPLAY)
                click = False

            elif switch_player == 2 and playerII.kind == False and loop_time == 2:
                if board.update == False:
                    board.origin, playerII.items =  playerII.artificial_move()
                    board.update = True
                    #pygame.time.wait(1000)

                if board.update == True:
                    board.update_board(playerII.items, engine, DISPLAY)
                    if playerII.items == []:
                        board.update = False
                        switch_player = 1
                        playerII.check_win_checkers()
                        playerI.available_moves()
                        if playerI.moves == {}:
                            end = True
                            winner = playerII.checker
                            engine.count = 240
                            loop_time = 0
           
            elif switch_player == 2 and playerII.kind == True:
                if playerII.lock == True and click == True:
                    if playerII.human_move(click, mouse_x, mouse_y, board, DISPLAY):
                        click = False
                        board.update = True
                        playerII.lock = False
                        board.origin = playerII.choosen[0]
                        
                        
                if board.update == True:
                    board.update_board(playerII.items, engine, DISPLAY)
                    if playerII.items == []:
                        board.update = False
                        switch_player = 1
                        loop_time = 0
                        playerII.check_win_checkers()
                        playerI.available_moves()
                        if playerI.moves == {}:
                            end = True
                            winner = playerII.checker
                            engine.count = 240
                            loop_time = 0
                
                playerII.point_checker(click, mouse_x, mouse_y, board, DISPLAY)
                click = False    

        elif end == True and loop_time == 2:
            play = False
            buttons.draw_game_over(DISPLAY, winner)
            
            if buttons.count == -120:
                buttons.count = 120
                
                choice = None
                end = False
                main_menu = True
                start = False
                    

        pygame.display.update()
        clock.tick(FPS)
        
        
        
main()
