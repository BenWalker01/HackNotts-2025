import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface


class Map:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("HackNotts25")
        self.load_map()

    def update_screen(self):
        self.screen.fill((0, 0, 0))
        render_width = self.image.get_width()
        render_height = self.image.get_height()
        render_surface = Surface((render_width, render_height))
        render_surface.blit(self.image, (0, 0))

        window_width, window_height = self.screen.get_size()
        render_ratio = render_width / render_height
        window_ratio = window_width / window_height
        if window_ratio <= render_ratio:
            rescaled_surf_width = window_width
            rescaled_surf_height = window_width // render_ratio
            rescaled_surf_x = 0
            rescaled_surf_y = (window_height - rescaled_surf_height) // 2
        else:
            rescaled_surf_width = int(window_height * render_ratio)
            rescaled_surf_height = window_height
            rescaled_surf_x = (window_width - rescaled_surf_width) // 2
            rescaled_surf_y = 0

        rescaled_surf = pygame.transform.scale(
            render_surface, (rescaled_surf_width, rescaled_surf_height))

        self.screen.blit(rescaled_surf, (rescaled_surf_x, rescaled_surf_y))

    def load_map(self):
        self. image = pygame.image.load("assets/toen/screen_cap_2.png")
