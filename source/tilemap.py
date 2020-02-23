import pygame
from pygame.sprite import Group, Sprite
from itertools import product
from .label import Label

class TileLayerData:
    def __init__(self, key=None, position=(0, 0), anchor="center"):
        self.key = key
        self.anchor = anchor
        self.position = position

    def set_rect(self, image, collide_by=4):
        self.rect = image.get_rect()
        self.rect.y = self.rect.height - (self.rect.height // collide_by)
        self.rect.height = self.rect.height // collide_by

class TileLayer:
    def draw(self, surface, position, images, player):
        pass

class TileSprite(Sprite):
    def __init__(self, image, position, anchor="topleft"):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(**{anchor: position})
        self.tile_position = pygame.Vector2(self.rect.center)
        self.map_position = pygame.Vector2(self.rect.center)

    def move(self, position, camera_position):
        self.tile_position += pygame.Vector2(position)
        self.map_position = self.tile_position - camera_position
        self.rect.center = self.map_position

    def update(self, camera_position):
        self.map_position = self.tile_position - camera_position
        self.rect.center = self.map_position

class TileMap:
    def __init__(self, images, screen_rect, tilesize):
        self.images = images
        self.map_data = [[]]
        self.map_size = 0, 0
        self.tilesize = tilesize
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.display_size = pygame.Vector2(int(screen_rect.w / tilesize) + 1,
                                           int(screen_rect.h / tilesize) + 1)

    def build_map(self, width, height):
        self.map_data = [[0 for x in range(width)] for y in range(height)]
        self.rect.size = width * self.tilesize, height * self.tilesize
        self.map_size = width, height

    def draw(self, surface, camera, player):
        x_pos = camera.position.x / self.tilesize
        y_pos = camera.position.y / self.tilesize
        x_range = self.get_range(camera.position.x, self.display_size.x, self.map_size[0])
        y_range = self.get_range(camera.position.y, self.display_size.y, self.map_size[1])
        for x, y in product(x_range, y_range):
            try:
                position = int((x - x_pos) * self.tilesize) , int((y - y_pos) * self.tilesize)
                tile = self.map_data[y][x]
                if isinstance(tile, TileLayer):
                    tile.draw(surface, position, self.images, player)
                else:
                    surface.blit(self.images[tile], position)
            except:
                pass

        player.draw(surface)

    def get_range(self, start, end, end_max):
        start = start / self.tilesize
        start_range = max(int(start), 0)
        end_range = min(int(start + end), end_max)
        return range(start_range, end_range)

# TileCamera moves the map. Not the player. Player would remain in the center.
class TileCamera:
    def __init__(self, position, tilemap, player):
        self.sprites = Group()
        self.tilemap = tilemap
        self.tilesprites = Group()
        self.position = pygame.Vector2(position)
        self.speed = 0.08
        self.player = player

    def draw(self, surface):
        self.tilemap.draw(surface, self, self.player)
        self.tilesprites.draw(surface)
        self.sprites.draw(surface)

    def update(self, delta):
        keys_pressed = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)
        triple = 1
        if keys_pressed[pygame.K_SPACE]:
            triple = 3

        if keys_pressed[pygame.K_w]:
            direction.y -= 1

        if keys_pressed[pygame.K_s]:
            direction.y += 1

        if keys_pressed[pygame.K_a]:
            direction.x -= 1

        if keys_pressed[pygame.K_d]:
            direction.x += 1

        if direction != pygame.Vector2(0, 0):
            direction.normalize_ip()
            self.position += direction * self.speed * delta * triple
            direction.x, direction.y = direction.y, direction.x
            angle = direction.as_polar()[1] - 90
            self.player.rotate(angle)

        self.tilesprites.update(self.position)
        self.sprites.update()
