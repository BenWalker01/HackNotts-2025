import pygame
from map import Map
from player import Player
from game_loop import GameLoop

pygame.init()


def main():
    map = Map()
    player = Player(map)
    map.add_player(player)
    game = GameLoop(player, map)
    game.run()


if __name__ == "__main__":
    main()
    pygame.quit()
