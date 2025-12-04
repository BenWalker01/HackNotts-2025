import pygame
import sys
from map import Map
from player import Player
from npc import NPC
from ui_manager import UIAssets, draw_textbox_
import logic.market_api as api
import logic.economy_bootstrap as eb

INTERACT_RADIUS = 12


class GameLoop:
    def __init__(self, player, maps: dict[str, Map], npcs, state):
        self.player: Player = player
        self.maps = maps
        self.current_map = "main"
        self.map: Map = self.maps[self.current_map]
        self.player_positions = {name: None for name in self.maps}
        self.player_positions[self.current_map] = getattr(
            self.player, "rect", None).topleft
        try:
            self.map.add_player(self.player)
        except Exception:
            pass

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
            print(f"[Map] Unknown map '{name}'")
            return

        # save current position for return trips
        if getattr(self.player, "rect", None):
            self.player_positions[self.current_map] = self.player.rect.topleft

        # swap active map
        self.current_map = name
        self.map = self.maps[name]

        # restore previous position or use map spawn or default
        spawn = (
            self.player_positions.get(name)
            or getattr(self.map, "spawn_pos", None)
            or (100, 100)
        )
        if getattr(self.player, "rect", None):
            self.player.rect.topleft = spawn
            # keep x/y in sync if your Player uses both
            if hasattr(self.player, "x"):
                self.player.x = spawn[0]
            if hasattr(self.player, "y"):
                self.player.y = spawn[1]

        # update player→map links
        if hasattr(self.player, "set_map"):
            self.player.set_map(self.map)
        try:
            self.map.add_player(self.player)
        except Exception:
            pass

        # center camera and redraw
        self.map.group.center(self.player.rect.center)
        self.map.update_screen()

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
    
    def _nearest_coord_in_range(self, radius=INTERACT_RADIUS):
        px, py = self.player.rect.center
        best = None
        best_d2 = radius * radius
        for npc in self.npcs:
            if hasattr(npc, "map_name") and npc.map_name != self.current_map:
                continue
            nx, ny = 217, 173
            d2 = (nx - px) * (nx - px) + (ny - py) * (ny - py)
            if d2 <= best_d2:
                best, best_d2 = npc, d2
        return best

    def is_near_point(self, point_xy, radius=INTERACT_RADIUS) -> bool:
        """Return True if the player is within radius of point_xy (x,y) in world pixels."""
        px, py = self.player.rect.center
        x, y = point_xy
        dx, dy = x - px, y - py
        return (dx*dx + dy*dy) <= (radius * radius)


    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:

            self.player.check_near_building(self.maps[self.current_map])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Talk to NPC / toggle textbox
                    if event.key == pygame.K_e:
                        if self.state.dialog_visible:
                            self.state.close_dialog()
                        else:
                            near_market_stand = self.is_near_point((217, 173), radius=12)
                            npc = self._nearest_npc_in_range()
                            if npc is not None:
                                self.state.open_rumor_dialog()
                            elif near_market_stand:
                                # Show first vendor's inventory
                                vendor_keys = list(eb.VENDORS.keys())
                                if vendor_keys:
                                    first_vendor = vendor_keys[0]
                                    formatted_text = self.state.format_buy_snapshot(first_vendor)
                                    self.state.set_dialog(formatted_text)
                                else:
                                    self.state.set_dialog("No vendors available.")

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if self.current_map == "main" and getattr(self.player, "near_building", None):
                            target = self.player.near_building.get(
                                "target_map")
                            if target:
                                self.load_map(target)
                        elif self.current_map != "main":
                            self.load_map("main")

                    # quick close for dialog
                    if event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                        self.state.close_dialog()

            keys = pygame.key.get_pressed()
            self.player.walking = False

            # freeze movement while dialog open
            if not self.state.dialog_visible:
                if keys[pygame.K_a]:
                    self.player.move_left()
                if keys[pygame.K_d]:
                    self.player.move_right()
                if keys[pygame.K_w]:
                    self.player.move_up()
                if keys[pygame.K_s]:
                    self.player.move_down()

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
