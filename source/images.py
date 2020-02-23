import xml.etree.ElementTree as ET
from pygame import Rect
from pygame.image import load as image_load
from pygame.transform import scale as image_scale

class Images:
    def __init__(self):
        self.scale_by = 2
        self.characters = self.image_load_scale("resources/spritesheet_characters.png")
        self.characters_xml = self.read_xml("resources/spritesheet_characters.xml")
        self.tilesheet = self.image_load_scale("resources/tilesheet_ground.png")
        self.tilesheet_size = 27, 20
        self.tilesize = 32

    def read_xml(self, xmlfile):
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        result = {}

        for child in root:
            rect = Rect([int(child.get(attrib)) // self.scale_by for attrib in ['x', 'y', 'width', 'height']])
            result[child.get('name')[:-4]] = rect

        return result

    def image_load_scale(self, filename):
        image = image_load(filename).convert_alpha()
        size = image.get_size()
        size = int(size[0] // self.scale_by), int(size[1] // self.scale_by)
        return image_scale(image, size)

    def get_tile(self, x, y):
        rect = (x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize)
        return self.tilesheet.subsurface(rect)

    def __getitem__(self, key):
        if key in self.characters_xml:
            return self.characters.subsurface(self.characters_xml[key])
