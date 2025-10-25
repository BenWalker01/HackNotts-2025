import pygame
import sys
from map import Map
from player import Player


class Game:
    def __init__(self, player, map):
        self.player: Player = player
        self.map: Map = map

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.player.walking = False
            if keys[pygame.K_a]:
                self.player.move_left()
            elif keys[pygame.K_d]:
                self.player.move_right()
            elif keys[pygame.K_w]:
                self.player.move_up()
            elif keys[pygame.K_s]:
                self.player.move_down()

            self.map.group.update()
            self.map.group.center(self.player.rect.center)
            self.map.update_screen()
            pygame.display.flip()
            clock.tick(60)
