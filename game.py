import pygame
import sys
import os
from map import Map
from player import Player


class Game:
    def __init__(self, player, map):
        self.player: Player = player
        self.map: Map = map
        self.current_building = None

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
            
            keys = pygame.key.get_pressed()
            self.player.walking = False
            
            # Left movement: A or LEFT arrow
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.player.move_left()
            
            # Right movement: D or RIGHT arrow
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.player.move_right()
            
            # Up movement: W or UP arrow
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.player.move_up()
            
            # Down movement: S or DOWN arrow
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.player.move_down()

            # Check if player is near a building (object triggers)
            self.current_building = self.map.check_building_collision(self.player.rect)

            # Check if player is standing on a non-zero tile in the "market" layer
            player_cx, player_cy = self.player.rect.center
            on_market_tile = self.map.is_on_nonzero_layer("market", player_cx, player_cy)

            self.map.group.update()
            self.map.group.center(self.player.rect)
            self.map.update_screen()
            
            # Draw caption if near a building (object) or on market tile
            if self.current_building:
                caption_text = f"Press ENTER to enter {self.current_building['name']}"
                caption_pos = (
                    self.map.screen.get_width() // 2,
                    self.map.screen.get_height() // 2 - 50
                )
                self.map.draw_caption(caption_text, caption_pos)
            elif on_market_tile:
                caption_text = "Click enter to go in the building"
                caption_pos = (
                    self.map.screen.get_width() // 2,
                    self.map.screen.get_height() // 2 - 50
                )
                self.map.draw_caption(caption_text, caption_pos)

            # Handle KEYDOWN events (Enter) after we know context
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if on_market_tile:
                            # Load market map
                            market_path = "assets\\tileset\\market.tmx"
                            print("Entering Market...")
                            # optional: save old player pos if needed
                            self.map.load_map(market_path)
                            self.player.x = 100
                            self.player.y = 100
                            self.map.add_player(self.player)
                        elif self.current_building:
                            self.enter_building(self.current_building)
            
            pygame.display.flip()
            clock.tick(60)
    
    def enter_building(self, building):
        """Load the building's interior map"""
        map_file = building.get("map_file", "")
        if map_file:
            print(f"Entering {building['name']}...")
            # Store player position before entering
            old_x, old_y = self.player.x, self.player.y
            
            # Construct the full path based on the map file
            if "tavern-preview.tmx" in map_file:
                full_path = "assets\\tileset\\lpc-tavern\\lpc-tavern\\preview\\tavern-preview.tmx"
            else:
                full_path = f"assets\\tileset\\{map_file}"
            
            # Load new map
            self.map.load_map(full_path)
            
            # Reset player position for interior (you can customize this)
            self.player.x = 100
            self.player.y = 100
            
            # Re-add player to new map
            self.map.add_player(self.player)