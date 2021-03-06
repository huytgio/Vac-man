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
        self.color = self.set_color()
        self.direct = vec(1,0)
        self.ps = self.set_ps()
        self.target = None
        self.speed = self.get_speed()
        self.p_pos = [pos.x, pos.y]
        
    def update(self):
        
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direct * self.speed
            if self.time_to_move():
                self.move()
        print(self.app.player.grid_pos)
        
        self.grid_pos[0]= (self.pix_pos[0]-TOP_BOTTOM_BF+
                           self.app.cell_width//2)//self.app.cell_width+1
        
        self.grid_pos[1]= (self.pix_pos[1]-TOP_BOTTOM_BF+
                           self.app.cell_height//2)//self.app.cell_height+1
        
    
    def get_speed(self):
        if self.number == 0:
            speed = 1
        if self.number > 0:
            speed = 0.8
        return speed
        
        
        
        
    def draw(self):
        
        if self.number >= 0:
              py.draw.circle(self.app.screen,self.color, (int(self.pix_pos.x),
                                                            int(self.pix_pos.y)),
                             self.radius)
    
    def set_target(self):
        if self.ps == "multi":
            if self.app.player.grid_pos[0] > 28//2 and self.app.player.grid_pos[1] > 32//2:
                return (2,2)
            if self.app.player.grid_pos[0] > 28//2 and self.app.player.grid_pos[1] < 32//2:
                return (2,ROWS-3)
            if self.app.player.grid_pos[0] < 28//2 and self.app.player.grid_pos[1] > 32//2:
                return (COLS-3,2)
            else:
                return (COLS-3,ROWS-3)
                 
        
            
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BF //2) % self.app.cell_width == 0:
            if self.direct == vec(1,0) or self.direct == vec(-1,0) or self.direct == vec(0,0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BF //2) % self.app.cell_height == 0:
            if self.direct == vec(0,1) or self.direct == vec(0,-1) or self.direct == vec(0,0):
                return True
        return False
    
    def move(self):
        if self.ps == 'orgin':
          self.direct = self.get_random_direction()
        # if self.ps == 'clone':
        #   self.direct = self.get_path_direction()
        if self.ps == 'multi':
          self.direct = self.get_path_direction(self.target)
          
    def get_path_direction(self,target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)
    
    def find_next_cell_in_path(self,target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
                        int(target[0]), int(target[1])])
        return path[1]
    
    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(32)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 32:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest
    
    
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
    
    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width)+TOP_BOTTOM_BF//2 + self.app.cell_width//2
                            , (self.grid_pos.y * self.app.cell_height)+TOP_BOTTOM_BF//2 + self.app.cell_height//2)
    
    def set_color(self):
        if self.number == 0:
           return (45,78,203)
        if self.number > 0:
           return (197,200,27)
    
    def set_ps(self):
        if self.number == 0:
            return "orgin"
        # elif self.number == 1:
        #     return "clone"
        else:
            return "multi"
        
    
    
   