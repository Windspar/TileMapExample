from pygame.transform import rotate as pygame_rotate
from pygame import Rect, Vector2


class TilePlayer:
    def __init__(self, image, position):
        self.original_image = image
        self.image = image
        self.rect = image.get_rect(center=position)
        self.buffer = []

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for layer, position in self.buffer:
            layer.draw(surface, position)

        self.buffer = []

    def get_location(self, position, tilesize):
        return (Vector2(self.rect.center) + position) / tilesize

    def get_collsion_locations(self, position, tilesize):
        size = min(self.rect.width, self.rect.height)
        rect = Rect(self.rect.topleft, (size, size))
        rect.center = self.rect.center
        points = rect.topleft, rect.topright, rect.bottomleft, rect.bottomright
        for point in points:
            return set([tuple(map(int, (point + position) / tilesize)) for point in points])

    def get_map_position(self, position):
        return Vector2(self.rect.center) + position

    def rotate(self, angle):
        self.image = pygame_rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
