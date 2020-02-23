import random
import pygame
from pygame.sprite import Sprite
from itertools import product
from .engine import Engine
from .images import Images
from .tilemap import *

class RotateSprite(Sprite):
    def __init__(self, image, position, anchor="topleft"):
        Sprite.__init__(self)
        self.original_image = image.copy()
        self.image = image
        self.rect = image.get_rect(**{anchor: position})

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

class Scene:
    def __init__(self):
        tiles = 20
        Engine.center_screen()
        self.engine = Engine("Example Tile Map", 32 * tiles * 2, 32 * tiles)
        self.images = Images()
        images = {"grass 1": self.images.get_tile(0, 0),
                  "grass 2": self.images.get_tile(1, 0),
                  "grass 3": self.images.get_tile(2, 0),
                  "grass 4": self.images.get_tile(3, 0),
                  "dirt 1": self.images.get_tile(4, 0),
                  "dirt 2": self.images.get_tile(5, 0),
                  "stone 1": self.images.get_tile(6, 0),
                  "stone 2": self.images.get_tile(7, 0)}

        self.player = RotateSprite(self.images['manBlue_stand'], self.engine.rect.center, "center")
        self.tilemap = TileMap(images, self.engine.rect, self.images.tilesize)
        self.tilemap.build_map(1000, 1000)
        images_choice = list(images.keys())
        for x, y in product(range(1000), range(1000)):
            self.tilemap.map_data[y][x] = random.choice(images_choice)

        self.camera = TileCamera(self.tilemap.rect.center, self.tilemap, self.player)

        font = pygame.font.Font(None, 24)
        self.fps_label = Label("FPS: 0", font, pygame.Color("lawngreen"), self.engine.rect.topright, "topright")
        self.fps_update_tick = 1000

        # Map coords
        x_pos = self.camera.position.x / self.tilemap.tilesize
        y_pos = self.camera.position.y / self.tilemap.tilesize
        text = "X: {},  Y: {}".format(x_pos, y_pos)
        self.map_label = Label(text, font, pygame.Color("navy"), (0, 0))
        self.map_update_tick = 100

        self.camera.sprites.add(self.fps_label, self.map_label)

    def on_draw(self, surface):
        surface.fill(pygame.Color('black'))
        surface.blit(self.images["manBlue_stand"], self.engine.rect.center)
        self.camera.draw(surface)

    def on_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.engine.quit()

    def on_update(self, delta):
        ticks = pygame.time.get_ticks()
        self.camera.update(delta)
        if ticks > self.fps_update_tick:
            self.fps_label.set_text("FPS: {}".format(int(self.engine.clock.get_fps())))
            self.fps_update_tick += 1000

        if ticks > self.map_update_tick:
            x_pos = self.camera.position.x / self.tilemap.tilesize
            y_pos = self.camera.position.y / self.tilemap.tilesize
            self.map_label.set_text("X: {},  Y: {}".format(x_pos, y_pos))
            self.map_update_tick += 100

    def mainloop(self):
        self.engine.running = True
        while self.engine.running:
            self.on_event()
            self.on_update(self.engine.delta)
            self.on_draw(self.engine.surface)
            pygame.display.flip()
            self.engine.idle()
