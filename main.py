import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface
from map import Map
from player import Player
from game import Game

pygame.init()

def main():
    # Load image and create window with default resolution
    window = pygame.display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)
    pygame.display.set_caption("Medieval Marketplace Game with Python")

    # The size of our game scene is the one of the image
    image = pygame.image.load("assets/toen/screen_cap_2.png")
    renderWidth = image.get_width()
    renderHeight = image.get_height()

    running = True
    while running:

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        # Render scene in a surface
        renderSurface = Surface((renderWidth, renderHeight))
        renderSurface.blit(image, (0, 0))

        # Scale rendering to window size
        windowWidth, windowHeight = window.get_size()
        renderRatio = renderWidth / renderHeight
        windowRatio = windowWidth / windowHeight
        if windowRatio <= renderRatio:
            rescaledSurfaceWidth = windowWidth
            rescaledSurfaceHeight = int(windowWidth / renderRatio)
            rescaledSurfaceX = 0
            rescaledSurfaceY = (windowHeight - rescaledSurfaceHeight) // 2
        else:
            rescaledSurfaceWidth = int(windowHeight * renderRatio)
            rescaledSurfaceHeight = windowHeight
            rescaledSurfaceX = (windowWidth - rescaledSurfaceWidth) // 2
            rescaledSurfaceY = 0

        # Scale the rendering to the window/screen size
        rescaledSurface = pygame.transform.scale(
            renderSurface, (rescaledSurfaceWidth, rescaledSurfaceHeight)
        )
        window.blit(rescaledSurface, (rescaledSurfaceX, rescaledSurfaceY))
        pygame.display.update()
    
    
if __name__ == "__main__":
    main()
    pygame.quit()