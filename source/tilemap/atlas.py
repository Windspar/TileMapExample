from types import SimpleNamespace
from pygame import Rect, Vector2
from itertools import product


class TileMap:
    def __init__(self, tilesize, width, height, display_rect, tile_collision):
        self.tilesize = tilesize
        self.tile_collision = tile_collision
        self.mapsize = Vector2(width, height)
        self.rect = Rect(0, 0, width * tilesize, height * tilesize)
        self.tilemap = [["None" for w in range(width)] for h in range(height)]
        self.display_size = (Vector2(display_rect.size) / tilesize).elementwise() + 1

    def __getitem__(self, key):
        if isinstance(key, (tuple, list)):
            x, y = key
            return self.tilemap[y][x]

        return self.tilemap[key]

    def __setitem__(self, key, value):
        if isinstance(key, (tuple, list)):
            x, y = key
            self.tilemap[y][x] = value
        else:
            self.tilemap[key] = value

    def get_range(self, start_position, end_position, max_position):
        start = start_position / self.tilesize
        start_range = max(int(start), 0)
        end_range = min(int(start + end_position), int(max_position))
        return range(start_range, end_range)

    def get_visable_tiles(self, cam_position):
        location = cam_position / self.tilesize
        xrange = self.get_range(cam_position.x, self.display_size.x, self.mapsize.x)
        yrange = self.get_range(cam_position.y, self.display_size.y, self.mapsize.y)
        for x, y in product(xrange, yrange):
            position = (Vector2(x, y) - location) * self.tilesize
            yield self.tilemap[y][x], position
