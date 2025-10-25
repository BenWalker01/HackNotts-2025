import pygame
pygame.init()

from map import Map

def main():
    map = Map()
    
    running = True
    while running:
        running = map.handle_event()
        map.update_screen()
        
        
    
    
if __name__ == "__main__":
    main()