import pygame
import checkers_settings
import checkers_players
from checkers_players import *
from checkers_settings import *
from pygame.locals import *

class Engine(object):
    def __init__(self):
        self.switch = 'On'
        self.click = pygame.mixer.Sound('sound/click.ogg')
        self.music = pygame.mixer.Sound('sound/music.ogg')
        self.play_music = self.play_music()
        

    def sound(self, turn):
        if turn == 'Sound On':
            self.switch = 'Off'
        elif turn == 'Sound Off':
            self.switch = 'On'
    
    
    def play_click(self):
        if self.switch == 'On':
            channelI = pygame.mixer.Channel(1)
            channelI.play(self.click)
            

    def play_music(self):
        channelII = pygame.mixer.Channel(2)
        channelII.play(self.music, -1)
        return channelII
    

    def pause_music(self):
        if self.switch == 'On':
            self.play_music.unpause()
        elif self.switch == 'Off':
            self.play_music.pause()
     
        
class Buttons(object):
    def __init__(self):
        # each header has its own text size that allows
        # to manipulate the size of the choosen header independly 
        self.title = [70, 'Checkers']
        self.headerI = [33, 'Second Human Player']
        self.headerII = [33, 'Easy Artificial Player']
        self.headerIII = [33, 'Normal Artificial Player']
        self.headerIV = [33, 'Tough Artificial Player']
        self.headerV = [33, 'Sound On']
        self.headerVI = [33, 'Exit']
        self.back_icon = [25, 'Back']
        self.sound_icon = [25, 'Sound On']
        # store display position of the each header in the list
        self.square = []
        self.count = 120
        
        
    def draw_main_menu(self, display):
        self.square = []
        title = self.create_text(self.title[0], self.title[1])
        title_sq = self.draw_text(display, title, (WIDTH / 2, MARGIN_Y + 100)) 
    
        headerI = self.create_text(self.headerI[0], self.headerI[1])
        headerI_sq = self.draw_text(display, headerI, (WIDTH / 2, MARGIN_Y + 220))
        self.square.append(headerI_sq)
        
        headerII = self.create_text(self.headerII[0], self.headerII[1])
        headerII_sq = self.draw_text(display, headerII, (WIDTH / 2, MARGIN_Y + 300))
        self.square.append(headerII_sq)
        
        headerIII = self.create_text(self.headerIII[0], self.headerIII[1])
        headerIII_sq = self.draw_text(display, headerIII, (WIDTH / 2, MARGIN_Y + 380))
        self.square.append(headerIII_sq)
        
        headerIV = self.create_text(self.headerIV[0], self.headerIV[1])
        headerIV_sq = self.draw_text(display, headerIV, (WIDTH / 2, MARGIN_Y + 460))
        self.square.append(headerIV_sq)
        
        headerV = self.create_text(self.headerV[0], self.headerV[1])
        headerV_sq = self.draw_text(display, headerV, (WIDTH / 2, MARGIN_Y + 540))
        self.square.append(headerV_sq)
        
        headerVI = self.create_text(self.headerVI[0], self.headerVI[1])
        headerVI_sq = self.draw_text(display, headerVI, (WIDTH / 2, MARGIN_Y + 620))
        self.square.append(headerVI_sq)
        
        
    def create_text(self, size, header):
        text = pygame.font.SysFont('ubuntu', size)
        rend = text.render(header, True, CHALK)
        return rend
    
    
    def draw_text(self, display, render, position):
        square = render.get_rect()
        square.center = position
        display.blit(render, square)
        return square
        
    
    def main_buttons(self, display, mouse_x, mouse_y, click, engine):
        if self.square[0].collidepoint(mouse_x, mouse_y):
            if click == True:
                click = False
                engine.play_click()
                return self.headerI[1]
            # make larger text when cursor on it
            if self.headerI[0] < 50:
                self.headerI[0] += 1
            # come back to orginal size when mouse cursor not present
        elif self.headerI[0] > 33:
                self.headerI[0] -= 1
            
        if self.square[1].collidepoint(mouse_x, mouse_y):
            if click == True:
                click = False
                engine.play_click()
                return self.headerII[1]
            if self.headerII[0] < 50:
                self.headerII[0] += 1
        elif self.headerII[0] > 33:
                self.headerII[0] -= 1   
                                
        if self.square[2].collidepoint(mouse_x, mouse_y):
            if click == True:
                click = False
                engine.play_click()
                return self.headerIII[1]
            if self.headerIII[0] < 50:
                self.headerIII[0] += 1
        elif self.headerIII[0] > 33:
                self.headerIII[0] -= 1  
                
        if self.square[3].collidepoint(mouse_x, mouse_y):
            if click == True:
                click = False
                engine.play_click()
                return self.headerIV[1]
            if self.headerIV[0] < 50:
                self.headerIV[0] += 1
        elif self.headerIV[0] > 33:
                self.headerIV[0] -= 1   
                                
        if self.square[4].collidepoint(mouse_x, mouse_y):
            if click == True:
                click = False
                engine.play_click()
                return self.headerV[1]
            if self.headerV[0] < 50:
                self.headerV[0] += 1
        elif self.headerV[0] > 33:
                self.headerV[0] -= 1    
                                
        if self.square[5].collidepoint(mouse_x, mouse_y):
            if click == True:
                click = False
                engine.play_click()
                return self.headerVI[1]
            if self.headerVI[0] < 50:
                self.headerVI[0] += 1
        elif self.headerVI[0] > 33:
                self.headerVI[0] -= 1   
                
        return None
        
    
    def draw_choose_checker(self, display):
        white_checker = pygame.image.load('graphic/white_checker2x.png')
        w_square = white_checker.get_rect()
        w_square.center = (WIDTH / 3, 400)
        display.blit(white_checker, w_square)
            
        black_checker = pygame.image.load('graphic/black_checker2x.png')
        b_square = black_checker.get_rect()
        b_square.center = (WIDTH - (WIDTH / 3), 400)
        display.blit(black_checker, b_square)
            
        font = pygame.font.SysFont('ubuntu', 45)
        rend = font.render('Choose Checker', True, CHALK)
        square = rend.get_rect()
        square.center = (480, 176)
        display.blit(rend, square)
            
        return w_square, b_square
        

    def highlight_checker(self, display, checker):
        size = (200, 200)
        surface = pygame.Surface(size)
        surface.set_alpha(100)
        # make rectangle shape of the surface invisible
        surface.set_colorkey(BLACK)
        surface.fill(BLACK)
        pygame.draw.circle(surface, HIGHLIGHT, (100, 100), 72, 8)
        square = surface.get_rect()
        # get central point from checker
        square.center = checker.center
        display.blit(surface, square)
        
   
    def draw_margin_buttons(self, display):
        back = self.create_text(self.back_icon[0], self.back_icon[1])
        back_square = self.draw_text(display, back,
                                     (MARGIN_X - 80, HEIGHT - (MARGIN_Y / 2)))
        
        sound = self.create_text(self.sound_icon[0], self.sound_icon[1])
        sound_square = self.draw_text(display, sound, (WIDTH - 104, HEIGHT - (MARGIN_Y / 2)))
        
        return back_square, sound_square 
        
    
    def draw_under_checker(self, display, white, black):
        white_num = self.create_text(25, white)
        white_square = self.draw_text(display, white_num,
                                      (MARGIN_X / 2, MARGIN_Y - 10))
        
        black_num = self.create_text(25, black)
        black_square = self.draw_text(display, black_num,
                                      (MARGIN_X + 640 + (MARGIN_X / 2), MARGIN_Y - 10))
        
    def draw_game_over(self, display, winner):
        self.count -= 1
        if self.count > 0:
            end = self.create_text(70, 'Game Over')
            end_square = self.draw_text(display, end, (WIDTH / 2, HEIGHT /2)) 
        
        else:
            if winner == 'black' or winner == 'black_queen':
                text = 'Black Wins'
            else:
                text = 'White Wins'
            end = self.create_text(70, text)
            end_square = self.draw_text(display, end, (WIDTH / 2, HEIGHT /2)) 
        
        
        
        
        
  
        

