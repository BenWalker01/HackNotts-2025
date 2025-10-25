import pygame

class Map:
    def __init__(self):
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption("HackNotts25")
        
    def handle_event(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
        
    def update_screen(self):
        ...