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
        self.load_map()

    def update_screen(self):
        self.group.draw(self.screen)

    def load_map(self):
        self.tmx_data = pytmx.util_pygame.load_pygame(
            "assets/tileset/baseMap.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)

        self.collision = [[False for _ in range(self.tmx_data.width)]
                          for _ in range(self.tmx_data.height)]
        collision_layer = self.tmx_data.get_layer_by_name("Collision")

        for x, y, tile in collision_layer.tiles():
            if tile:
                self.collision[y][x] = True

        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size())
        map_layer.zoom = 3

        self.group = pyscroll.PyscrollGroup(
            map_layer=map_layer, default_layer=1)

    def add_player(self, player):
        self.group.add(player, layer=999)
        self.group.update()
        print("added player")

    def can_move_to(self, px, py):
        tile_x = int(px / TILE_SIZE)
        tile_y = int(py / TILE_SIZE)
        if 0 <= tile_x < self.tmx_data.width and 0 <= tile_y < self.tmx_data.height:
            return not self.collision[tile_y][tile_x]
        return False
