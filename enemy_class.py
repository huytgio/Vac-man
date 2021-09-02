import pygame as py
from pygame.math import Vector2 as vec
from setting import *
import random
class Enemy:
    def __init__(self,app,pos,number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.direct = vec(1,0)
        self.ps = self.set_ps()
        
        
    
        
    def update(self):
        print(self.grid_pos)
       
        self.pix_pos += self.direct
            
     
        
        if self.time_to_move():
            self.move()
        
        self.grid_pos[0]= (self.pix_pos[0]-TOP_BOTTOM_BF+self.app.cell_width//2)//self.app.cell_width+1
        
        self.grid_pos[1]= (self.pix_pos[1]-TOP_BOTTOM_BF+self.app.cell_height//2)//self.app.cell_height+1
    
    def draw(self):
        if self.number >= 0:
             py.draw.circle(self.app.screen,(140,30,175), (int(self.pix_pos.x),int(self.pix_pos.y)),self.radius)
             
    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width)+TOP_BOTTOM_BF//2 + self.app.cell_width//2
                            , (self.grid_pos.y * self.app.cell_height)+TOP_BOTTOM_BF//2 + self.app.cell_height//2)
    
    def set_ps(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "run"
        elif self.number == 2:
            return "noob"
        elif self.number == 3:
            return "clone"
        
    def move(self):
        if self.ps == 'speedy':
         self.direct = self.get_random_direction()
    
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BF //2) % self.app.cell_width == 0:
            if self.direct == vec(1,0) or self.direct == vec(-1,0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BF //2) % self.app.cell_height == 0:
            if self.direct == vec(0,1) or self.direct == vec(0,-1):
                return True
        return False
    
    def get_random_direction(self):
        while True:
            number = random.randint(0, 80)
            if number >= 0 and number <=20:
                x_dir, y_dir = 1, 0
            elif number >= 20 and number <=40:
                x_dir, y_dir = 0, 1
            elif number >= 40 and number <=60:
                x_dir, y_dir = -1, 0
            elif number >= 60 and number <=80:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)
