import pygame
from map import Map
from player import Player
from npc import NPC
from game_loop import GameLoop


def main():
    pygame.init()

    # Load maps
    maps = {
        "main": Map("assets/tileset/baseMap.tmx"),
        "tavern": Map("assets/tileset/tavern.tmx"),
        "market": Map("assets/tileset/market.tmx"),
        "cottage": Map("assets/tileset/cottage.tmx"),
    }

    # Create player & NPCs
    player = Player(maps["main"])
    npcs = [NPC(maps["main"]) for _ in range(5)]
    for npc in npcs:
        maps[npc.map_name].add_npc(npc)

    # Start the main game loop
    game = GameLoop(player, maps, npcs)
    game.run()


if __name__ == "__main__":
    main()
