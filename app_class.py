import pygame, sys
from setting import *
from player_class import *



Vec = pygame.math.Vector2()
pygame.init()

## Game inittialized
class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock  = pygame.time.Clock()
        self.running= True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//28
        self.cell_height = MAZE_HEIGHT//32
        self.player = Player(self,PLAYER_START_POS)
        self.walls = []
        self.gate = []
        
        self.load()
        
        
        
    def run(self):
        while self.running:
    
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            if self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            if self.state == "quit":
                self.running = False
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
## Common Function        
    def draw_text(self,pos,text,screen,size,color,font_name,center = False):
        font = pygame.font.Font(font_name, size)
        text = font.render(text, False, color)
        text_size = text.get_size()
        if center:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)
    
    def load(self):
        self.background = pygame.image.load('./img/maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH,MAZE_HEIGHT))
        with open('wall.txt','r') as file:
            for yidx,line in enumerate(file):
                for xidx,char in enumerate(line):
                    if char == '1':
                       self.walls.append(vec(xidx,yidx))
        
       
    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, (255,255,255), (x * self.cell_width,0), (x*self.cell_width,HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, (255,255,255), (0,x * self.cell_height), (WIDTH,x*self.cell_height))
        for wall in self.walls:
            pygame.draw.rect(self.background,(200,200,200),(wall.x * self.cell_width,wall.y * self.cell_height,
                                                            self.cell_width,self.cell_height))
    
## Start Function        
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = 'quit'
                
    def start_update(self):
       pass
        
        
    
    
    def start_draw(self):
       
        self.screen.fill((0,0,0))
        self.draw_text([WIDTH//2,HEIGHT//2],'PUSH SPACE BAR',self.screen,START_TEXT_SIZE,COLOR_LIST[0],START_FONT,center = True)
        self.draw_text([WIDTH//2,HEIGHT//2+40],'1 PLAYER ONLY',self.screen,START_TEXT_SIZE,(33,137,156),START_FONT,center = True)
        self.draw_text([5,0],'HIGHSCORE',self.screen,START_TEXT_SIZE,(255,255,255),START_FONT)
        pygame.display.update()
## Playing Function
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                   
                    self.player.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    
                    self.player.move(vec(+1,0))
                if event.key == pygame.K_UP:
                  
                    self.player.move(vec(0,-1))
                if event.key == pygame.K_DOWN:
                   
                    self.player.move(vec(0,+1))
                
    def playing_update(self):
        self.player.update()
    
    
    def playing_draw(self):
        self.screen.fill((8,23,84))
        self.screen.blit(self.background, (TOP_BOTTOM_BF//2,TOP_BOTTOM_BF//2))
        # self.draw_grid()
        self.draw_text([5,2],'SCORE:0',self.screen,START_TEXT_SIZE,(255,255,255),START_FONT)
        self.draw_text([WIDTH//2+50,2],'HIGHSCORE:',self.screen,START_TEXT_SIZE,(255,255,255),START_FONT)
        self.player.draw()
        pygame.display.update()