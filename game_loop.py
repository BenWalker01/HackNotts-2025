import pygame
import sys
from map import Map
from player import Player
from npc import NPC


class GameLoop:
    def __init__(self, player, map, npcs):
        self.player: Player = player
        self.map: Map = map
        self.npcs: list[NPC] = npcs

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())

            keys = pygame.key.get_pressed()
            self.player.walking = False
            if keys[pygame.K_a]:
                self.player.move_left()
            if keys[pygame.K_d]:
                self.player.move_right()
            if keys[pygame.K_w]:
                self.player.move_up()
            if keys[pygame.K_s]:
                self.player.move_down()

            for npc in self.npcs:
                npc.update()

            self.map.group.update()
            self.map.group.center(self.player.rect.center)
            self.map.update_screen()
            pygame.display.flip()
            clock.tick(60)
