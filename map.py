import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface
import pyscroll
import pytmx


class Map:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("HackNotts25")
        self.load_map()

    def update_screen(self):
        self.group.draw(self.screen)

    def load_map(self):
        tmx_data = pytmx.util_pygame.load_pygame("assets/tileset/baseMap.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size())
        map_layer.zoom = 3

        self.group = pyscroll.PyscrollGroup(
            map_layer=map_layer, default_layer=1)

    def add_player(self, player):
        self.group.add(player, layer=999)
        self.group.update()
        print("added player")
