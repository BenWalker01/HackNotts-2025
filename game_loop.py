import pygame
import sys
from map import Map
from player import Player
from npc import NPC


class GameLoop:
    def __init__(self, player, maps, npcs):
        self.player: Player = player
        self.maps: dict[str, Map] = maps
        self.npcs: list[NPC] = npcs
        self.screen = pygame.display.get_surface()

        # Load speech bubble image
        self.speech_bubble = pygame.image.load(
            "assets/speech/pixel-speech-bubble-enter.png")
        self.speech_bubble = pygame.transform.scale(
            self.speech_bubble, (200, 100))  # Adjust size as needed

        try:
            self.book_surf = pygame.image.load(
                "assets/speech/W_Book01.png").convert_alpha()
            self.book_surf = pygame.transform.scale(self.book_surf, (24, 28))
        except Exception:
            book_w, book_h = 24, 28
            self.book_surf = pygame.Surface((book_w, book_h), pygame.SRCALPHA)
            self.book_surf.fill((235, 195, 120))
            pygame.draw.rect(self.book_surf, (120, 80, 40),
                             self.book_surf.get_rect(), 2)

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

            for npc in self.npcs:
                if npc.map == self.map:
                    npc.update()
            self.map.group.update()
            self.map.group.center(self.player.rect.center)
            self.map.update_screen()

            if self.current_map == "main" and self.player.near_building:
                padding = 8
                book_w, book_h = self.book_surf.get_size()
                book_x = padding
                book_y = self.screen.get_height() - book_h - padding

                bubble_x = book_x + book_w + 6
                bubble_y = self.screen.get_height() - self.speech_bubble.get_height() - padding

                max_bubble_x = self.screen.get_width() - self.speech_bubble.get_width() - padding
                if bubble_x > max_bubble_x:
                    shift = bubble_x - max_bubble_x
                    bubble_x -= shift
                    book_x = max(padding, book_x - shift)

                self.screen.blit(self.book_surf, (book_x, book_y))
                self.screen.blit(self.speech_bubble, (bubble_x, bubble_y))

            pygame.display.flip()
            clock.tick(60)
