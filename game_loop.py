import pygame
import sys
from map import Map
from player import Player
from npc import NPC

INTERACT_RADIUS = 12


class GameLoop:
    def __init__(self, player, maps, npcs, state):
        self.player: Player = player
        self.maps: dict[str, Map] = maps
        self.npcs: list[NPC] = npcs
        self.state = state

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

        self.current_map = "main"
        self.map = self.maps[self.current_map]

        # Store player positions per map
        self.player_positions = {name: (100, 100) for name in maps}

        # Setup map & player
        self.player.set_map(self.map)
        self.map.add_player(self.player)

        # Assign NPCs to their maps (once)
        for npc in self.npcs:
            npc_map = npc.map_name if hasattr(npc, "map_name") else "main"
            if npc_map in self.maps:
                npc.set_map(self.maps[npc_map])
                self.maps[npc_map].group.add(npc)

    def load_map(self, target_map_name):
        """Switch to a new map, remembering positions."""
        if target_map_name not in self.maps:
            print(f"Error: Map '{target_map_name}' not loaded.")
            return

        # Save position before switching
        self.player_positions[self.current_map] = (
            self.player.x, self.player.y)

        print(f"Switching to map: {target_map_name}")
        self.current_map = target_map_name
        self.map = self.maps[self.current_map]

        # Restore previous position on new map
        spawn_x, spawn_y = self.player_positions.get(
            target_map_name, (100, 100))
        self.player.x, self.player.y = spawn_x, spawn_y
        self.player.rect.topleft = (spawn_x, spawn_y)

        # Update player’s map reference
        self.player.set_map(self.map)
        self.map.add_player(self.player)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.player.check_near_building(self.map)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Enter building
                        if self.current_map == "main" and self.player.near_building:
                            self.load_map(
                                self.player.near_building["target_map"])
                        # Leave building
                        elif self.current_map != "main":
                            self.load_map("main")

            # Player movement
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

            # Update only NPCs on the current map
            for npc in self.npcs:
                if npc.map == self.map:
                    npc.update()

            # Update and draw
            self.map.group.update()
            self.map.group.center(self.player.rect.center)
            self.map.update_screen()
            pygame.display.flip()
            clock.tick(60)
