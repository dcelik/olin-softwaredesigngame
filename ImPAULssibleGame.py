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

class BrickBreakerModel:
    """ This class encodes the game state """
    def __init__(self):
        self.all_sprite_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        wallleft = Wall(640,10,0,0)
        wallright = Wall(640,10,630,0)
        walltop = Wall(10,640,)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        
        
        
        self.walls = []
        wallleft = Wall(,640,10,0,0)
        wallright = Wall(40,10,630,0)
        walltop = Wall(10,640,0,0)
        wallbot = Wall((random.randint(0,255),random.randint(0,255),random.randint(0,255)),10,640,0,630)        
        self.walls.append(wallleft)
        self.walls.append(wallright)
        self.walls.append(walltop)
        self.walls.append(wallbot)
        self.paddle = Paddle((random.randint(0,255),random.randint(0,255),random.randint(0,255)),20,100,200,450)
    def update(self):
        self.paddle.update()

class Wall(pygame.sprite.Sprite):
    """ Encodes the state of a brick in the game """
    def __init__(self,height,width,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.color = (255,255,255)
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        
class Paddle:
    """ Encodes the state of the paddle in the game"""
    def __init__(self,color,height,width,x,y):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0

    def update(self):
        """ Update the state of the paddle """
        self.x += self.vx
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
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.paddle.vx +=-1.0
        if event.key == pygame.K_RIGHT:
            self.model.paddle.vx +=1.0
        if event.key == pygame.K_DOWN:
            self.model.paddle.vy +=1.0
        if event.key == pygame.K_UP:
            self.model.paddle.vy +=-1.0
            
class PyGameMouseController:
    def __init__(self,model):
        self.model = model

    def handle_mouse_event(self,event):
         if event.type ==MOUSEMOTION:
             self.model.paddle.x =event.pos[0]-self.model.paddle.width
             self.model.paddle.y =event.pos[1]-self.model.paddle.height

if __name__ == '__main__':
    pygame.init()

    size = (640,640)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('The ImPAULssible Game)
    
    model  = BrickBreakerModel()
    view = PyGameWindowView(model,screen)
#    controller = PyGameKeyboardController(model)
    controller = PyGameMouseController(model)    
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
#            if event.type == KEYDOWN:
#                controller.handle_keyboard_event(event)
            if event.type == MOUSEMOTION:
                controller.handle_mouse_event(event)
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()