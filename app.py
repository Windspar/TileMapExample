import pygame
from source.core.scene import Manager
from source.map_scene import MapScene

def main():
    pygame.init()
    tiles = 20
    tilesize = 32
    width = tiles * tilesize * 2
    height = tiles * tilesize
    manager = Manager("Tile Map Example", width, height)
    manager.flip(MapScene(manager))
    manager.mainloop()

main()
