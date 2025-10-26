import pygame
import sys
from map import Map
from player import Player
from npc import NPC
from ui_manager import UIAssets, draw_textbox_

INTERACT_RADIUS = 12

class GameLoop:
    def __init__(self, player, map, npcs, state):
        self.player: Player = player
        self.map: Map = map
        self.npcs: list[NPC] = npcs
        self.state = state
        self.ui = UIAssets()

    def _nearest_npc_in_range(self, radius=INTERACT_RADIUS):
        px, py = self.player.rect.center
        best = None
        best_d2 = radius * radius
        for npc in self.npcs:
            nx, ny = npc.rect.center
            dx = nx - px
            dy = ny - py
            d2 = dx*dx + dy*dy
            if d2 <= best_d2:
                best = npc
                best_d2 = d2
        return best

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # NEW: handle E press to talk to nearest NPC
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    npc = self._nearest_npc_in_range()
                    if npc is not None:
                        text = self.state.get_one_rumor_text()
                        screen = pygame.display.get_surface()
                        draw_textbox_(screen, self.ui, text)
                        print("[Rumor]", text)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        if self.state.dialog_visible:
                            self.state.close_dialog()
                        else:
                            npc = self._nearest_npc_in_range()
                            if npc is not None:
                                self.state.open_rumor_dialog()

                    # optional quick close keys:
                    if event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                        self.state.close_dialog()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())

            keys = pygame.key.get_pressed()
            self.player.walking = False

            if not self.state.dialog_visible:
                if keys[pygame.K_a]: self.player.move_left()
                if keys[pygame.K_d]: self.player.move_right()
                if keys[pygame.K_w]: self.player.move_up()
                if keys[pygame.K_s]: self.player.move_down()

            for npc in self.npcs:
                npc.update()

            self.map.group.update()
            self.map.group.center(self.player.rect.center)
            self.map.update_screen()

            screen = pygame.display.get_surface()
            if self.state.dialog_visible:
                draw_textbox_(screen, self.ui, self.state.dialog_text)

            pygame.display.flip()
            clock.tick(60)
