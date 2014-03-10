# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:34:24 2014

@author: pruvolo
"""

import pygame
from pygame.locals import *
import random
import math
import time

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SPEED = 2
LIVES = 3

class BrickBreakerModel:
    """ This class encodes the game state """
    def __init__(self):
        self.all_sprite_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.wall_list_vert = pygame.sprite.Group()
        self.wall_list_horz = pygame.sprite.Group()
        self.ball_list = pygame.sprite.Group()
        
        wallleft = Wall(SCREEN_HEIGHT,10,0,0)
        wallright = Wall(SCREEN_HEIGHT,10,SCREEN_WIDTH-10,0)
        walltop = Wall(10,SCREEN_WIDTH,0,0)
        wallbot = Wall(10,SCREEN_WIDTH,0,SCREEN_HEIGHT-10)
        
        self.wall_list.add(wallleft)
        self.all_sprite_list.add(wallleft)
        self.wall_list_vert.add(wallleft)
        
        self.wall_list.add(wallright)
        self.all_sprite_list.add(wallright)
        self.wall_list_vert.add(wallright)
        
        self.wall_list.add(walltop)
        self.all_sprite_list.add(walltop)
        self.wall_list_horz.add(walltop)
        
        self.wall_list.add(wallbot)
        self.all_sprite_list.add(wallbot)
        self.wall_list_horz.add(wallbot)
                
        ball = Ball(random.randint(200,SCREEN_WIDTH-200),random.randint(200,SCREEN_HEIGHT-200))
        self.ball_list.add(ball)
        self.all_sprite_list.add(ball)
        ball.wallshorz = self.wall_list_horz
        ball.wallsvert = self.wall_list_vert
        
        ball = Ball(random.randint(200,SCREEN_WIDTH-200),random.randint(200,SCREEN_HEIGHT-200))
        self.ball_list.add(ball)
        self.all_sprite_list.add(ball)
        ball.wallshorz = self.wall_list_horz
        ball.wallsvert = self.wall_list_vert
        
        ball = Ball(random.randint(200,SCREEN_WIDTH-200),random.randint(200,SCREEN_HEIGHT-200))
        self.ball_list.add(ball)
        self.all_sprite_list.add(ball)
        ball.wallshorz = self.wall_list_horz
        ball.wallsvert = self.wall_list_vert
        
        self.player = Player(SCREEN_HEIGHT/2,SCREEN_HEIGHT/2)
        self.player.walls = self.wall_list
        self.player.balls = self.ball_list
        self.all_sprite_list.add(self.player) 
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
    velx = random.randint(1,3)
    vely = random.randint(1,3)
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
    

class Portal:
    """ Encodes the state of the portal in the game"""
    def __init__(self,color,height,width,x,y,vx,vy):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        """ Update the state of the portal """
        self.x += self.vx
        self.y += self.vy

class PyGameWindowView:
    """ A view of brick breaker rendered in a Pygame window"""
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for wall in self.model.walls:
            pygame.draw.rect(self.screen, pygame.Color(wall.color[0],wall.color[1],wall.color[2]),pygame.Rect(wall.x,wall.y,wall.width,wall.height))            
        pygame.draw.rect(self.screen, pygame.Color(self.model.paddle.color[0],self.model.paddle.color[1],self.model.paddle.color[2]),pygame.Rect(self.model.paddle.x,self.model.paddle.y,self.model.paddle.width,self.model.paddle.height))
        pygame.display.update()

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
         if event.type ==MOUSEMOTION:
             self.model.player.rect.x =event.pos[0]
             self.model.player.rect.y =event.pos[1]

if __name__ == '__main__':
    pygame.init()
    global LIVES
    size = (SCREEN_WIDTH,SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('The ImPAULssible Game')
    
    model  = BrickBreakerModel()
    controller = PyGameKeyboardController(model)
#    controller = PyGameMouseController(model)    
    
    pygame.mixer.music.load('Paul_Mixdown.ogg')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.0)
    
    running = True
    ball = 0
    while running:
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
#
        model.update()
        screen.fill((0,0,0))
        model.all_sprite_list.draw(screen)
        pygame.display.flip()
        time.sleep(.001)
        ball+=1
        if ball == 3000:
            ball = Ball(random.randint(200,SCREEN_WIDTH-200),random.randint(200,SCREEN_HEIGHT-200))
            ball.wallshorz = model.wall_list_horz
            ball.wallsvert = model.wall_list_vert
            model.ball_list.add(ball)
            model.all_sprite_list.add(ball)
            ball = 0
    pygame.quit()