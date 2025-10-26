import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface
import pyscroll
import pytmx

TILE_SIZE = 16


class Map:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("HackNotts25")
        self.current_map = "assets/tileset/baseMap.tmx"
        self.load_map(self.current_map)
        self.tile_size = TILE_SIZE  # Track current tile size

        # Load font for captions
        self.font = pygame.font.Font("assets/font.ttf", 24)

    def update_screen(self):
        self.group.draw(self.screen)

    def load_map(self, map_path):
        self.current_map = map_path
        self.tmx_data = pytmx.util_pygame.load_pygame(map_path)
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.tile_size = self.tmx_data.tilewidth
        self.collision = [[False for _ in range(self.tmx_data.width)]
                          for _ in range(self.tmx_data.height)]
        
        # Load collision layer
        try:
            collision_layer = self.tmx_data.get_layer_by_name("Collision")
            for x, y, tile in collision_layer.tiles():
                if tile:
                    self.collision[y][x] = True
        except ValueError:
            print("No Collision layer found")

        # Load building triggers from object layers
        self.building_triggers = []
        try:
            # Check all layers for object layers
            for layer in self.tmx_data.layers:
                if isinstance(layer, pytmx.TiledObjectGroup):
                    if layer.name == "Buildings":
                        for obj in layer:
                            building_info = {
                                "name": obj.name,
                                "rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                                "map_file": obj.properties.get("map_file", "")
                            }
                            self.building_triggers.append(building_info)
                            print(f"Loaded building trigger: {obj.name}")
        except Exception as e:
            print(f"Error loading building triggers: {e}")
            self.building_triggers = []

        # Build quick lookup for named tile layers (store gids)
        self.tile_layers = {}
        # Index specific named tile layers we care about
        for name in ("market", "tavern"):
            try:
                layer = self.tmx_data.get_layer_by_name(name)
                layer_tiles = [[0 for _ in range(self.tmx_data.width)]
                               for _ in range(self.tmx_data.height)]
                for x, y, gid in layer.tiles():
                    layer_tiles[y][x] = gid
                self.tile_layers[name] = layer_tiles
            except ValueError:
                # layer not present — skip
                pass

        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size())
        base_zoom = 3
        if self.tile_size == 32:
            base_zoom = 1.5  # Half zoom for double-sized tiles
        elif self.tile_size == 16:
            base_zoom = 3
        map_layer.zoom = base_zoom

        self.group = pyscroll.PyscrollGroup(
            map_layer=map_layer, default_layer=1)

    def add_player(self, player):
        self.group.add(player, layer=999)
        self.group.update()
        print("added player")

    def can_move_to(self, px, py):
        tile_x = int(px / self.tile_size)
        tile_y = int(py / self.tile_size)
        if 0 <= tile_x < self.tmx_data.width and 0 <= tile_y < self.tmx_data.height:
            return not self.collision[tile_y][tile_x]
        return False
    
    def check_building_collision(self, player_rect):
        """Check if player is colliding with any building trigger"""
        for building in self.building_triggers:
            if player_rect.colliderect(building["rect"]):
                return building
        return None
    
    def draw_caption(self, text, position):
        """Draw a caption on screen"""
        # Create text surface with shadow
        shadow = self.font.render(text, True, (0, 0, 0))
        text_surface = self.font.render(text, True, (255, 255, 255))
        
        # Create background box
        padding = 10
        box_width = text_surface.get_width() + padding * 2
        box_height = text_surface.get_height() + padding * 2
        box_surface = pygame.Surface((box_width, box_height))
        box_surface.set_alpha(180)
        box_surface.fill((50, 50, 50))
        
        # Center the caption at the given position
        box_x = position[0] - box_width // 2
        box_y = position[1] - box_height - 20
        
        # Draw box, shadow, and text
        self.screen.blit(box_surface, (box_x, box_y))
        self.screen.blit(shadow, (box_x + padding + 2, box_y + padding + 2))
        self.screen.blit(text_surface, (box_x + padding, box_y + padding))

    def is_on_nonzero_layer(self, layer_name, px, py):
        """Return True if the tile under (px,py) on layer_name has a non-zero gid."""
        tile_x = int(px / self.tile_size)
        tile_y = int(py / self.tile_size)
        if layer_name not in self.tile_layers:
            return False
        if 0 <= tile_x < self.tmx_data.width and 0 <= tile_y < self.tmx_data.height:
            return self.tile_layers[layer_name][tile_y][tile_x] != 0
        return False