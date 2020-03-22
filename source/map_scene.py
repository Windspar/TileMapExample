import pygame
import random
from itertools import product
from .core.label import Label
from .core.scene import Scene
from .core.timer import Timer
from .images import Images
from .tilemap import *
from .tilelayer import TileLayer


class MapScene(Scene):
    def __init__(self, manager):
        Scene.__init__(self, manager)
        self.sprites = pygame.sprite.Group()
        self.images = Images()
        self.player = TilePlayer(self.images['manBlue_stand'], manager.rect.center)
        self.build_world()
        self.camera = TileCamera(self.tilemap.rect.center, self.tilemap, self.player)
        self.build_labels()
        self.background = pygame.Color('black')

        print(self.player.get_collsion_locations(self.camera.position, self.tilemap.tilesize))

    def build_labels(self):
        font = pygame.font.Font(None, 24)
        self.fps_label = Label("Fps: 0", font, pygame.Color("lawngreen"), self.manager.rect.topright, "topright")
        coords = (self.camera.position + pygame.Vector2(self.player.rect.center)) / self.tilemap.tilesize
        text = "X: {}, Y: {}".format(*map(int, coords))
        self.position_label = Label(text, font, pygame.Color("darkred"), self.manager.rect.topleft)
        ticks = pygame.time.get_ticks()
        self.timers = [Timer(ticks, 1000, self.timer_fps), Timer(ticks, 200, self.timer_position)]

        self.sprites.add(self.fps_label, self.position_label)

    def build_world(self):
        self.map_images = {"grass 1": self.images.get_tile(0, 0),
                           "grass 2": self.images.get_tile(1, 0),
                           "grass 3": self.images.get_tile(2, 0),
                           "grass 4": self.images.get_tile(3, 0),
                           "dirt 1": self.images.get_tile(4, 0),
                           "dirt 2": self.images.get_tile(5, 0),
                           "stone 1": self.images.get_tile(6, 0),
                           "stone 2": self.images.get_tile(7, 0)}

        self.object_images = {"bush": self.images.get_tile(20, 6),
                              "grass": self.images.get_tile(20, 7),
                              "leaves": self.images.get_tile(23, 7)}

        self.object_collision = ["bush"]

        self.layers = {'ground': self.map_images,
                       'object': self.object_images,
                       'object_collision': self.object_collision}

        self.tilemap = TileMap(self.images.tilesize, 1000, 1000, self.manager.rect, self.object_collision)

        ground_image_choices = list(self.map_images.keys())
        object_image_choices = list(self.object_images.keys())

        for x, y in product(range(1000), range(1000)):
            ground_key = random.choice(ground_image_choices)
            object_key = None
            if random.randint(0, 10) == 1:
                object_key = random.choice(object_image_choices)

            self.tilemap[(y, x)] = TileLayer(ground_key, object_key)

    def draw_tile(self, surface, tile, position):
        tile.draw(surface, position, self.layers)

    def timer_fps(self, timer):
        self.fps_label.set_text("FPS: {}".format(int(self.manager.clock.get_fps())))

    def timer_position(self, timer):
        coords = self.player.get_location(self.camera.position, self.tilemap.tilesize)
        text = "X: {}, Y: {}".format(int(coords.x), int(coords.y))
        self.position_label.set_text(text)

    def on_draw(self, surface):
        surface.fill(self.background)
        self.camera.draw(surface, self.draw_tile)
        self.sprites.draw(surface)

    def on_update(self, delta):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            self.camera.speed_boost = 5
        else:
            self.camera.speed_boost = 1

        self.camera.update(delta, keys_pressed)

        ticks = pygame.time.get_ticks()
        for timer in self.timers:
            timer.update(ticks)
