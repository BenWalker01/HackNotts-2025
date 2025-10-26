import pygame
from map import Map
from player import Player
from game import Game

from npc import NPC

pygame.init()


def main():
    map = Map()
    player = Player(map)
    map.add_player(player)

    npcs = []
    for i in range(5):
        npc = NPC(map)
        map.add_player(npc)
        npcs.append(npc)

    game = Game(player, map, npcs)
    game.run()


if __name__ == "__main__":
    main()
    pygame.quit()
