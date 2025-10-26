import pygame
from map import Map
from player import Player
from game_loop import GameLoop

from npc import NPC

pygame.init()


def main():
    main_map = Map("assets/tileset/baseMap.tmx")

    player = Player(map)
    map.add_player(player)

    npcs = []

    maps = {
        "main": main_map,
        "tavern": Map("assets/tileset/tavern.tmx"),
        "market": Map("assets/tileset/market.tmx"),


    }

    for i in range(5):
        npc = NPC(map)
        map.add_player(npc)
        npcs.append(npc)

    game = GameLoop(player, map, npcs)
    game.run()


if __name__ == "__main__":
    main()
    pygame.quit()
