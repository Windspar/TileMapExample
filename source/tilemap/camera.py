from pygame import K_w, K_a, K_d, K_s, K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.sprite import Group
from pygame import Rect, Vector2


class TileCameraKeys:
    def __init__(self, camera):
        self.camera = camera
        self.up = [K_w, K_UP]
        self.down = [K_s, K_DOWN]
        self.left = [K_a, K_LEFT]
        self.right = [K_d, K_RIGHT]

    def key_press(self, keys, keys_pressed):
        return any([keys_pressed[key] for key in keys])

    def update(self, delta, keys_pressed):
        direction = Vector2()
        if self.key_press(self.up, keys_pressed):
            direction.y -= 1

        if self.key_press(self.down, keys_pressed):
            direction.y += 1

        if self.key_press(self.left, keys_pressed):
            direction.x -= 1

        if self.key_press(self.right, keys_pressed):
            direction.x += 1

        if direction != Vector2():
            direction.normalize_ip()
            self.camera.move(direction, delta)

class TileCamera:
    def __init__(self, start_position, tilemap, tileplayer, speed=0.08, camera_keys=None):
        self.tilemap = tilemap
        self.tilesprites = Group()
        self.tileplayer = tileplayer
        self.position = Vector2(start_position)
        self.speed = speed
        self.speed_boost = 1

        if camera_keys is None:
            self.camera_keys = TileCameraKeys(self)
        else:
            self.camera_keys = camera_keys

    def collision(self, position):
        tilesize = self.tilemap.tilesize
        # old_position = self.tileplayer.get_map_position(self.position)
        # new_position = self.tileplayer.get_map_position(position)

        for point in self.tileplayer.get_collsion_locations(position, tilesize):
            if self.tilemap[point].object_key in self.tilemap.tile_collision:
                return

        self.position = position

    def draw(self, surface, callback):
        for tile, position in self.tilemap.get_visable_tiles(self.position):
            callback(surface, tile, position)
        self.tilesprites.draw(surface)
        self.tileplayer.draw(surface)

    def move(self, direction, delta):
        position = self.position + direction * self.speed * delta * self.speed_boost
        self.collision(position)

        direction.x, direction.y = direction.y, direction.x
        angle = direction.as_polar()[1] - 90
        self.tileplayer.rotate(angle)

    def update(self, delta, keys_pressed):
        self.camera_keys.update(delta, keys_pressed)
        self.tilesprites.update(self.position)
