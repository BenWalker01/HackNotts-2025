import pygame
import sys
from map import Map
from player import Player

class Game:
    def __init__(self,player, map):
        self.player : Player = player
        self.map : Map = map
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.player.move_left()
                        
                    if event.key == pygame.K_d:
                        self.player.move_right()
                        
                    if event.key == pygame.K_w:
                        self.player.move_up()
                        
                    if event.key == pygame.K_s:
                        self.player.move_down()
            
            self.map.update_screen()
            self.player.draw()
            pygame.display.update()
            