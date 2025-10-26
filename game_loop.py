import pygame, sys
from map import Map
from player import Player
from npc import NPC
from ui_manager import UIAssets, draw_textbox_

INTERACT_RADIUS = 12

class GameLoop:
    def __init__(self, player, maps: dict[str, Map], npcs, state):
        self.player: Player = player
        self.maps = maps
        self.current_map = "main"   
        self.map: Map = self.maps[self.current_map]

        self.npcs: list[NPC] = npcs
        self.state = state
        self.ui = UIAssets()

        try:
            self.map.add_player(self.player)
        except Exception:
            pass

    def load_map(self, name: str):
        """Switch to another map (e.g., tavern/market) and re-center camera."""
        if name not in self.maps:
            return
        self.current_map = name
        self.map = self.maps[name]
        self.map.group.center(self.player.rect.center)
        self.map.update_screen()
        try:
            self.map.add_player(self.player)
        except Exception:
            pass

    def _nearest_npc_in_range(self, radius=INTERACT_RADIUS):
        px, py = self.player.rect.center
        best = None
        best_d2 = radius * radius
        for npc in self.npcs:
            if hasattr(npc, "map_name") and npc.map_name != self.current_map:
                continue
            nx, ny = npc.rect.center
            d2 = (nx - px) * (nx - px) + (ny - py) * (ny - py)
            if d2 <= best_d2:
                best, best_d2 = npc, d2
        return best

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Talk to NPC / toggle textbox
                    if event.key == pygame.K_e:
                        if self.state.dialog_visible:
                            self.state.close_dialog()
                        else:
                            npc = self._nearest_npc_in_range()
                            if npc is not None:
                                self.state.open_rumor_dialog()

                    # Enter/leave buildings (Enter)
                    if event.key == pygame.K_RETURN:
                        # if your Player exposes near_building with {"target_map": ...}
                        if self.current_map == "main" and getattr(self.player, "near_building", None):
                            target = self.player.near_building.get("target_map")
                            if target: self.load_map(target)
                        elif self.current_map != "main":
                            self.load_map("main")

                    # quick close for dialog
                    if event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                        self.state.close_dialog()

            keys = pygame.key.get_pressed()
            self.player.walking = False

            # freeze movement while dialog open
            if not self.state.dialog_visible:
                if keys[pygame.K_a]: self.player.move_left()
                if keys[pygame.K_d]: self.player.move_right()
                if keys[pygame.K_w]: self.player.move_up()
                if keys[pygame.K_s]: self.player.move_down()

            # update only NPCs on the current map
            for npc in self.npcs:
                if not hasattr(npc, "map_name") or npc.map_name == self.current_map:
                    npc.update()

            # draw world
            self.map.group.update()
            self.map.group.center(self.player.rect.center)
            self.map.update_screen()

            # draw dialog on top
            if self.state.dialog_visible:
                screen = pygame.display.get_surface()
                draw_textbox_(screen, self.ui, self.state.dialog_text)

            pygame.display.flip()
            clock.tick(60)
