import pygame

class Map:
    def __init__(self):
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption("HackNotts25")
                
    def update_screen(self):
        self.screen.fill((0,0,0))