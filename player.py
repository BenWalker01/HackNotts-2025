import pygame

SPEED = 5

class Player:
    def __init__(self,window):
        self.x,self.y = (100,100)
        self.window = window
        
        
    def draw(self):
        pygame.draw.circle(self.window.screen, (0,0,255), (self.x,self.y), 5)
        
    def move_up(self):
        self.y -= SPEED
    def move_down(self):
        self.y += SPEED
    def move_left(self):
        self.x -= SPEED
    def move_right(self):
        self.x += SPEED