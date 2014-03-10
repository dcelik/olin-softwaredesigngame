# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:34:24 2014

@author: Deniz Celik, Subhash Gubba, Danny Kang

Skeleton Provided by Paul Ruvolo from breakout_starter.py
We modified a menu taken from: http://scripters-corner.net/2013/04/11/creating-a-menu-in-pygame/

 
"""

import pygame
from pygame.locals import *
import random
import math
import time
import sys

SCREEN_WIDTH = 1550
SCREEN_HEIGHT = 840
SPEED = 3
LIVES = 4

class BrickBreakerModel:
    """ This class encodes the game state """
    def __init__(self):
        self.all_sprite_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.wall_list_vert = pygame.sprite.Group()
        self.wall_list_horz = pygame.sprite.Group()
        self.ball_list = pygame.sprite.Group()
        self.portals_list = pygame.sprite.Group()
        #Creating the different walls
        wallleft = Wall(SCREEN_HEIGHT,10,0,0)
        wallright = Wall(SCREEN_HEIGHT,10,SCREEN_WIDTH-10,0)
        walltop = Wall(10,SCREEN_WIDTH,0,0)
        wallbot = Wall(10,SCREEN_WIDTH,0,SCREEN_HEIGHT-10)
        #Classifying the left wall and adding it to lists
        self.wall_list.add(wallleft)
        self.all_sprite_list.add(wallleft)
        self.wall_list_vert.add(wallleft)
        #Classifying the right wall and adding it to lists
        self.wall_list.add(wallright)
        self.all_sprite_list.add(wallright)
        self.wall_list_vert.add(wallright)
        #Classifying the top wall and adding it to lists
        self.wall_list.add(walltop)
        self.all_sprite_list.add(walltop)
        self.wall_list_horz.add(walltop)
        #Classifying the bottom wall and adding it to lists
        self.wall_list.add(wallbot)
        self.all_sprite_list.add(wallbot)
        self.wall_list_horz.add(wallbot)
        #Making the enemy balls and adding them to lists        
        ball = Ball(random.randint(110,220),random.randint(110,220))
        self.ball_list.add(ball)
        self.all_sprite_list.add(ball)
        self.portals_list.add(ball)
        ball.wallshorz = self.wall_list_horz
        ball.wallsvert = self.wall_list_vert
        
        ball = Ball(random.randint(110,220),random.randint(SCREEN_HEIGHT-220,SCREEN_HEIGHT-110))
        self.ball_list.add(ball)
        self.all_sprite_list.add(ball)
        self.portals_list.add(ball)
        ball.wallshorz = self.wall_list_horz
        ball.wallsvert = self.wall_list_vert
        
        ball = Ball(random.randint(SCREEN_WIDTH-220,SCREEN_WIDTH-110),random.randint(110,220))
        self.ball_list.add(ball)
        self.all_sprite_list.add(ball)
        self.portals_list.add(ball)
        ball.wallshorz = self.wall_list_horz
        ball.wallsvert = self.wall_list_vert
        
        ball = Ball(random.randint(SCREEN_WIDTH-220,SCREEN_WIDTH-110),random.randint(SCREEN_HEIGHT-220,SCREEN_HEIGHT-110))
        self.ball_list.add(ball)
        self.all_sprite_list.add(ball)
        self.portals_list.add(ball)
        ball.wallshorz = self.wall_list_horz
        ball.wallsvert = self.wall_list_vert
        #Making the player
        self.player = Player(SCREEN_HEIGHT/2,SCREEN_HEIGHT/2)
        self.player.walls = self.wall_list
        self.player.balls = self.ball_list
        self.all_sprite_list.add(self.player)
        #Making the portal
        self.portal1 = Portal(20,100,10,10,0,2,1)
        self.portal2 = Portal(100,20,10,10,2,0,2)
        self.portal1.sprites = self.portals_list
        self.portal2.sprites = self.portals_list
        self.portal1.walls = self.wall_list
        self.portal2.walls = self.wall_list
        self.portal1.portal_exit = self.portal2
        self.portal2.portal_exit = self.portal1
        self.all_sprite_list.add(self.portal1)
        self.all_sprite_list.add(self.portal2)
        
        
    def update(self):
#        self.player.update()
        self.all_sprite_list.update()

class Wall(pygame.sprite.Sprite):
    """ Encodes the state of a brick in the game """
    def __init__(self,height,width,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Player(pygame.sprite.Sprite):
    # -- Attributes
    # Set speed vector
    change_x = 0
    change_y = 0
    walls = None
    balls = None
    # -- Methods
    # Constructor function
    def __init__(self,x,y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        # Set height, width
        paul = pygame.image.load('Paul.png')
        paul = paul.convert_alpha()
        self.image = paul
        #Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x += x
        self.change_y += y
        # Find a new position for the player
    def update(self):
        self.rect.x += self.change_x
        
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                
        # Move up/down
        self.rect.y += self.change_y
        
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
                
        block_hit_list = pygame.sprite.spritecollide(self, self.balls, False)
        for block in block_hit_list:
            global LIVES
            LIVES+=-1
            sound = pygame.mixer.Sound('Paul_Hit.ogg')
            sound.play(0)
            block.rect.x = -1000 #random.randint(200,SCREEN_WIDTH-200)
            block.rect.y = -1000 #random.randint(200,SCREEN_HEIGHT-200)
            
class Ball(pygame.sprite.Sprite):
    # -- Attributes
    # Set speed vector
    velx = random.randint(2,4)
    vely = random.randint(2,4)
    player = None
    wallsvert = None
    wallshorz = None
    # -- Methods
    # Constructor function
    def __init__(self,x,y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        # Set height, width
        paul = pygame.image.load('Paulinvert.png')
        paul = paul.convert_alpha()
        self.image = paul
        #Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = [self.velx,self.vely]
    def update(self):
        
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.wallsvert, False)
        if len(block_hit_list)>0:
            for block in block_hit_list:
               self.speed[0] = -self.speed[0]
        
        block_hit_list = pygame.sprite.spritecollide(self, self.wallshorz, False)
        if len(block_hit_list)>0:
            for block in block_hit_list:
                self.speed[1] = -self.speed[1]

        self.rect.y += self.speed[1]
        self.rect.x += self.speed[0]
    

class Portal(pygame.sprite.Sprite):
    """ Encodes the state of the portal in the game"""
    portal_exit  = None
    walls = None
    sprites = None
    def __init__(self,height,width,x,y,vx,vy,portnum):
        pygame.sprite.Sprite.__init__(self)
        if portnum ==1:
            port = pygame.image.load('PORTAL1.png')
        if portnum ==2:
            port = pygame.image.load('PORTAL2.png')
        port = port.convert_alpha()
        self.image = port
        self.height = height
        self.width = width
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        """ Update the state of the portal """
        self.rect.x += self.vx
        self.rect.y += self.vy
        block_hit_list = pygame.sprite.spritecollide(self, self.sprites, False)
        if len(block_hit_list)>0:
            for block in block_hit_list:
                if self.vy is not 0:
                    block.rect.x = self.portal_exit.rect.x+50
                    block.rect.y = self.portal_exit.rect.y+50
                    temp = -block.speed[0]
                    block.speed[0] = -block.speed[1]
                    block.speed[1] = temp
                if self.vx is not 0:
                    block.rect.x = self.portal_exit.rect.x+50
                    block.rect.y = self.portal_exit.rect.y+50
                    temp = -block.speed[0]
                    block.speed[0] = -block.speed[1]
                    block.speed[1] = temp   
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            self.vx = -self.vx
            self.vy = -self.vy
class PyGameKeyboardController:
    
    def __init__(self,model):
        self.model = model
        
    def handle_keyboard_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.model.player.changespeed(-SPEED,0)
            elif event.key == pygame.K_RIGHT:
                self.model.player.changespeed(SPEED,0)
            elif event.key == pygame.K_UP:
                self.model.player.changespeed(0,-SPEED)
            elif event.key == pygame.K_DOWN:
                self.model.player.changespeed(0,SPEED)
    # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.model.player.changespeed(SPEED,0)
            elif event.key == pygame.K_RIGHT:
                self.model.player.changespeed(-SPEED,0)
            elif event.key == pygame.K_UP:
                self.model.player.changespeed(0,SPEED)
            elif event.key == pygame.K_DOWN:
                self.model.player.changespeed(0,-SPEED)
            
class PyGameMouseController:
    def __init__(self,model):
        self.model = model

    def handle_mouse_event(self,event):
        """ Controlling the player using the mouse position """         
        if event.type ==MOUSEMOTION:
             self.model.player.rect.x =event.pos[0]
             self.model.player.rect.y =event.pos[1]
             
class MenuItem(pygame.font.Font):
    """ Creating the menu """
    def __init__(self, text, font=None, font_size=30,
                 font_color=(255, 255, 255), (pos_x, pos_y)=(0, 0)):
        """ Initializes variables for Menu """
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y
 
    def set_position(self, x, y):
        """ Sets menu position """
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y
 
    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)
 
    def is_mouse_selection(self, (posx, posy)):
        """ Checks if mouse is hovering over options """
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
            (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True
        return False
 
 
class GameMenu():
    def __init__(self, screen, items, bg_color=(0,0,0), font=None, font_size=30,
                    font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
 
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
 
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item)#, '/home/nebelhom/.fonts/SHOWG.TTF')
 
            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + (index * menu_item.height)
 
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
 
    def run(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
            mpos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            if item.text == "Start":
                                mainloop = False
                            else:
                                pygame.quit()
                                sys.exit()
            # Redraw the background
            self.screen.fill(self.bg_color)
 
            for item in self.items:
                if item.is_mouse_selection(pygame.mouse.get_pos()):
                    item.set_font_color((255, 0, 0))
                    item.set_italic(True)
                else:
                    item.set_font_color((255, 255, 255))
                    item.set_italic(False)
                self.screen.blit(item.label, item.position)
 
            pygame.display.flip()
 
if __name__ == '__main__':
    while 1:
        pygame.init()
        global LIVES
        LIVES =4
        size = (SCREEN_WIDTH,SCREEN_HEIGHT)
        screen = pygame.display.set_mode(size)
        
    
    
        menu_items = ('Start', 'Quit')
 
        pygame.display.set_caption('Game Menu')
        gm = GameMenu(screen, menu_items)
        gm.run()
        pygame.display.set_caption('The ImPAULssible Game           Lives: %d' %(LIVES))
        model  = BrickBreakerModel()
        controller = PyGameKeyboardController(model)
#       controller = PyGameMouseController(model)       
    
        pygame.mixer.music.load('Paul_Mixdown.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1.0)
    
        running = True
        ball = 0
        beginning = True
        while running:
            pygame.display.set_caption('The ImPAULssible Game           Lives: %d' %(LIVES))
            if LIVES <=0:
                running = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    controller.handle_keyboard_event(event)
                if event.type == KEYUP:
                    controller.handle_keyboard_event(event)
#            if event.type == MOUSEMOTION:
#                controller.handle_mouse_event(event)

            model.update()
            screen.fill((0,0,0))
            model.all_sprite_list.draw(screen)
            pygame.display.flip()
            time.sleep(.001)
            if beginning:
                time.sleep(1)
                beginning = False
            ball+=1
            if ball == 2000:
                ball = Ball(random.randint(200,SCREEN_WIDTH-200),random.randint(200,SCREEN_HEIGHT-200))
                ball.wallshorz = model.wall_list_horz
                ball.wallsvert = model.wall_list_vert
                model.ball_list.add(ball)
                model.all_sprite_list.add(ball)
                model.portals_list.add(ball)
                ball = 0
        pygame.mixer.music.stop()