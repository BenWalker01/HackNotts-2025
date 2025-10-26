import pygame
import pyscroll
import pytmx

TILE_SIZE = 16


class Map:
    def __init__(self, path: str):
        """path: path to a .tmx file (or any identifier you like)."""
        self.path = path

        # display surface (one window for the whole game)
        # If another module already created the display, calling set_mode again is
        # harmless — it will just return the same display surface.
        self.screen = pygame.display.set_mode(
            (1024, 768), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("HackNotts25")

        # placeholders that will be set in load_map()
        self.tmx_data = None
        self.collision = []
        self.group = None
        self.entrances = []  # list of entrance dicts
        self.load_map()

    def update_screen(self):
        """Draw the pyscroll group to the display."""
        self.group.draw(self.screen)

    def load_map(self):
        """Load .tmx, build collision matrix, create pyscroll group and parse Entrances layer."""
        self.tmx_data = pytmx.util_pygame.load_pygame(self.path)
        map_data = pyscroll.data.TiledMapData(self.tmx_data)

        # collision matrix (False = walkable)
        self.collision = [[False for _ in range(self.tmx_data.width)]
                          for _ in range(self.tmx_data.height)]
        try:
            collision_layer = self.tmx_data.get_layer_by_name("Collision")
            for x, y, tile in collision_layer.tiles():
                if tile:
                    self.collision[y][x] = True
        except ValueError:
            # No Collision layer found; keep default empty collision
            pass

        # renderer
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size())
        map_layer.zoom = 3

        self.group = pyscroll.PyscrollGroup(
            map_layer=map_layer, default_layer=1)

        # parse Entrances object layer (optional)
        self.entrances = []
        try:
            entrances_layer = self.tmx_data.get_layer_by_name("Entrances")
            # Tiled object layers iterate through objects directly
            for obj in entrances_layer:
                props = {}
                # pytmx object properties are in obj.properties
                props["rect"] = pygame.Rect(
                    obj.x, obj.y, obj.width, obj.height)
                # Get optional properties: target_map, spawn_x, spawn_y, name
                props["target_map"] = obj.properties.get("target_map")
                props["spawn_x"] = obj.properties.get("spawn_x")
                props["spawn_y"] = obj.properties.get("spawn_y")
                props["name"] = obj.name or obj.properties.get("name")
                self.entrances.append(props)
        except ValueError:
            # No Entrances layer — caller can rely on hardcoded BUILDINGS fallback
            self.entrances = []

    def add_player(self, player_sprite):
        """Add player to the pyscroll group and update the group once so player appears."""
        # remove any existing instance of the same sprite to avoid duplicates:
        try:
            self.group.remove(player_sprite)
        except Exception:
            pass
        self.group.add(player_sprite, layer=999)
        self.group.update()

    def can_move_to(self, px: int, py: int) -> bool:
        """Return True if the pixel coordinate (px,py) is walkable.

        px,py are pixel positions (screen coordinates / player's sprite hitbox point).
        We convert to tile coordinates using TILE_SIZE.
        """
        tile_x = int(px / TILE_SIZE)
        tile_y = int(py / TILE_SIZE)
        if 0 <= tile_x < self.tmx_data.width and 0 <= tile_y < self.tmx_data.height:
            return not self.collision[tile_y][tile_x]
        # Outside the map bounds -> not walkable
        return False

    def add_npc(self, npc):
        """Add an NPC sprite to this map's drawing group."""
        self.group.add(npc, layer=998)  # slightly below player layer
