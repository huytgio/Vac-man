import pygame as py
from pygame.math import Vector2 as vec
from setting import *
from pygame.locals import (RLEACCEL)


class Player:
    def __init__(self,app,pos):
        self.app = app
        self.grid_pos = vec(pos[0],pos[1])
        self.direction = vec(1,0)
        self.pix_pos = self.get_pix_pos()
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.highscore = None
        self.p_pos = [pos.x, pos.y]
        self.speed = 1
        self.lives = 1
       
        
    def update(self):
        self.highscore = 0
        if self.update_highscore():
            self.highscore = self.current_score
       
        if self.pix_pos == [30,315]:
            self.pix_pos = [570,315]
        if self.pix_pos == [580,315]:
            self.pix_pos = [30,315]
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
            
     
        
        if self.time_to_move():
                if self.stored_direction != None:
                    self.direction = self.stored_direction
                self.able_to_move = self.can_move()
                
        
        
                
        # print(self.grid_pos,self.direction,self.grid_pos + self.direction)
       
        
        self.grid_pos[0]= (self.pix_pos[0]-TOP_BOTTOM_BF+self.app.cell_width//2)//self.app.cell_width+1
        
        self.grid_pos[1]= (self.pix_pos[1]-TOP_BOTTOM_BF+self.app.cell_height//2)//self.app.cell_height+1
        
        if self.on_coin():
            self.eat_coin()
        
    
    
    def on_coin(self):
        if self.grid_pos in self.app.coin:
            if int(self.pix_pos.x + TOP_BOTTOM_BF //2) % self.app.cell_width == 0:
               if self.direction == vec(1,0) or self.direction == vec(-1,0):
                 return True
            if int(self.pix_pos.y + TOP_BOTTOM_BF //2) % self.app.cell_height == 0:
               if self.direction == vec(0,1) or self.direction == vec(0,-1):
                 return True
        return False
     
    def eat_coin(self):
       
        self.app.coin.remove(self.grid_pos)
        self.current_score += 1
    
    
    def draw(self):
       py.draw.circle(self.app.screen,PLAYER_COL, (int(self.pix_pos.x),int(self.pix_pos.y)), self.app.cell_width//2-2)
       # py.draw.rect(self.app.screen, (255,0,0), (self.grid_pos.x*self.app.cell_width+TOP_BOTTOM_BF//2,
       #                                           self.grid_pos.y*self.app.cell_height+TOP_BOTTOM_BF//2,
       #                                           self.app.cell_width,self.app.cell_height),1,)
       for x in range(self.lives):
           py.draw.circle(self.app.screen,PLAYER_COL, (100 + x * 20,HEIGHT-12), self.app.cell_width//2)
    
    def move(self, direction):
        self.stored_direction = direction
    
    
    def get_pix_pos(self):
        return vec((self.grid_pos[0] * self.app.cell_width)+TOP_BOTTOM_BF//2 + self.app.cell_width//2
                            , (self.grid_pos[1] * self.app.cell_height)+TOP_BOTTOM_BF//2 + self.app.cell_height//2)
    
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BF //2) % self.app.cell_width == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0) or self.direction == vec(0,0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BF //2) % self.app.cell_height == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1) or self.direction == vec(0,0):
                return True
            
    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True
    def update_highscore(self):
        if self.current_score > self.highscore:
            return True
        return False
    
    
        
      