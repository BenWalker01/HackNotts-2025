import pygame
from map import Map
from player import Player
from game import Game

pygame.init()


def main():
    map = Map()
    player = Player(map)
    game = Game(player, map)
    game.run()


if __name__ == "__main__":
    main()
    pygame.quit()
