from pygame import Surface


class TileLayer:
    def __init__(self, ground_key, object_key):
        self.ground_key = ground_key
        self.object_key = object_key
        self.render_image = None

    def draw(self, surface, position, layers):
        pos = tuple(map(int, position))
        if self.render_image:
            surface.blit(self.render_image, pos)
        else:
            self.render(layers)
            surface.blit(self.render_image, pos)

    def render(self, layers):
        self.render_image = Surface(layers["ground"][self.ground_key].get_size())
        self.render_image.blit(layers['ground'][self.ground_key], (0, 0))
        if self.object_key:
            self.render_image.blit(layers['object'][self.object_key], (0, 0))
