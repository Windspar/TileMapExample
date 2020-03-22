from pygame.sprite import Sprite
from pygame import Vector2


class TileSprite(Sprite):
    def __init__(self, image, position, anchor="topleft"):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(**{anchor: position})
        self.tile_position = Vector2(self.rect.center)
        self.map_position = Vector2(self.rect.center)

    def move(self, position, camera_position):
        self.tile_position += Vector2(position)
        self.map_position = self.tile_position - camera_position
        self.rect.center = self.map_position

    def update(self, camera_position):
        self.map_position = self.tile_position - camera_position
        self.rect.center = self.map_position
