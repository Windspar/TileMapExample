from pygame.sprite import Sprite

class Label(Sprite):
    def __init__(self, text, font, color, position, anchor="topleft"):
        Sprite.__init__(self)
        self._text = text
        self._font = font
        self._color = color
        self._anchor = anchor
        self._position = position
        self.render()

    def render(self):
        self.image = self._font.render(self._text, 1, self._color)
        self.rect = self.image.get_rect(**{self._anchor: self._position})

    def set_text(self, text):
        self._text = text
        self.render()
